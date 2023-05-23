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

        self.phase = None  # Tells you which phase of parsing its in
        self.current_symbol = None
        self.previous_symbol = None


    @staticmethod
    def check_sentence(sentence: str):
        """Primary check if there is a syntax error using regex
        Returns False and the sentence type if the sentence does 
        not have any syntax errors. True otherwise with None 
        as sentence type."""
        sentence_type = "init device"
        return False, sentence_type


    def classify_syntax_error(self, sentence: str):
        """Check for the first syntax error in the sentence"""
        pass
        # 
        # return self.error_type


    def update_symbol(self):
        self.previous_symbol = self.current_symbol
        self.current_symbol = self.scanner.get_symbol()

    def go_to_next_sentence(self):
        while self.current_symbol != self.scanner.SEMICOLON:
            self.update_symbol(self)


    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        return True

        oututs = {}
        inputs = {}
        connections = {}


        self.update_symbol()

        if self.phase == None:
            if self.current_symbol.type == self.scanner.INIT:
                self.phase = 1
            else:
                raise SyntaxError("SYNTAX[Incomplete File]: Missing start mark") # Will have to change this
        
        self.update_symbol()
        if self.current_symbol.type != self.scanner.SEMICOLON:
            raise SyntaxError("SYNTAX[No Termination]: Missing termination mark")
        
        while self.phase == 1:
            self.update_symbol()

            # Deal with syntax error
            if self.previous_symbol.type == self.scanner.SEMICOLON:
                current_sentence = " ".join(self.scanner.get_sentence())
                syntax_error, sentence_type = self.check_sentence(current_sentence)
                if  syntax_error:
                    error = self.classify_syntax_error(current_sentence)
                    self.go_to_next_sentence()
                    continue
                    raise SyntaxError(error)

            # Everything into hashes. Hashes are great.
            if sentence_type == "init device":
                if self.current_symbol.type == self.scanner.DEVICE_NAME:
                    if self.current_symbol not in oututs:
                        oututs.add(self.current_symbol)

                if self.current_symbol.type == self.scanner.DEVICE_TYPE:
                    device = self.current_symbol

                if self.current_symbol.type == self.scanner.NUMBER:
                    if self.current_symbol > 3:
                        pass

        return True
