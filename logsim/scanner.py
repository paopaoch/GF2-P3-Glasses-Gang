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
        self.pos = None
        self.line_pos = None


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
        self.last_line_pos = 0

    def read_file(self):
        return self.file.read(1)

    def restart(self):
        self.file.seek(0)

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
    
    def get_pointer(self, symbol, path, front=False):
        try:
            f = open(path, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()
        start_pos = f.seek(symbol.line_pos)
        sentence = f.read(symbol.pos-start_pos)
        sentence = sentence.strip()                     # Remove spaces before or after the sentence
        comment_regex = "\/\*.*?\*\/"
        sentence = ' '.join(sentence.split('\n'))       # Remove any newline within a sentence
        sentence = re.sub(comment_regex, '', sentence)  # Remove comments
        symbol_len = 1
        if not front or sentence[-1] == ";":            # Pointer points to the end of a symbol
            pointer = " " * (len(sentence) - 1) + '^'   # or semicolumn
            pointer_mes = sentence + '\n' + pointer
        else:                                           # Pointer points before the symbol
            for i in range(len(sentence)-1, 0, -1):     # or points to the first character
                if sentence[i] != ' ':                  # at the start of a sentence
                    symbol_len += 1
                else:
                    break
            pointer = " " * (len(sentence) - symbol_len) + '^'
            pointer_mes = sentence + '\n' + pointer
        return pointer_mes

    def get_line_position(self, symbol, path):
        try:
            f = open(path, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()
        line_number = 1
        cur_char = f.read(1)
        for i in range(symbol.pos-1):
            if cur_char == '\n':
                line_number += 1               # line number increases when find newline
            cur_char = f.read(1)
        return line_number
    
    def print_error_message(self, symbol, error, path, front=False):
        pointer_mes = self.get_pointer(symbol, path, front)
        line_number = self.get_line_position(symbol, path)
        error_mes = "Error in line: " + str(line_number)
        error_mes += '\n' + pointer_mes
        error_mes += '\n' + error.error_message()
        return error_mes

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        self.current_char = self.read_file()
        self.skip_spaces_and_linebreaks()
        symbol_get = Symbol()
        symbol_string = ""
        name_rule = re.compile("\A[A-Z]+\d+$")                              # Regex format for device name
        in_rule = re.compile("\A[A-Z]+\d+.((I\d+)|DATA|CLK|CLEAR|SET)$")    # Regex format for device input
        out_rule = re.compile("\A[A-Z]+\d+(.(Q|QBAR))?$")                   # Regex format for device output
        if self.current_char == '':
            symbol_get.type = self.EOF
            symbol_get.pos = self.file.tell()
            symbol_get.line_pos = self.last_line_pos
            return symbol_get
        if self.current_char == ';':
            symbol_get.type = self.SEMICOLON
            symbol_get.pos = self.file.tell()
            symbol_get.line_pos = self.last_line_pos
            self.last_line_pos = self.file.tell()
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
                self.file.seek(self.file.tell())
                break
            elif self.current_char == '/':
                self.current_char = self.read_file()
                if self.current_char == '*':
                    self.skip_comment()
                    if self.current_char == '':
                        symbol_get.type = self.EOF
                        symbol_get.pos = self.file.tell()
                        symbol_get.line_pos = self.last_line_pos
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
            [symbol_get.id] = self.names.lookup([symbol_string])          
        elif in_rule.match(symbol_string):
            symbol_get.type = self.DEVICE_IN
            [symbol_get.id] = self.names.lookup([symbol_string])   
        elif symbol_string in self.device_type_list:
            symbol_get.type = self.DEVICE_TYPE
            [symbol_get.id] = self.names.lookup([symbol_string])  
        elif out_rule.match(symbol_string):
            symbol_get.type = self.DEVICE_OUT
            [symbol_get.id] = self.names.lookup([symbol_string])
        else:
            symbol_get.type = self.ERROR

        symbol_get.pos = self.file.tell()
        symbol_get.line_pos = self.last_line_pos
        return symbol_get
        