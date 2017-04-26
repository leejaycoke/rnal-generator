#-*- coding: utf-8 -*-

import re
import rnal_generator as gen

def test_random_file():
    filename = gen.get_random_filename("{random_file:test.txt}")
    assert filename == "test.txt"

def test_get_ip_address_from_file():
    ip_address = gen.get_ip_address("{random_file:ip_address.txt}")
    assert ip_address is not None
    assert "{random_file:ip_address.txt}" in gen.CACHE_IP_ADDRESS

def test_get_string_ip_address():
    ip_address = gen.get_ip_address("211.42.242.170")
    assert ip_address == "211.42.242.170"
    assert "211.42.242.170" in gen.CACHE_IP_ADDRESS

def test_get_random_time_range():
    value = "{random_time:00:00:00,23:59:59}"
    result = gen.get_random_time_range(value)
    assert result == ['00:00:00', '23:59:59']

def test_get_random_time():
    value = "{random_time:00:00:00,23:59:59}"
    result = gen.get_time(value)
    assert result is not None
    assert len(result) == 8

def test_get_string_time():
    value = "21:00:09"
    result = gen.get_time(value)
    assert result == "21:00:09"

def test_string_path():
    value = "/users"
    assert gen.get_path(value) == "/users"

def test_random_int_pattern_path():
    value = "/users/{random_int:213,2135}"
    path = gen.get_path(value)
    match = re.compile(r"^\/users\/[0-9]+$").match(path)
    assert match is not None

def test_random_multi_int_pattern_path():
    value = "/users/{random_int:213,2135}/{random_int:0,0}"
    path = gen.get_path(value)
    match = re.compile(r"^\/users\/[0-9]+\/0$").match(path)
    assert match is not None

def test_random_file_pattern_path():
    value = "/users/{random_file:integer.txt}"
    path = gen.get_path(value)
    match = re.compile(r"^\/users\/[0-9]+$").match(path)
    assert match is not None

def test_complex_random_pattern_path():
    value = "/users/{random_file:integer.txt}/{random_int:0,0}"
    path = gen.get_path(value)
    match = re.compile(r"^\/users\/[0-9]\/0+$").match(path)
    assert match is not None

def test_random_int_bytes_sent():
    value = "{random_int:0,0}"
    assert gen.get_bytes_sent(value) == "0"

def test_single_int_bytes_sent():
    value = "1"
    assert gen.get_bytes_sent(value) == "1"

def test_random_file_user_agent():
    user_agent = "foo"
    assert gen.get_user_agent(user_agent) == "foo"

def test_random_file_user_agent():
    user_agent = "{random_file:user_agent.txt}"
    assert gen.get_user_agent(user_agent) is not None

def test_line():
    assert False
