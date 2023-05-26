from names import Names
from network import Network
from devices import Devices
from monitors import Monitors
from scanner import Symbol, Scanner

class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names: Names, devices: Devices, 
                network: Network, monitors: Monitors, 
                scanner: Scanner):

        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

    def parse_network(self):
        [SW1_ID, CK1_ID, OR1_ID, DT1_ID, I1, I2,] = self.names.lookup(["SW1", "CK2", "OR1", "DT1", "I1",
                                                     "I2"])
        
        # Make dem devices
        OR_error = self.devices.make_device(OR1_ID, self.devices.OR, 2)
        SW1_error = self.devices.make_device(SW1_ID, self.devices.SWITCH, 0)
        CK1_error = self.devices.make_device(CK1_ID, self.devices.CLOCK, 20)

        print(OR_error, SW1_error, CK1_error)

        # Get devices
        OR1 = self.devices.get_device(OR1_ID)
        SW1 = self.devices.get_device(SW1_ID)
        CK2 = self.devices.get_device(CK1_ID)

        # Make connections
        self.network.make_connection(SW1_ID, None, OR1_ID, I2)
        self.network.make_connection(CK1_ID, None, OR1_ID, I1)
        # self.network.make_connection(CK1_ID, None, OR1_ID, I2)

        return True


if __name__ == "__main__":
    names = Names()
    devices = Devices(names)
    scanner = None
    network = Network(names, devices)
    monitors = None

    test_parser = Parser(names, devices, network, monitors, scanner)

    test_parser.parse_network()


