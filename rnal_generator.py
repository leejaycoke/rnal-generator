#-*- coding: utf-8 -*-

"""
Name.
Describe what this script does

Usage:
 rna-gen path <path> [--count-range=<count-range] [--method=<method>] [--timedelta=<timedelta>] [--user-agent=<user-agent>] [--date=<date>] [--success-rate=<success-rate>]

Options:
  -h --help     Show this screen.
"""

import re
import sys
import random
import socket
import struct
import json
from datetime import datetime

HTTP_METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'HEAD']

LOG_FORMAT = """{ip_address} - - [{date}:{time} {timedelta}] "{method} {path} HTTP/1.1" 200 {sent} \
"-" "{useragent}"""

RANDOM_FILE_PATTERN = re.compile(r"^{random_file:(?P<filename>.+)}$")

def get_random_filename(value):
    match = RANDOM_FILE_PATTERN.match(value)
    if match:
        return match.groupdict().get('filename')
    return None

def read_lines_from_file(filename):
    with open('./' + filename) as fp:
        lines = fp.readlines()
        return [line.strip() for line in lines]

CACHE_IP_ADDRESS = {}
def get_ip_address(ip_config):
    if ip_config in CACHE_IP_ADDRESS:
        return random.choice(CACHE_IP_ADDRESS[ip_config])

    filename = get_random_filename(ip_config)
    if filename:
        lines = read_lines_from_file(filename)
        CACHE_IP_ADDRESS[ip_config] = lines
    else:
        CACHE_IP_ADDRESS[ip_config] = [ip_config]

    return random.choice(CACHE_IP_ADDRESS[ip_config])

def process(config):
    ip_address = get_ip_address(config['ip_address'])
    date = get_date(config['date'])
    time = get_time(config['time'])
    time_offset = config['time_offset']
    method = config['method']
    path = get_path(config['path'])
    bytes_sent = get_bytes_sent(config['bytes_sent'])
    user_agent = get_user_agent(config['user_agent'])

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
    print(config)
    main(config)

# 50.1.1.1 - example [23/Sep/2016:19:00:00 +0000] "POST /api/is_individual
# HTTP/1.1" 200 58 "-" "python-requests/2.7.0 CPython/2.7.6
# Linux/3.13.0-36-generic"

"""

"""
