"""Test the parse module."""
import pytest

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner, Symbol
from parse import Parser


@pytest.fixture
def parse_check_next_sentence():
    """Return a Parser instance using 'check_next_sentence.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_next_sentence.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_correct():
    """Return a Parser instance using 'check_structure_correct.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_correct.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_invalid():
    """Return a Parser instance using 'check_structure_invalid.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_invalid.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_semicolon():
    """Return a Parser instance using 'check_semicolon.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_semicolon.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_keywords():
    """Return a Parser instance using 'check_keywords.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_keywords.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner) 

'''
@pytest.fixture
def parse_check_missing_words():
    """Return a Parser instance using 'check_missing_words.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_missing_words.txt'
    scanner = Scanner(path, names,devices, network)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_init():
    """Return a Parser instance using 'check_init.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_init.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_connect():
    """Return a Parser instance using 'check_connect.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_connect.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner) 


@pytest.fixture
def parse_check_monitor():
    """Return a Parser instance using 'check_monitor.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_monitor.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_network():
    """Return a Parser instance using 'check_network.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_network.txt'
    scanner = Scanner(path, names, devices, network)
    return Parser(names, devices, network, monitors, scanner)  
'''

def test_go_to_next_sentence(parse_check_next_sentence):
    """Test the function go_to_next_sentence() go to the end of sentence."""
    scanner = parse_check_next_sentence.scanner
    # For first sentence, it will go to semicolon
    parse_check_next_sentence.symbol = scanner.get_symbol()
    parse_check_next_sentence.phase = 1
    parse_check_next_sentence.go_to_next_sentece()
    assert parse_check_next_sentence.symbol.type == scanner.SEMICOLON
    # For second sentence, it will go to EOF
    parse_check_next_sentence.symbol = scanner.get_symbol()
    parse_check_next_sentence.go_to_next_sentece()
    assert parse_check_next_sentence.symbol.type == scanner.EOF


def test_parse_structure_correct(parse_check_structure_correct):
    """Test check_structure() returns True when it's valid structure."""
    res = parse_check_structure_correct.check_structure()
    assert res == True


def test_parse_structure_invalid(parse_check_structure_invalid):
    """Test check_structure() returns False when it's invalid structure"""
    res = parse_check_structure_invalid.check_structure()
    assert res == False
    scanner = parse_check_structure_invalid.scanner
    # The error is missing start mark
    assert scanner.error.error_code == scanner.error.MISS_START_MARK


def test_parse_semicolon(parse_check_semicolon):
    """Test parse_semicolon() returns the expected results."""
    # If missing semicolon for start marks, it will not raise structure error
    res = parse_check_semicolon.check_structure()
    assert res == True

    # parsing missing semicolon
    scanner = parse_check_semicolon.scanner
    for i in range(10):
        scanner.get_symbol()
    parse_check_semicolon.symbol = scanner.get_symbol()
    parse_check_semicolon.phase = 1
    parse_check_semicolon.parse_semicolon()
    assert scanner.error.error_code == scanner.error.MISS_TERMINATION


def test_parse_keywords(parse_check_keywords):
    """Test handle_unexpected_keyword() returns the expected results"""
    scanner = parse_check_keywords.scanner
    # parse the wrong keywords in initialisation
    for i in range(8):
        scanner.get_symbol()
    parse_check_keywords.symbol = scanner.get_symbol()
    parse_check_keywords.expect_type = scanner.DEVICE_TYPE
    parse_check_keywords.phase = 1
    bool1, bool2 = parse_check_keywords.handle_unexpected_keyword()
    assert bool1 == True, bool2 == False
    assert scanner.error.error_code == scanner.error.INIT_MISS_KEYWORD

    # parse
    for i in range(16):
        scanner.get_symbol()
    parse_check_keywords.symbol = scanner.get_symbol()
    parse_check_keywords.expect_type = scanner.DEVICE_TYPE
    parse_check_keywords.phase = 1
    bool1, bool2 = parse_check_keywords.handle_unexpected_keyword()
    assert bool1 == True, bool2 == False
    assert scanner.error.error_code == scanner.error.INIT_MISS_KEYWORD

    for i in range(34):
        scanner.get_symbol()
    parse_check_keywords.symbol = scanner.get_symbol()
    parse_check_keywords.expect_type = scanner.DEVICE_IN
    parse_check_keywords.phase = 2
    bool1, bool2 = parse_check_keywords.handle_unexpected_keyword()
    assert bool1 == True, bool2 == False
    assert scanner.error.error_code == scanner.error.KEYWORD_NOT_FOUND

'''
def test_parse_missing_words(parse_check_missing_words):

def test_parse_init(parse_check_init):

def test_parse_connect(parse_check_connect):

def test_parse_monitor(parse_check_monitor):

def test_parse_network(parse_check_network):'''