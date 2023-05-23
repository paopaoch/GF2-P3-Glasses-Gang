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

        self.new_line = True  # Tells you if the current symbol is a start of a new line
        self.expect_type = None
        self.sentence_type = None


    def go_to_next_sentece(self):
        while self.symbol.type != self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol(self)
        self.new_line = True

    

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        return True
        self.expect_type = self.scanner.INIT
        self.symbol = self.scanner.get_symbol(self)
        self.sentence_type = None
        self.phase = 1

        if self.symbol.type != self.expect_type:  # Check for INIT
            print("SYNTAX[Incomplete File]: Missing start mark")

        self.expect_type = self.scanner.SEMICOLON
        self.new_line = False
            

        while self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol(self)

            if self.symbol.type == self.scanner.ERROR:
                print("SYNTAX[Keyword Not Found]: Scanner can not process invalid keyword")
                self.go_to_next_sentece()
                continue

            if self.expect_type == self.scanner.SEMICOLON and self.symbol.type != self.SEMICOLON:
                print("SYNTAX[No Termination]: Missing termination mark")
                self.expect_type = self.scanner.DEVICE_NAME  # need to be dynamic for each type
                self.new_line = True
                # continue
            else:
                self.expect_type = self.scanner.DEVICE_NAME  # can be dynamic for each type
                self.new_line = True
                continue

            if self.phase == 1:
                if self.new_line and self.symbol.type == self.CONNECT:  # Check for CONNECT
                    self.phase = 2
                    self.expect_type = self.scanner.SEMICOLON
                    continue
                elif self.new_line:
                    if self.symbol.type != self.scanner.DEVICE_NAME:
                        print("SYNTAX[Invalid Initialisation]: Invalid device name")
                        self.expect_type = self.scanner.DEVICE_NAME
                        self.go_to_next_sentece()
                        continue

                    else:
                        self.expect_type = self.scanner.INIT_IS
                        self.new_line = False
                    
                elif not self.new_line:
                    if self.expect_type != self.symbol.type:
                        if self.expect_type == self.scanner.NUMBER:
                            print("SYNTAX[Invalid Initialisation]: Invalid setting")
                        else:
                            print("SYNTAX[Invalid Initialisation]: Missing keywords")
                        self.go_to_next_sentece()
                        self.expect_type = self.scanner.DEVICE_NAME
                        continue

                    elif self.symbol.type == self.scanner.INIT_IS:
                        self.expect_type = self.scanner.DEVICE_TYPE
                        continue

                    elif self.symbol.type == self.scanner.DEVICE_TYPE:
                        self.sentence_type = self.names.get_name_string(self.symbol.id)
                        if self.sentence_type == "XOR":
                            self.expect_type = self.scanner.SEMICOLON
                        elif self.sentence_type == "DTYPE":
                            self.expect_type = self.scanner.SEMICOLON
                        elif self.sentence_type == "SWITCH":
                            self.expect_type = self.scanner.INIT_SWITCH
                        elif self.sentence_type in {"NAND", "AND", "NOR", "OR"}:
                            self.expect_type = self.scanner.INIT_WITH
                        elif self.sentence_type == "CLOCK":
                            self.expect_type = self.scanner.INIT_CLK
                        continue

                    elif self.symbol.type == self.scanner.INIT_SWITCH:
                        self.expect_type = self.scanner.NUMBER
                    
                    elif self.symbol.type == self.scanner.INIT_WITH:
                        self.expect_type = self.scanner.NUMBER

                    elif self.symbol.type == self.scanner.INIT_CLK:
                        self.expect_type = self.scanner.scanner.NUMBER
                    
                    elif self.symbol.type == self.scanner.NUMBER:
                        if self.sentence_type == "SWITCH":
                            if self.names.get_name_string(self.symbol.id) not in {0,1}:
                                print("SYNTAX[Invalid Initialisation]: Invalid setting")
                            self.expect_type = self.scanner.SEMICOLON
                        elif self.sentence_type in {"NAND", "AND", "NOR", "OR"}:
                            self.expect_type = self.scanner.INIT_GATE
                        elif self.sentence_type == "CLOCK":
                            self.expect_type = self.scanner.SEMICOLON
                        continue
                    
                    elif self.symbol.type == self.scanner.INIT_GATE:
                        self.expect_type = self.scanner.SEMICOLON

                else:
                    print("UNKNOWN ERROR: Parser cannot parse. Please seek help. You need it")

            # # Check for MONITOR
            # elif self.phase == 2 and self.symbol.type != self.CONNECT:
            #     print("SYNTAX[Incomplete File]: Missing start mark")
            #     self.phase = 3
            #     expect_semi_colon = True

            # elif expect_semi_colon and self.symbol.type != self.SEMICOLON:
            #     print("SYNTAX[No Termination]: Missing termination mark")
            else:
                self.expect_type = None
                self.new_line = True




