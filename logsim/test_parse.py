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
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_correct():
    """Return a Parser instance using 'check_structure_correct.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_correct.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_invalid_start_mark():
    """Return a Parser instance using 'check_structure_invalid.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_invalid.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_structure_miss_sentence():
    """Return a Parser instance using check_structure_invalid_sentence.txt'"""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_structure_invalid_sentence.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_semicolon():
    """Return a Parser instance using 'check_semicolon.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_semicolon.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_keywords():
    """Return a Parser instance using 'check_keywords.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_keywords.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_init():
    """Return a Parser instance using 'check_init.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_init.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_connect():
    """Return a Parser instance using 'check_connect.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_connect.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_connect_rc():
    """Return a Parser instance using 'check_connect_rc.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_connect_rc.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_monitor():
    """Return a Parser instance using 'check_monitor.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_monitor.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_monitor_dup():
    """Return a Parser instance using 'check_monitor.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_monitor_duplicate.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_network():
    """Return a Parser instance using 'check_network.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_network.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_oscillate():
    """Return a Parser instance using 'check_network_oscillate.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_network_oscillate.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


@pytest.fixture
def parse_check_unused():
    """Return a Parser instance using 'check_network_unused.txt'."""
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    path = 'parse_test_files/check_network_unused.txt'
    scanner = Scanner(path, names, devices, network, monitors)
    return Parser(names, devices, network, monitors, scanner)


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
    assert res


def test_parse_structure_invalid(parse_check_structure_invalid_start_mark):
    """Test check_structure() returns False when it's invalid structure"""
    res = parse_check_structure_invalid_start_mark.check_structure()
    assert not res
    scanner = parse_check_structure_invalid_start_mark.scanner
    # The error is missing start mark
    assert scanner.error.error_code == scanner.error.MISS_START_MARK


def test_parse_structure_miss_sentence(parse_check_structure_miss_sentence):
    """Test check_structure() returns False when it's invalid structure"""
    res = parse_check_structure_miss_sentence.check_structure()
    assert not res
    scanner = parse_check_structure_miss_sentence.scanner
    # The error is missing sentence
    print(scanner.error.error_code)
    assert scanner.error.error_code == scanner.error.MISS_DESCRIPTION


def test_parse_semicolon(parse_check_semicolon):
    """Test parse_semicolon() returns the expected results."""
    # If missing semicolon for start marks, it will not raise structure error
    res = parse_check_semicolon.check_structure()
    assert res

    # parsing missing semicolon
    scanner = parse_check_semicolon.scanner
    for i in range(10):
        scanner.get_symbol()
    parse_check_semicolon.symbol = scanner.get_symbol()
    parse_check_semicolon.phase = 1
    parse_check_semicolon.parse_semicolon()
    assert scanner.error.error_code == scanner.error.MISS_TERMINATION


def test_parse_keywords_init(parse_check_keywords):
    """Test handle_unexpected_keyword() returns the expected results"""
    scanner = parse_check_keywords.scanner
    parse_check_keywords.new_line = False
    # parse the wrong keywords in initialisation
    for i in range(8):
        scanner.get_symbol()
    parse_check_keywords.symbol = scanner.get_symbol()
    parse_check_keywords.expect_type = scanner.DEVICE_TYPE
    parse_check_keywords.phase = 1
    bool1, bool2 = parse_check_keywords.handle_unexpected_keyword()
    assert bool1, not bool2
    # The error type is missing keyword in initialisation
    assert scanner.error.error_code == scanner.error.INIT_MISS_KEYWORD


def test_parse_keywords_connect(parse_check_keywords):
    """Test handle_unexpected_keyword() returns the expected results"""
    scanner = parse_check_keywords.scanner
    parse_check_keywords.new_line = False
    # parse the wrong keywords in connection
    for i in range(61):
        scanner.get_symbol()
    parse_check_keywords.symbol = scanner.get_symbol()
    parse_check_keywords.expect_type = scanner.DEVICE_IN
    parse_check_keywords.phase = 2
    bool1, bool2 = parse_check_keywords.handle_unexpected_keyword()
    assert bool1, not bool2
    # The error type is invalid device input in connection
    assert scanner.error.error_code == scanner.error.CONNECT_WRONG_IO


