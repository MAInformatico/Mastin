import os
import pytest
from checker import checker

# data for testing
HOSTS_CONTENT = """192.168.1.1
192.168.1.2
192.168.1.3
"""
DICTIONARY_CONTENT = """192.168.1.1 router
192.168.1.2 laptop-mike
192.168.1.3 tv-salon
"""

@pytest.fixture
def setup_files(tmp_path):
    hosts_file = tmp_path / "hosts.txt"
    dictionary_file = tmp_path / "dictionary.txt"
    hosts_file.write_text(HOSTS_CONTENT)
    dictionary_file.write_text(DICTIONARY_CONTENT)
    return str(hosts_file), str(dictionary_file)

def test_get_ips(setup_files):
    hosts_file, _ = setup_files
    c = checker()
    ips = c.getIPs(hosts_file)
    assert ips == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

def test_read_file(setup_files):
    _, dictionary_file = setup_files
    c = checker()
    data = c.readFile(dictionary_file)
    assert data["192.168.1.1"] == "router"
    assert data["192.168.1.2"] == "laptop-mike"

def test_get_hostname(setup_files):
    _, dictionary_file = setup_files
    c = checker()
    assert c.getHostname("192.168.1.1", dictionary_file) == "router"
    assert c.getHostname("192.168.1.99", dictionary_file) is None

def test_get_hosts(setup_files):
    hosts_file, dictionary_file = setup_files
    c = checker()
    c.hosts_file = hosts_file
    c.dictionary_file = dictionary_file
    hosts = c.getHosts()
    assert hosts == ["router", "laptop-mike", "tv-salon"]