"""Test the scanner module."""
import pytest

from names import Names
from devices import Devices
from network import Network
from scanner import Scanner, Symbol

@pytest.fixture
def new_scanner():
    """Return a new instance of the Scanner class."""
    new_names = Names()
    new_devices = Devices(new_names)
    new_network = Network(new_names, new_devices)
    filename = 'test_scanner.txt'
    return Scanner(filename, new_names, new_devices, new_network)

def test_get_symbol(new_scanner):
    """Test if get_symbol() return a correct Symbol type."""
    sym = new_scanner.get_symbol() # sym is device type "AND"
    assert sym.type == new_scanner.DEVICE_TYPE
    assert new_scanner.names.get_name_string(sym.id) == "AND"
    assert sym.pos == 3            # position of last character
    assert sym.line_pos == 0       # position of start of a sentence
    new_scanner.get_symbol()
    sym = new_scanner.get_symbol() # sym is device input "G123.I7"
    assert sym.type == new_scanner.DEVICE_IN
    assert new_scanner.names.get_name_string(sym.id) == "G123.I7"
    assert sym.pos == 11
    assert sym.line_pos == 4

