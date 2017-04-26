#-*- coding: utf-8 -*-

import rna_gen

def test_random_file():
    filename = rna_gen.get_random_filename("{random_file:test.txt}")
    assert filename == "test.txt"

def test_get_ip_address_from_file():
    ip_address = rna_gen.get_ip_address("{random_file:ip_address.txt}")
    assert ip_address is not None
    assert "{random_file:ip_address.txt}" in rna_gen.CACHE_IP_ADDRESS

def test_get_ip_address_string():
    ip_address = rna_gen.get_ip_address("211.42.242.170")
    assert ip_address == "211.42.242.170"
    assert "211.42.242.170" in rna_gen.CACHE_IP_ADDRESS
