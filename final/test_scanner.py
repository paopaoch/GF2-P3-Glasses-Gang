"""Test the scanner module."""
import pytest

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner, Symbol


@pytest.fixture
def scanner_example_1():
    """Return a new instance of the Scanner class."""
    names_1 = Names()
    devices_1 = Devices(names_1)
    network_1 = Network(names_1, devices_1)
    monitors_1 = Monitors(names_1, devices_1, network_1)
    filename_1 = 'scanner_test_files/scanner_example_file_1.txt'
    return Scanner(filename_1, names_1, devices_1, network_1, monitors_1)


@pytest.fixture
def scanner_example_2():
    """Return a new instance of the Scanner class."""
    names_2 = Names()
    devices_2 = Devices(names_2)
    network_2 = Network(names_2, devices_2)
    monitors_2 = Monitors(names_2, devices_2, network_2)
    filename_2 = 'scanner_test_files/scanner_example_file_2.txt'
    return Scanner(filename_2, names_2, devices_2, network_2, monitors_2)


@pytest.fixture
def scanner_example_3():
    """Return a new instance of the Scanner class."""
    names_3 = Names()
    devices_3 = Devices(names_3)
    network_3 = Network(names_3, devices_3)
    monitors_3 = Monitors(names_3, devices_3, network_3)
    filename_3 = 'scanner_test_files/scanner_example_file_3.txt'
    return Scanner(filename_3, names_3, devices_3, network_3, monitors_3)


def test_get_name(scanner_example_1):
    """Test if get_name() return alphabets."""
    scanner_example_1.current_char = scanner_example_1.read_file()
    name = scanner_example_1.get_name()
    assert name == "AND"


def test_get_number(scanner_example_1):
    """Test if get_number() return digits."""
    scanner_example_1.file.seek(6)
    scanner_example_1.current_char = scanner_example_1.read_file()
    number = scanner_example_1.get_number()
    assert number == "123"


def test_get_symbol(scanner_example_1):
    """Test if get_symbol() return a correct Symbol type."""
    sym = scanner_example_1.get_symbol()        # sym is device type "AND"
    assert sym.type == scanner_example_1.DEVICE_TYPE
    assert scanner_example_1.names.get_name_string(sym.id) == "AND"
    assert sym.pos == 3                         # position of last character
    assert sym.line_pos == 0                    # position of start of a line

    scanner_example_1.get_symbol()
    sym = scanner_example_1.get_symbol()        # sym is device input "G123.I7"
    assert sym.type == scanner_example_1.DEVICE_IN
    assert scanner_example_1.names.get_name_string(sym.id) == "G123.I7"
    assert sym.pos == 12
    assert sym.line_pos == 5

    sym = scanner_example_1.get_symbol()        # sym is SIGGEN waveform
    assert sym.type == scanner_example_1.SIGGEN_WAVE
    assert scanner_example_1.names.get_name_string(sym.id) == "101"

    sym = scanner_example_1.get_symbol()        # sym is EOF
    assert sym.type == scanner_example_1.EOF


def test_skip_valid_comment(scanner_example_2):
    """Test if skip_comment() is able to skip valid comment."""
    sym = scanner_example_2.get_symbol()     # sym is "INIT" after comment
    assert sym.type == scanner_example_2.INIT


def test_report_invalid_comment(scanner_example_2):
    """Test if skip_comment() is able to report invalid comment."""
    scanner_example_2.get_symbol()
    scanner_example_2.get_symbol()
    scanner_example_2.get_symbol()
    assert (scanner_example_2.error.error_code
            == scanner_example_2.error.INVALID_COMMENT)


def test_get_line_position(scanner_example_1):
    """Test if get_line_position() return a correct line number."""
    sym = scanner_example_1.get_symbol()                     # sym is "AND"
    line_number = scanner_example_1.get_line_position(sym)   # line number is 1
    assert line_number == 1

    scanner_example_1.get_symbol()
    sym = scanner_example_1.get_symbol()                     # sym is "G123.I7"
    line_number = scanner_example_1.get_line_position(sym)   # line number is 2
    assert line_number == 2


def test_get_pointer(scanner_example_3):
    """Test if get_pointer() return a correct pointer.

    The pointer message returned should be the whole line where
    the symbol is located, with the pointer points to the end
    character of that symbol.
    """
    scanner_example_3.get_symbol()
    scanner_example_3.get_symbol()
    sym = scanner_example_3.get_symbol()   # sym "d1" invalid device name error
    pointer_msg = scanner_example_3.get_pointer(sym)
    assert pointer_msg == "INIT; d1 is DTYPE;" + '\n' + "       ^"


def test_get_pointer_front(scanner_example_3):
    """Test if get_pointer(front=True) return a correct pointer.

    The pointer message returned should be the whole line where
    the symbol is located, with the pointer points to the start
    character of that symbol.
    """
    for i in range(7):
        scanner_example_3.get_symbol()
    sym = scanner_example_3.get_symbol()   # sym = "DTYPE" missing "is"
    pointer_msg = scanner_example_3.get_pointer(sym, front=True)
    assert pointer_msg == "D2 DTYPE;" + '\n' + "  ^"


def test_get_pointer_start(scanner_example_3):
    """Test if get_pointer(start_of_sen=True) return a correct pointer.

    The pointer message returned should be the whole line where
    the symbol is located, with the pointer points to the start
    of the whole sentence.
    """
    scanner_example_3.get_symbol()
    scanner_example_3.get_symbol()
    sym = scanner_example_3.get_symbol()
    pointer_msg = scanner_example_3.get_pointer(sym, start_of_sen=True)
    assert pointer_msg == "INIT; d1 is DTYPE;" + '\n' + "^"


def test_get_pointer_behind(scanner_example_3):
    """Test if get_pointer(behind=True) return a correct pointer.

    The pointer message returned should be the whole line where
    the symbol is located, with the pointer points to the symbol
    before.
    """
    scanner_example_3.get_symbol()
    sym = scanner_example_3.get_symbol()    # sym is semicolon
    pointer_msg = scanner_example_3.get_pointer(sym, behind=True)
    # pointer points to INIT
    assert pointer_msg == "INIT; d1 is DTYPE;" + '\n' + "   ^"


def test_print_error_message(scanner_example_3):
    """Test if print_error_message return a correct message.

    The error message returned should include the line number,
    the line sentence, the pointer points to correct position,
    and a specific error sentence.
    """
    scanner_example_3.get_symbol()
    scanner_example_3.get_symbol()
    sym = scanner_example_3.get_symbol()
    error_type = scanner_example_3.error.SYNTAX
    error = scanner_example_3.error
    error.error_code = error.INIT_WRONG_NAME
    msg = scanner_example_3.print_error_message(sym, error_type)

    assert msg == ("Error in line: 1"
                    + '\n' + "INIT; d1 is DTYPE;"
                    + '\n' + "       ^" + '\n'
                    + "SYNTAX[Invalid Initialisation]: Invalid device name ")
