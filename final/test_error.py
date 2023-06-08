"""Test the error module."""
import pytest

from names import Names
from devices import Devices
from network import Network
from error import Error


@pytest.fixture
def new_error():
    """Return a new instance of the Error class."""
    new_names = Names()
    new_devices = Devices(new_names)
    new_network = Network(new_names, new_devices)
    return Error(new_names, new_devices, new_network)


def test_syntax_error_message(new_error):
    """Test if the error message is correctly selected."""
    # set error_code to MISS_START_MARK
    new_error.error_code = new_error.MISS_START_MARK
    # set error_type to SYNTAX
    error_type = new_error.SYNTAX
    errormsg = new_error.error_message(error_type)
    assert errormsg == "SYNTAX[Incomplete File]: Missing start mark "


def test_device_semantic_error_message(new_error):
    """Test if the error message is correctly selected."""
    # set error_code to BAD_DEVICE
    new_error.error_code = new_error.devices.BAD_DEVICE
    # set error_type to SEMANTIC
    error_type = new_error.SEMANTIC
    errormsg = new_error.error_message(error_type)
    assert errormsg == "SEMANTIC[INIT]: Bad device "


def test_network_semantic_error_message(new_error):
    """Test if the error message is correctly selected."""
    # set error_code to OUTPUT_TO_OUTPUT
    new_error.error_code = new_error.network.OUTPUT_TO_OUTPUT
    # set error_type to SEMANTIC
    error_type = new_error.SEMANTIC
    errormsg = new_error.error_message(error_type)
    assert errormsg == "SEMANTIC[CONNECT]: Output is connected to an output "


def test_add_syntax_error(new_error):
    """Test if the syntax error counter works"""
    error_type = new_error.SYNTAX
    new_error.error_code = new_error.MISS_START_MARK
    new_error.add_error(error_type)
    new_error.error_code = new_error.MISS_DESCRIPTION
    new_error.add_error(error_type)
    assert new_error.syntax_error_count == 2


def test_add_semantic_error(new_error):
    """Test if the semantic error counter works"""
    error_type = new_error.SEMANTIC
    new_error.error_code = new_error.devices.NO_QUALIFIER
    new_error.add_error(error_type)
    new_error.error_code = new_error.network.INPUT_TO_INPUT
    new_error.add_error(error_type)
    assert new_error.semantic_error_count == 2
