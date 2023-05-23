"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

from names import Names
from network import Network
from devices import Devices
from monitors import Monitors
from scanner import symbol, Scanner

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
        self.phase = 0
        self.symbol = None

    def go_to_next_sentece(self):
        while self.symbol.type != self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol(self)

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        return True
        expect_type = self.scanner.INIT  # tells you whehter the current char should be a ;
        new_line = True  # Tells you if the current symbol is a start of a new line
        self.symbol = self.scanner.get_symbol(self)
        sentence_type = None

        if self.symbol.type != expect_type:  # Check for INIT
            print("SYNTAX[Incomplete File]: Missing start mark")
        self.phase = 1
        expect_type = self.scanner.SEMICOLON
        new_line = False
            

        while self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol(self)
            
            if expect_type == self.scanner.SEMICOLON and self.symbol.type != self.SEMICOLON:
                print("SYNTAX[No Termination]: Missing termination mark")
            else:
                expect_type = None
                new_line = True
                pass

            if self.phase == 1:
                if new_line and self.symbol.type == self.CONNECT:  # Check for CONNECT
                    self.phase = 2
                    expect_type = self.scanner.SEMICOLON
                    pass
                elif new_line:
                    if self.symbol.type != self.DEVICE_NAME:
                        print("SYNTAX[Invalid Monitor]: Missing keywords")
                        new_line = True
                        expect_type = self.DEVICE_NAME
                        self.go_to_next_sentece()
                        pass
                    else:
                        expect_type = self.scanner.INIT_IS
                        new_line = False
                    
                elif not new_line:
                    if expect_type != self.symbol.type:
                        print("SYNTAX[Invalid Monitor]: Missing keywords")
                        self.go_to_next_sentece()
                        expect_type = self.DEVICE_NAME
                        new_line = True
                    elif self.symbol.type == self.scanner.INIT_IS:
                        expect_type = self.DEVICE_TYPE
                        pass
                    elif self.symbol.type == self.DEVICE_TYPE:
                        if self.names.get_name_string(self.symbol.id):
                            sentence_type = self.DEVICE_TYPE

                else:
                    pass


            # # Check for MONITOR
            # elif self.phase == 2 and self.symbol.type != self.CONNECT:
            #     print("SYNTAX[Incomplete File]: Missing start mark")
            #     self.phase = 3
            #     expect_semi_colon = True

            # elif expect_semi_colon and self.symbol.type != self.SEMICOLON:
            #     print("SYNTAX[No Termination]: Missing termination mark")
            else:
                expect_type = None
                new_line = True




