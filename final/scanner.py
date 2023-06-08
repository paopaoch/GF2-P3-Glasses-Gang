"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser. Print error
messages and check for invalid comment error.

Classes
-------
Scanner - reads definition file and translates characters into symbols. Print
          error messages and check for invalid comments.
Symbol - encapsulates a symbol and stores its properties.
"""
import sys
import re
from error import Error


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
        # Position of the last char of the symbol
        self.pos = None
        # Position of the first char of the line that symbol is in
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
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    -------------
    read_file(self): Read file for the next character.

    restart(self): Restart reading the file from the beginning.

    get_name(self): Return the alphabetic string may with "_", update
                    the current character to the next non-alphabetic
                    character.

    get_number(self): Return the numerical string, update the current
                      character to the next non-numerical character.

    skip_spaces_and_linebreaks(self): Skip the spaces and linebreaks
                                      between symbols.

    skip_comment(self): Skip comments if comment is in valid form, or
                        report syntax error if invalid comment detected.

    get_pointer(self, symbol, front=False, start_of_sen=False, behind=False):
                        Return pointer message which includes the sentence
                        where the symbol located,and a pointer points to the
                        desired position.

    get_line_position(self, symbol): Return the line number of the
                                     symbol located in the file.

    print_error_message(self, symbol, pointer=True, front=False,
                        start_of_sen=False, behind=False, optional_mess=""):
                        Return the complete error message which includes the
                        line number, pointer message, and error message.

    get_symbol(self): Translates the next sequence of characters into a
                      symbol and returns the symbol.
    """

    def __init__(self, path, names, devices, network, monitors):
        """Open specified file and initialise reserved words and IDs."""
        # Open the file
        self.path = path
        try:
            self.file = open(path, "r")
        except IOError:
            print("Error: can\'t find file")
            print("Please check the file path and run again.")
            sys.exit()

        # Set Name instance
        self.names = names

        # Create Error instance
        self.error = Error(self.names, devices, network, monitors)

        # Assign symbol types
        self.symbol_type_list = [self.ERROR, self.INIT, self.CONNECT,
                                 self.MONITOR, self.DEVICE_TYPE,
                                 self.NUMBER, self.DEVICE_NAME,
                                 self.DEVICE_IN, self.DEVICE_OUT,
                                 self.INIT_IS, self.INIT_WITH,
                                 self.INIT_GATE, self.INIT_SWITCH,
                                 self.INIT_CLK, self.CONNECTION,
                                 self.INIT_MONITOR, self.SEMICOLON,
                                 self.SIGGEN_WAVE, self.EOF] = range(19)

        # Add keywords to names
        self.device_type_list = ['AND', 'NAND', 'OR', 'NOR', 'XOR',
                                 'SWITCH', 'DTYPE', 'CLOCK', 'RC', 'SIGGEN']

        self.names.lookup(self.device_type_list)

        # Character at current reading position
        self.current_char = None

        # Position of start char of the line is reading
        self.last_line_pos = 0

        # Whether comment error is raised
        self.invalid_comment = False

    def read_file(self):
        """Read file for the next character."""
        return self.file.read(1)

    def restart(self):
        """Go back to the start of the file."""
        self.file.seek(0)
        self.last_line_pos = 0

    def get_name(self):
        """Return alphabetic string may with '_', update current_char."""
        if not self.current_char.isalpha():
            raise TypeError("The current character should be Alphabet.")
        name = ""
        while self.current_char.isalnum() or self.current_char == '_':
            name += str(self.current_char)
            self.current_char = self.read_file()
        return name

    def get_number(self):
        """Return numerical string, update current_char."""
        if not self.current_char.isdigit():
            raise TypeError("The current character should be Digit.")
        number = ""
        while self.current_char.isdigit():
            number += str(self.current_char)
            self.current_char = self.read_file()
        return number

    def skip_spaces_and_linebreaks(self):
        """Skip spaces and linebreaks, update current_char."""
        while self.current_char.isspace() or self.current_char == '\n':
            if self.current_char == '\n':
                self.last_line_pos = self.file.tell()
            self.current_char = self.read_file()

    def skip_comment(self):
        """Skip comment if valid comment, otherwise report error."""
        if not self.current_char == '*':
            raise TypeError("The current character should be '*'.")
        sentence = "/*"
        self.current_char = self.read_file()
        sentence += self.current_char
        if self.current_char == '' and self.invalid_comment is False:
            self.error.error_code = self.error.INVALID_COMMENT
            sentence += '\n' + " " * len(sentence) + '^'
            print(sentence)
            print(self.error.error_message(self.error.SYNTAX))
            self.invalid_comment = True
            return

        end_left = self.current_char
        self.current_char = self.read_file()
        end_right = self.current_char
        sentence += self.current_char
        if self.current_char == '' and self.invalid_comment is False:
            self.error.error_code = self.error.INVALID_COMMENT
            sentence += '\n' + " " * len(sentence) + '^'
            print(sentence)
            print(self.error.error_message(self.error.SYNTAX))
            self.invalid_comment = True
            return

        while (not (end_left == '*' and end_right == '/')
                and (not self.current_char == '')):
            self.current_char = self.read_file()
            sentence += self.current_char
            end_left = end_right
            end_right = self.current_char
        if (not (end_left == '*' and end_right == '/')
                and self.invalid_comment is False):
            self.error.error_code = self.error.INVALID_COMMENT
            sentence = " ".join(sentence.split('\n'))
            sentence = sentence[:3] + " ... " + sentence[-3:]
            sentence += '\n' + " " * 11 + '^'
            print(sentence)
            print(self.error.error_message(self.error.SYNTAX))
            self.invalid_comment = True
        else:
            self.current_char = self.read_file()
        self.skip_spaces_and_linebreaks()

    def get_pointer(self, symbol, front=False, start_of_sen=False,
                    behind=False):
        """Return the pointer message.

        Pointer message includes the sentence where the symbol located,
        and a pointer points to the symbol, can eithrt point to the end
        of the symbol or front of the symbol or start of the line, or
        the symbol before.
        """
        try:
            f = open(self.path, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()

        # extract the line the symbol located
        f.seek(symbol.line_pos)
        sentence = ""
        symbol_pos = symbol.pos - symbol.line_pos
        space_len = 0
        last_space_len = 0
        cur_char = f.read(1)
        while cur_char != '\n':
            sentence += cur_char
            if cur_char == " ":
                space_len += 1
            else:
                last_space_len = space_len
                space_len = 0
            cur_char = f.read(1)
            if cur_char == '':
                break
        # Create the pointer message
        if start_of_sen or sentence == '':
            pointer_mes = sentence + '\n' + '^'
            return pointer_mes

        if not front or symbol.type == self.SEMICOLON:
            pointer = " " * (symbol_pos - 1) + '^'
            if behind and len(pointer) > 1:
                pointer = pointer[last_space_len+1:]
            pointer_mes = sentence + '\n' + pointer
        else:
            symbol_len = 0
            f.seek(symbol.line_pos)
            strings = f.read(symbol_pos)
            symbol_len = len(strings.split(' ')[-1])
            if symbol_pos - symbol_len >= 1:
                pointer = " " * (symbol_pos - symbol_len - 1) + '^'
            else:
                pointer = " " * (symbol_pos - symbol_len) + '^'
            if behind and len(pointer) > 1:
                pointer = pointer[last_space_len+1:]
            pointer_mes = sentence + '\n' + pointer
        return pointer_mes

    def get_line_position(self, symbol):
        """Return the line number of the symbol located in the file."""
        try:
            f = open(self.path, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()
        line_number = 1
        cur_char = f.read(1)
        for i in range(symbol.pos-1):
            # line number increases when find newline
            if cur_char == '\n':
                line_number += 1
            cur_char = f.read(1)
        return line_number

    def print_error_message(self, symbol, error_type, front=False,
                            start_of_sen=False, behind=False,
                            optional_mess=""):
        """Return the complete error message.

        Complete error message includes the line number,
        pointer message, and error message.
        """
        line_number = self.get_line_position(symbol)
        error_mes = "Error in line: " + str(line_number)
        if not start_of_sen:
            pointer_mes = self.get_pointer(symbol, front, start_of_sen, behind)
            error_mes += '\n' + pointer_mes
            error_mes += '\n' + self.error.error_message(error_type,
                                                         optional_mess)
        else:
            pointer_mes = self.get_pointer(symbol, front, start_of_sen, behind)
            # error_mes = self.error.error_message(error_type, optional_mess)
            error_mes += '\n' + pointer_mes
            error_mes += '\n' + self.error.error_message(error_type,
                                                         optional_mess)
        return error_mes

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        self.current_char = self.read_file()
        self.skip_spaces_and_linebreaks()
        symbol_get = Symbol()
        symbol_string = ""
        # Regex format for device name
        name_rule = re.compile(r'\A[A-Z]+\d+$')
        # Regex format for device input
        in_rule = re.compile(r'\A[A-Z]+\d+.((I\d+)|DATA|CLK|CLEAR|SET)$')
        # Regex format for device output
        out_rule = re.compile(r'\A[A-Z]+\d+(.(Q|QBAR))?$')
        # Regex format for siggen waveform
        siggen_rule = re.compile(r'\A"[01]+"$')

        if self.current_char == '':
            symbol_get.type = self.EOF
            symbol_get.pos = self.file.tell()
            symbol_get.line_pos = self.last_line_pos
            return symbol_get
        if self.current_char == ';':
            symbol_get.type = self.SEMICOLON
            symbol_get.pos = self.file.tell()
            symbol_get.line_pos = self.last_line_pos
            return symbol_get

        while not (self.current_char.isspace() or self.current_char == '\n'):
            # read alphabets
            if self.current_char.isalpha():
                alphabets = self.get_name()
                symbol_string += alphabets
            # read numbers
            elif self.current_char.isdigit():
                num = self.get_number()
                symbol_string += num
            # read SIGGEN waveform
            elif self.current_char == "\"":
                symbol_string += "\""
                self.current_char = self.read_file()
            # read termination
            elif self.current_char == ';':
                symbol_get.pos = self.file.tell() - 1
                self.file.seek(self.file.tell() - 1)
                break
            # read EOF
            elif self.current_char == '':
                symbol_get.pos = self.file.tell()
                self.file.seek(self.file.tell())
                break
            # read comments
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
        # set symbol type and id
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
        elif symbol_string == "connect_to":
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
        elif siggen_rule.match(symbol_string):
            symbol_get.type = self.SIGGEN_WAVE
            # store the siggen waveform without quotation marks
            [symbol_get.id] = self.names.lookup([symbol_string[1:-1]])
        else:
            symbol_get.type = self.ERROR
        if symbol_get.pos is None:
            symbol_get.pos = self.file.tell() - 1
        symbol_get.line_pos = self.last_line_pos
        if self.current_char == '\n':
            self.last_line_pos = self.file.tell()
        return symbol_get
