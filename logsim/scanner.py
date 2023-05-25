"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
import sys
import re


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_name(self):
    get_nuber(self):
    skip_spaces_and_linebreaks(self):
    skip_comment(self):
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        try:
            self.file = open(path, "r")

        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()
        
        self.names = names

        self.symbol_type_list = [self.ERROR, self.INIT, self.CONNECT, 
                                 self.MONITOR, self.DEVICE_TYPE, 
                                 self.NUMBER, self.DEVICE_NAME, 
                                 self.DEVICE_IN, self.DEVICE_OUT, 
                                 self.INIT_IS, self.INIT_WITH, 
                                 self.INIT_GATE, self.INIT_SWITCH, 
                                 self.INIT_CLK, self.CONNECTION, 
                                 self.INIT_MONITOR, self.SEMICOLON, 
                                 self.EOF] = range(18)
        self.device_type_list = ['AND', 'NAND', 'OR', 'NOR', 'XOR', 
                                 'SWITCH', 'DTYPE', 'CLOCK']
        self.device_input_pin_list = ['I1', 'I2', 'I3', 'I4', 'I5', 
                                      'I6', 'I7', 'I8', 'I9', 'I10', 
                                      'I11', 'I12', 'I13', 'I14', 'I15', 
                                      'I16', 'DATA', 'CLK', 'SET', 'CLEAR']
        self.device_output_pin_list = ['Q', 'QBAR']
        self.names.lookup(self.device_type_list)
        self.names.lookup(self.device_input_pin_list)
        self.names.lookup(self.device_output_pin_list)

        self.current_char = None

    def read_file(self):
        return self.file.read(1)

    def get_name(self):
        if not self.current_char.isalpha():
            raise TypeError("The current character should be Alphabet.")
        name = ""
        while self.current_char.isalnum() or self.current_char == '_':
            name += str(self.current_char)
            self.current_char = self.read_file()
        return name

    def get_number(self):
        if not self.current_char.isdigit():
            raise TypeError("The current character should be Digit.")
        number = ""
        while self.current_char.isdigit():
            number += str(self.current_char)
            self.current_char = self.read_file()
        return number

    def skip_spaces_and_linebreaks(self):
        while self.current_char.isspace() or self.current_char == '\n':
            self.current_char = self.read_file()
    
    def skip_comment(self):
        if not self.current_char == '*':
            raise TypeError("The current character should be '*'.")
        self.current_char = self.read_file()
        if self.current_char == '':
            print("Invalid comment")
            return
        
        end_left = self.current_char
        self.current_char = self.read_file()
        end_right = self.current_char
        if self.current_char == '':
            print("Invalid comment")
            return
        
        while (not (end_left == '*' and end_right == '/')
                and (not self.current_char == '')):
            self.current_char = self.read_file()
            end_left = end_right
            end_right = self.current_char
        if not (end_left == '*' and end_right == '/'):
            print("Invalid comment")
        else:
            self.current_char = self.read_file()
        self.skip_spaces_and_linebreaks()
    
    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        self.current_char = self.read_file()
        self.skip_spaces_and_linebreaks()
        symbol_get = Symbol()
        symbol_string = ""
        name_rule = re.compile("\A[A-Z]+\d+$")
        in_rule = re.compile("\A[A-Z]+\d+.((I\d+)|DATA|CLK|CLEAR|SET)$")

        if self.current_char == '':
            symbol_get.type = self.EOF
            return symbol_get
        if self.current_char == ';':
            symbol_get.type = self.SEMICOLON
            return symbol_get

        while not (self.current_char.isspace() or self.current_char == '\n'):
            if self.current_char.isalpha():
                alphabets = self.get_name()
                symbol_string += alphabets
            elif self.current_char.isdigit():
                num = self.get_number()
                symbol_string += num
            elif self.current_char == ';':
                self.file.seek(self.file.tell() - 1)
                break
            elif self.current_char == '':
                self.file.seek(self.file.tell() - 1)
                break
            elif self.current_char == '/':
                self.current_char = self.read_file()
                if self.current_char == '*':
                    self.skip_comment()
                    if self.current_char == '':
                        symbol_get.type = self.EOF
                        return symbol_get
                else:
                    symbol_string += "/"
                    symbol_string += str(self.current_char)
                    self.current_char = self.read_file()
            else:
                symbol_string += str(self.current_char)
                self.current_char = self.read_file()

        if symbol_string == "INIT":
            symbol_get.type = self.INIT
        elif symbol_string == "CONNECT":
            symbol_get.type = self.CONNECT
        elif symbol_string == "MONITOR":
            symbol_get.type = self.MONITOR
        elif symbol_string == "is":
            symbol_get.type = self.INIT_IS
        elif symbol_string == "with":
            symbol_get.type = self.INIT_WITH
        elif symbol_string == "inputs" or symbol_string == "input":
            symbol_get.type = self.INIT_GATE
        elif symbol_string == "initially_at":
            symbol_get.type = self.INIT_SWITCH
        elif symbol_string == "with_simulation_cycles":
            symbol_get.type = self.INIT_CLK
        elif symbol_string == "is_connected_to":
            symbol_get.type = self.CONNECTION
        elif symbol_string == "Initial_monitor_at":
            symbol_get.type = self.INIT_MONITOR
        elif name_rule.match(symbol_string):
            symbol_get.type = self.DEVICE_NAME
            [symbol_get.id] = self.names.lookup([symbol_string])  
        elif symbol_string.isdigit():
            symbol_get.type = self.NUMBER            
        elif in_rule.match(symbol_string):
            symbol_get.type = self.DEVICE_IN
            [symbol_get.id] = self.names.lookup([symbol_string])   
        elif symbol_string in self.device_type_list:
            symbol_get.type = self.DEVICE_TYPE
            [symbol_get.id] = self.names.lookup([symbol_string])  
        elif symbol_string in self.device_output_pin_list:
            symbol_get.type = self.DEVICE_OUT
            [symbol_get.id] = self.names.lookup([symbol_string])
        else:
            symbol_get.type = self.ERROR

        return symbol_get
        
