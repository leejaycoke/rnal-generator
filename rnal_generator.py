#-*- coding: utf-8 -*-

import re
import sys
import random
import socket
import struct
import json
from datetime import datetime

HTTP_METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'HEAD']

LOG_FORMAT = '{ip_address} - - [{date}:{time} {time_offset}] "{method} {path} HTTP/1.1" 200 {bytes_sent} "-" "{user_agent}"'

RANDOM_FILE_PATTERN = re.compile(r"^{random_file:(?P<filename>.+)}$")
RANDOM_TIME_PATTERN = re.compile(r"^{random_time:(?P<time>[0-9:,]{17})}$")
RANDOM_INT_PATTERN = re.compile(
    r"^{random_int:(?P<start>[0-9]+)\,(?P<end>[0-9]+)}$")

RANDOM_INT_FINDER = re.compile(r"{random_int:[0-9]+\,[0-9]+}")
RANDOM_FILE_FINDER = re.compile(r"{random_file:.+}")

CACHE_IP_ADDRESS = {}
CACHE_TIME = {}
CACHE_PATH = {}
CACHE_FILE = {}
CACHE_USER_AGENT = {}


def get_random_filename(value):
    match = RANDOM_FILE_PATTERN.match(value)
    if match:
        return match.groupdict().get('filename')
    return None


def get_random_time_range(value):
    match = RANDOM_TIME_PATTERN.match(value)
    if match:
        return match.groupdict().get('time').split(',')
    return None


def read_lines_from_file(filename):
    if filename not in CACHE_FILE:
        with open('./' + filename) as fp:
            CACHE_FILE[filename] = [line.strip() for line in fp.readlines()]
    return CACHE_FILE[filename]


def get_ip_address(value):
    if value not in CACHE_IP_ADDRESS:
        filename = get_random_filename(value)
        if filename:
            lines = read_lines_from_file(filename)
            CACHE_IP_ADDRESS[value] = lines
        else:
            CACHE_IP_ADDRESS[value] = [value]

    return random.choice(CACHE_IP_ADDRESS[value])


def get_time(value):
    if value not in CACHE_TIME:
        time_range = get_random_time_range(value)
        if time_range:
            sh, sm, ss = time_range[0].split(':')
            eh, em, es = time_range[1].split(':')

            CACHE_TIME[value] = int(sh), int(eh), int(
                sm), int(em), int(ss), int(es)
        else:
            CACHE_TIME[value] = value

    if isinstance(CACHE_TIME[value], tuple):
        sh, eh, sm, em, ss, es = CACHE_TIME[value]
        return "%02d:%02d:%02d" % (
            random.randint(sh, eh),
            random.randint(sm, em),
            random.randint(ss, es)
        )
    return CACHE_TIME[value]


def get_path(value):
    random_ints = RANDOM_INT_FINDER.findall(value)
    if random_ints:
        for random_int in random_ints:
            args = random_int.split(',')
            start, end = int(args[0].split(':')[1]), int(args[1].split('}')[0])
            value = value.replace(random_int, str(random.randint(start, end)))

    random_files = RANDOM_FILE_FINDER.findall(value)
    if random_files:
        for random_file in random_files:
            filename = random_file.split(':')[1].split('}')[0]
            lines = read_lines_from_file(filename)
            value = value.replace(random_file, random.choice(lines))
    return value


def get_bytes_sent(value):
    match = RANDOM_INT_PATTERN.match(value)
    if match:
        groups = match.groupdict()
        random_int = random.randint(int(groups['start']), int(groups['end']))
        return str(random_int)
    return value


def get_user_agent(value):
    if value not in CACHE_USER_AGENT:
        match = RANDOM_FILE_PATTERN.match(value)
        if match:
            filename = match.groupdict()['filename']
            lines = read_lines_from_file(filename)
            CACHE_USER_AGENT[value] = lines
        else:
            CACHE_USER_AGENT[value] = [value]

    return random.choice(CACHE_USER_AGENT[value])


def process(config):
    for _ in range(int(config['count'])):
        line = LOG_FORMAT.format(**{
            'ip_address': get_ip_address(config['ip_address']),
            'date': config['date'],
            'time': get_time(config['time']),
            'time_offset': config['time_offset'],
            'method': config['method'],
            'path': get_path(config['path']),
            'bytes_sent': get_bytes_sent(config['bytes_sent']),
            'user_agent': get_user_agent(config['user_agent'])}
        )
        print(line)


def main(configs):
    for config in configs:
        process(config)


def read_config():
    with open('./line.conf') as fp:
        lines = fp.readlines()[1:]

    configs = []
    for columns in [line.split() for line in lines]:
        configs.append(
            {
                'count': columns[0],
                'ip_address': columns[1],
                'date': columns[2],
                'time': columns[3],
                'time_offset': columns[4],
                'method': columns[5],
                'path': columns[6],
                'bytes_sent': columns[7],
                'user_agent': columns[8]
            }
        )
    return configs


if __name__ == "__main__":
    config = read_config()
    main(config)
