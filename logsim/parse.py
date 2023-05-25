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
        self.phase = 0
        self.symbol = None

        self.new_line = True  # Tells you if the current symbol is a start of a new line
        self.expect_type = None
        self.sentence_type = None


    def go_to_next_sentece(self):
        while self.symbol.type != self.scanner.SEMICOLON:
            self.count += 1
            self.symbol = self.scanner.get_symbol()
        self.new_line = True

    

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        # return True
        self.expect_type = self.scanner.INIT
        self.symbol = self.scanner.get_symbol()
        self.sentence_type = None
        self.phase = 1
        self.device_name = False

        if self.symbol.type != self.expect_type:  # Check for INIT
            print("SYNTAX[Incomplete File]: Missing start mark")

        self.expect_type = self.scanner.SEMICOLON
        self.new_line = False
            
        self.count = 0
        while self.symbol.type != self.scanner.EOF:
            self.count += 1
            self.symbol = self.scanner.get_symbol()
            print(self.count)
            if self.symbol.type == self.scanner.ERROR:
                print("SYNTAX[Keyword Not Found]: Scanner can not process invalid keyword")
                self.go_to_next_sentece()
                continue

            if self.expect_type == self.scanner.SEMICOLON:
                if self.symbol.type != self.scanner.SEMICOLON:
                    print("SYNTAX[No Termination]: Missing termination mark")
                if self.phase == 1:
                    self.expect_type = self.scanner.DEVICE_NAME
                elif self.phase == 2:
                    self.expect_type = self.scanner.DEVICE_OUT
                else:
                    self.expect_type = self.scanner.INIT_MONITOR
                self.new_line = True
                continue

            if self.expect_type != self.symbol.type:
                if self.phase == 1:
                    if self.expect_type == self.scanner.NUMBER:
                        print("SYNTAX[Invalid Initialisation]: Invalid setting")
                    else:
                        print("SYNTAX[Invalid Initialisation]: Missing keywords")
                elif self.phase == 2:
                    if self.expect_type == self.scanner.DEVICE_OUT:
                        if self.symbol.type != self.scanner.DEVICE_NAME:
                            print("SYNTAX[Invalid Connection]: Missing keywords")
                        else:
                            device_name = True
                else:
                    if self.expect_type == self.scanner.DEVICE_OUT:
                        if self.symbol.type != self.scanner.DEVICE_NAME:
                            print("SYNTAX[Invalid Monitor]: Invalid monitor point")
                        else:
                            device_name = True
                    else:
                        print("SYNTAX[Invalid Monitor]: Missing keywords")
                if not device_name:
                    self.go_to_next_sentece()
                    if self.phase == 1:
                        self.expect_type = self.scanner.DEVICE_NAME
                    elif self.phase == 2:
                        self.expect_type = self.scanner.DEVICE_OUT
                    else:
                        self.expect_type = self.scanner.DEVICE_OUT
                    device_name = False
                    continue
                
            # Check INIT
            if self.phase == 1:
                if self.new_line and self.symbol.type == self.scanner.CONNECT:  # Check for CONNECT
                    self.phase = 2
                    self.expect_type = self.scanner.SEMICOLON
                    self.new_line = False
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
  
                else:
                    if self.symbol.type == self.scanner.INIT_IS:
                        self.expect_type = self.scanner.DEVICE_TYPE

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

                    elif self.symbol.type == self.scanner.INIT_SWITCH:
                        self.expect_type = self.scanner.NUMBER
                    
                    elif self.symbol.type == self.scanner.INIT_WITH:
                        self.expect_type = self.scanner.NUMBER

                    elif self.symbol.type == self.scanner.INIT_CLK:
                        self.expect_type = self.scanner.NUMBER
                    
                    elif self.symbol.type == self.scanner.NUMBER:
                        if self.sentence_type == "SWITCH":
                            if self.names.get_name_string(self.symbol.id) not in {0,1}:
                                print("SYNTAX[Invalid Initialisation]: Invalid setting")
                            self.expect_type = self.scanner.SEMICOLON
                        elif self.sentence_type in {"NAND", "AND", "NOR", "OR"}:
                            self.expect_type = self.scanner.INIT_GATE
                        elif self.sentence_type == "CLOCK":
                            self.expect_type = self.scanner.SEMICOLON
                    elif self.symbol.type == self.scanner.INIT_GATE:
                        self.expect_type = self.scanner.SEMICOLON
                
            # Check for CONNECT
            elif self.phase == 2:
                if self.new_line and self.symbol.type == self.scanner.MONITOR:  # Check for CONNECT
                    self.phase = 3
                    self.expect_type = self.scanner.SEMICOLON
                    self.new_line = False
                    continue

                elif self.new_line:
                    if (self.symbol.type != self.scanner.DEVICE_NAME 
                        and self.symbol.type != self.scanner.DEVICE_OUT):
                        print("SYNTAX[Invalid Connection]: Invalid device I/O")
                        self.expect_type = self.scanner.DEVICE_NAME
                        self.go_to_next_sentece()
                        continue
                    else:
                        self.expect_type = self.scanner.CONNECTION
                        self.new_line = False
                        
                else:
                    if self.symbol.type == self.scanner.CONNECTION:
                        self.expect_type = self.scanner.DEVICE_IN
                    if self.symbol.type == self.scanner.DEVICE_IN:
                        self.expect_type = self.scanner.SEMICOLON

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
        

if __name__ == "__main__":
    names = Names()
    scanner = Scanner('logsim/parser_connection_test_file.txt', names)
    network = None
    monitors = None
    devices = None

    test_parser = Parser(names, devices, network, monitors, scanner)

    test_parser.parse_network()