def test_parse_init(parse_check_init):
    """Test parse_init() parsing the initialisation section."""
    scanner = parse_check_init.scanner
    parse_check_init.device_holder = parse_check_init.init_device_holder()
    parse_check_init.phase = 1
    for i in range(6):
        scanner.get_symbol()
    parse_check_init.new_line = True

    # parse line 2 symbol by symbol
    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.INIT_IS

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.DEVICE_TYPE

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.INIT_SWITCH

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.NUMBER

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err == scanner.error.INIT_WRONG_SET

    # parse line 3 no error
    parse_check_init.new_line = True
    parse_check_init.symbol = scanner.get_symbol()
    sym = parse_check_init.symbol
    err, expect_type = parse_check_init.parse_init()
    assert err is None

    # parse line 4 raise error for DEVICE_PRESENT
    for i in range(3):
        scanner.get_symbol()
    parse_check_init.new_line = True
    parse_check_init.devices.make_device(sym.id,
                                parse_check_init.devices.D_TYPE)
    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err == parse_check_init.devices.DEVICE_PRESENT

    # parse raise error INVALID_QUALIFIER for AND gate
    parse_check_init.new_line = True
    err, expect_type = parse_check_init.parse_init()
    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.INIT_IS

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.DEVICE_TYPE

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.INIT_WITH

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err is None, expect_type == scanner.NUMBER

    parse_check_init.symbol = scanner.get_symbol()
    err, expect_type = parse_check_init.parse_init()
    assert err == parse_check_init.devices.INVALID_QUALIFIER


def test_parse_connect(parse_check_connect):
    """Test parse_connect() parsing the connection section."""
    # test for device output undefined
    scanner = parse_check_connect.scanner
    parse_check_connect.connection_holder = (parse_check_connect
                                             .init_connection_holder())
    parse_check_connect.phase = 2
    parse_check_connect.new_line = True
    parse_check_connect.symbol = scanner.get_symbol()
    err, expected_type = parse_check_connect.parse_connect()
    assert err == parse_check_connect.network.DEVICE_ABSENT

    # test for dtype.CLK
    parse_check_connect.names.lookup(["D1"])
    sym_id = parse_check_connect.names.query("D1")
    parse_check_connect.devices.make_device(sym_id,
                                        parse_check_connect.devices.D_TYPE)
    parse_check_connect.names.lookup(["SW1"])
    sym_id = parse_check_connect.names.query("SW1")
    parse_check_connect.devices.make_device(sym_id,
                                        parse_check_connect.devices.SWITCH, 1)
    parse_check_connect.names.lookup(["SW2"])
    sym_id = parse_check_connect.names.query("SW2")
    parse_check_connect.devices.make_device(sym_id,
                                        parse_check_connect.devices.SWITCH, 0)
    parse_check_connect.names.lookup(["SW3"])
    sym_id = parse_check_connect.names.query("SW3")
    parse_check_connect.devices.make_device(sym_id,
                                        parse_check_connect.devices.SWITCH, 0)
    sym = scanner.get_symbol()
    parse_check_connect.new_line = True

    # Test when clk input to dtype is not clock
    parse_check_connect.symbol = sym
    parse_check_connect.parse_connect()
    parse_check_connect.symbol = scanner.get_symbol()
    parse_check_connect.parse_connect()
    parse_check_connect.symbol = scanner.get_symbol()
    err, expected_type = parse_check_connect.parse_connect()
    assert err == parse_check_connect.scanner.error.NOT_CLOCK_TO_CLK

    # test when that it does not raise an error with duplication
    parse_check_connect.symbol = scanner.get_symbol()
    err, expected_type = parse_check_connect.parse_connect()
    assert err is None


def test_parse_connect_rc(parse_check_connect_rc):
    """Test parse_connect() parsing the connection section."""
    # test for device output undefined
    scanner = parse_check_connect_rc.scanner
    parse_check_connect_rc.connection_holder = (parse_check_connect_rc
                                             .init_connection_holder())
    parse_check_connect_rc.phase = 2
    parse_check_connect_rc.new_line = True
    parse_check_connect_rc.expect_type = (parse_check_connect_rc
                                          .scanner.DEVICE_OUT)

    parse_check_connect_rc.names.lookup(["D1"])
    sym_id = parse_check_connect_rc.names.query("D1")
    parse_check_connect_rc.devices.make_device(sym_id,
                                        parse_check_connect_rc.devices.D_TYPE)
    parse_check_connect_rc.names.lookup(["OR1"])
    sym_id = parse_check_connect_rc.names.query("OR1")
    parse_check_connect_rc.devices.make_device(sym_id,
                                        parse_check_connect_rc.devices.OR, 1)
    parse_check_connect_rc.names.lookup(["RC1"])
    sym_id = parse_check_connect_rc.names.query("RC1")
    parse_check_connect_rc.devices.make_device(sym_id,
                                        parse_check_connect_rc.devices.RC, 10)

    # Test when RC input is not to a DTYPE
    parse_check_connect_rc.symbol = scanner.get_symbol()
    parse_check_connect_rc.parse_connect()
    parse_check_connect_rc.symbol = scanner.get_symbol()
    parse_check_connect_rc.parse_connect()
    parse_check_connect_rc.symbol = scanner.get_symbol()
    err, expected_type = parse_check_connect_rc.parse_connect()
    assert err == parse_check_connect_rc.scanner.error.NOT_RC_TO_D_TYPE

    # Test when RC input is not to a DTYPE SET or CLEAR
    parse_check_connect_rc.symbol = scanner.get_symbol()  # this is semicolon
    parse_check_connect_rc.new_line = True
    parse_check_connect_rc.expect_type = (parse_check_connect_rc
                                          .scanner.DEVICE_OUT)
    parse_check_connect_rc.symbol = scanner.get_symbol()
    parse_check_connect_rc.parse_connect()
    parse_check_connect_rc.symbol = scanner.get_symbol()
    parse_check_connect_rc.parse_connect()
    parse_check_connect_rc.symbol = scanner.get_symbol()
    err, expected_type = parse_check_connect_rc.parse_connect()
    assert err == parse_check_connect_rc.scanner.error.NOT_RC_TO_D_TYPE

