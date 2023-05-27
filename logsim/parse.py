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

    def set_new_line_word(self):
        if self.phase == 1:
            self.expect_type = self.scanner.DEVICE_NAME
        elif self.phase == 2:
            self.expect_type = self.scanner.DEVICE_OUT
        elif self.phase == 3:
            self.expect_type = self.scanner.INIT_MONITOR
        else:
            raise ValueError("Phase can only be 1, 2, or 3")
        self.new_line = True

    def go_to_next_sentece(self):
        while (self.symbol.type != self.scanner.SEMICOLON
               and self.symbol.type != self.scanner.EOF):
            self.symbol = self.scanner.get_symbol()
            print(self.count)
            self.count += 1
        self.set_new_line_word()
        # print("Found new sentence")

    def increment_phase(self):
        self.phase += 1
        self.new_line = False
        self.expect_type = self.scanner.SEMICOLON


    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        # return True
        self.count = 0
        self.expect_type = self.scanner.INIT
        self.symbol = self.scanner.get_symbol()
        self.count += 1
        self.sentence_type = None
        self.phase = 1
        self.device_name = False

        if self.symbol.type != self.expect_type:  # Check for INIT
            print("SYNTAX[Incomplete File]: Missing start mark")

        self.expect_type = self.scanner.SEMICOLON
        self.new_line = False

        while self.symbol.type != self.scanner.EOF:
            print(self.symbol.type, self.scanner.EOF)
            print(self.scanner.DEVICE_NAME)
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.EOF:
                break
            # print(self.count)
            self.count += 1
            if self.symbol.type == self.scanner.ERROR:
                # print(self.symbol.id)
                print("SYNTAX[Keyword Not Found]: Scanner can not process invalid keyword")
                # print("Next sentence, wrong keyword")
                self.go_to_next_sentece()
                continue

            if self.expect_type == self.scanner.SEMICOLON:
                if self.symbol.type != self.scanner.SEMICOLON:
                    print("SYNTAX[No Termination]: Missing termination mark")
                self.set_new_line_word()
                self.new_line = True
                continue

            if self.expect_type != self.symbol.type:
                if self.new_line and self.phase != 3:
                    if self.phase == 1:
                        if self.symbol.type == self.scanner.CONNECT:
                            print("DONE WITH INIT")
                            self.increment_phase()
                            continue
                        elif self.expect_type == self.scanner.NUMBER:
                            print("SYNTAX[Invalid Initialisation]: Invalid setting should init with numbers")
                            self.go_to_next_sentece()
                            continue
                        else:
                            print("SYNTAX[Invalid Initialisation]: Missing keywords")
                            self.go_to_next_sentece()
                            continue
                    if self.phase == 2:
                        if self.symbol.type == self.scanner.MONITOR:
                            print("DONE WITH CONNECT")
                            self.increment_phase()
                            continue
                    
                        if self.expect_type == self.scanner.DEVICE_OUT:
                            if self.symbol.type != self.scanner.DEVICE_NAME:
                                print("SYNTAX[Invalid Connection]: Missing keywords expected a device output")
                                self.go_to_next_sentece()
                                continue
                        else:
                            print("SYNTAX[Invalid Connection]: Missing keywords")
                            self.go_to_next_sentece()
                            continue
                else:
                    if self.phase == 3:
                        if self.expect_type == self.scanner.DEVICE_OUT:
                            if self.symbol.type == self.scanner.SEMICOLON:
                                self.expect_type = self.scanner.DEVICE_OUT
                                continue
                            if self.symbol.type == self.scanner.EOF:
                                print("SYNTAX[No Termination]: Missing termination mark")
                                self.expect_type = self.scanner.EOF
                                break
                            elif self.symbol.type != self.scanner.DEVICE_NAME:
                                print(self.expect_type)
                                print(self.scanner.DEVICE_OUT)
                                print("SYNTAX[Invalid Monitor]: Missing keywords expected a device output")
                                continue
                    else:
                        print("SYNTAX[Invalid Keyword]: Unexpected keyword found")
                        print("expected", self.names.get_name_string(self.symbol.id))
                        print("got", self.symbol.type)
                        self.go_to_next_sentece()
                        continue

            # Check INIT
            if self.phase == 1:
                if self.new_line:
                    if self.symbol.type != self.scanner.DEVICE_NAME:
                        print("SYNTAX[Invalid Initialisation]: Invalid device name")
                        self.expect_type = self.scanner.DEVICE_NAME
                        # print("Next sentence new line expect device name")
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
                        # print("device", self.names.get_name_string(self.symbol.id))
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
                            if self.names.get_name_string(self.symbol.id) not in {'0','1'}:
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
                if self.new_line:
                    if (self.symbol.type != self.scanner.DEVICE_NAME 
                        and self.symbol.type != self.scanner.DEVICE_OUT):
                        print("SYNTAX[Invalid Connection]: Invalid device I/O")
                        self.expect_type = self.scanner.DEVICE_NAME
                        # print("Next sentence new line expect device name")
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

            elif self.phase == 3:
                if self.symbol.type == self.scanner.INIT_MONITOR:
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.new_line = False

        return True


if __name__ == "__main__":
    names = Names()
    scanner = Scanner('parser_test_file.txt', names)
    network = None
    monitors = None
    devices = None

    test_parser = Parser(names, devices, network, monitors, scanner)

    test_parser.parse_network()


