"""Test the parse module."""
import pytest

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner, Symbol
from parse import Parser


@pytest.fixture
def parse_check_structure_no_INIT():
    """Return a Parser instance using 'check_structure_no_init.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_no_init.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_no_CONNECT():
    """Return a Parser instance using 'check_structure_no_con.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_no_con.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_no_MONITOR():
    """Return a Parser instance using 'check_structure_no_mon.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_no_mon.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_semicolon():
    """Return a Parser instance using 'check_semicolon.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_semicolon.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_keywords():
    """Return a Parser instance using 'check_keywords.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_keywords.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_missing_words():
    """Return a Parser instance using 'check_missing_words.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_missing_words.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_init():
    """Return a Parser instance using 'check_init.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_init.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_connect():
    """Return a Parser instance using 'check_connect.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_connect.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_monitor():
    """Return a Parser instance using 'check_monitor.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_monitor.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_network():
    """Return a Parser instance using 'check_network.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_network.txt'
    scanner = Scanner(path, names)
    return Parser(names, devices, network, monitors, scanner)  


def test_parse_no_INIT(parse_check_structure_no_INIT):

def test_parse_no_CONNECT(parse_check_structure_no_CONNECT):

def test_parse_no_MONITOR(parse_check_structure_no_MONITOR):

def test_parse_semicolon(parse_check_semicolon):

def test_parse_keywords(parse_check_keywords):

def test_parse_missing_words(parse_check_missing_words):

def test_parse_init(parse_check_init):

def test_parse_connect(parse_check_connect):

def test_parse_monitor(parse_check_monitor):

def test_parse_network(parse_check_network):