def test_parse_monitor(parse_check_monitor):
    """Test parse_monitor() parsing the monitor section"""
    scanner = parse_check_monitor.scanner
    parse_check_monitor.phase = 3
    parse_check_monitor.names.lookup(["AND1"])
    sym_id = parse_check_monitor.names.query("AND1")
    parse_check_monitor.devices.make_device(sym_id,
                                parse_check_monitor.devices.AND, 2)
    parse_check_monitor.new_line = True
    # test for invalid monitor point
    for i in range(2):
        scanner.get_symbol()
    parse_check_monitor.symbol = scanner.get_symbol()
    parse_check_monitor.parse_monitor()
    parse_check_monitor.symbol = scanner.get_symbol()
    err, expected_type = parse_check_monitor.parse_monitor()
    assert err == parse_check_monitor.network.DEVICE_ABSENT

    parse_check_monitor.symbol = scanner.get_symbol()
    err, expected_type = parse_check_monitor.parse_monitor()
    assert err is None


def test_parse_monitor_dup(parse_check_monitor_dup):
    """Test parse_monitor() parsing the monitor section"""
    scanner = parse_check_monitor_dup.scanner
    parse_check_monitor_dup.phase = 3
    parse_check_monitor_dup.names.lookup("D1")
    sym_id = parse_check_monitor_dup.names.query("D1")
    parse_check_monitor_dup.devices.make_device(sym_id,
                                    parse_check_monitor_dup.devices.D_TYPE)
    parse_check_monitor_dup.new_line = True
    # test for invalid monitor point
    for i in range(2):
        scanner.get_symbol()

    # test for duplicate monitor point
    parse_check_monitor_dup.symbol = scanner.get_symbol()
    parse_check_monitor_dup.parse_monitor()
    parse_check_monitor_dup.symbol = scanner.get_symbol()
    parse_check_monitor_dup.parse_monitor()
    parse_check_monitor_dup.symbol = scanner.get_symbol()
    err, expected_type = parse_check_monitor_dup.parse_monitor()
    assert err == parse_check_monitor_dup.monitors.MONITOR_PRESENT


def test_parse_network(parse_check_network):
    """Test parse_network() correctly build circuits"""
    # parser return True for correct description file
    res = parse_check_network.parse_network()
    assert res is True

    # check for devices
    devices = parse_check_network.devices
    assert len(devices.find_devices(devices.SWITCH)) == 3
    assert len(devices.find_devices(devices.D_TYPE)) == 1
    assert len(devices.find_devices(devices.AND)) == 1
    assert len(devices.find_devices(devices.CLOCK)) == 1

    # check for network
    network = parse_check_network.network
    assert network.check_network()


def test_parse_network_oscillate(parse_check_oscillate):
    """Test parse_network() circuits oscillates"""
    # parser return True for correct description file
    res = parse_check_oscillate.parse_network()
    assert res is False

    scanner = parse_check_oscillate.scanner
    # The error is missing start mark
    assert scanner.error.error_code == scanner.error.OSCILLATE


def test_parse_network_unused_inputs(parse_check_unused):
    """Test parse_network() circuits oscillates"""
    # parser return True for correct description file
    res = parse_check_unused.parse_network()
    assert res is False

    scanner = parse_check_unused.scanner
    # The error is missing start mark
    assert scanner.error.error_code == scanner.error.UNUSED_INPUTS
