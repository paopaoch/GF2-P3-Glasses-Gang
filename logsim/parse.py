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
    parse_network(self):    Parses the circuit definition file.

                            return True if network was connected
                            correctly
    
    Private methods
    ---------------
    go_to_next_sentece():   Get new symbols until a end of 
                            symbol or end of file is reached
                            
                            return current symbol type should
                            be EOF or semicolon

    check_structure():      Check if for structural errors in the 
                            files. this includes missing start mark 
                            eg. CONNECT and missing sentences in 
                            phases
                            
                            return True if no errors, False otherwise
    
    parse_semicolon():      contains the logic to deal with parsing
                            when we expect a semicolon. This includes
                            device connection or initialisation

                            return error code if there is an error
                            otherwise return None
    
    handle_unexpected_keyword():
                            Handle cases when the symbols type are not
                            the expected type. This could be an eror or
                            not an error eg. if it found a start mark at
                            start of a sentence then its not an error.

                            return (boolean, boolean) where the first one
                            tells the main code whether to continue and
                            the second one tells you whther to break.

    parse_init():           Handle initialise sentence logic and stores
                            device info in placeholder accordingly
                            return error code if error found otherwise
                            return None

    parse_connect():        Handle connection setence logic
                            return error code if error found otherwise
                            return None

    parse_monitor():        Handle monitor sentence logic
                            return error code if error found otherwise
                            return None

    Void methods
    ------------
    set_new_line_word():    Set the expected type of symbol of a 
                            new line depending on the phase
    
    increment_phase():      Increment phase and set new line and 
                            expected symbol type accordingly
    
    handle_error():         Function to show the error

    restart_and_get_symbol():  Take the cursor to the start of the
                               file and get the first symbol

    init_device_holder():   (STATIC) Initialise a device dectionary
                            to store current device info
                            and for making  device later
    
    init_connection_holder():   (STATIC) Initise a connection device
                                to store connection info and for
                                making connections later

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

        self.new_line = True
        self.expect_type = None
        self.sentence_type = None
        self.error_devices = []  # tracks any devices with errors
        self.current_device = None

    def set_new_line_word(self):
        """Set the expected type of symbol of a 
        new line depending on the phase"""
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
        """Get new symbols until a end of symbol or end of file is reached"""
        while (self.symbol.type != self.scanner.SEMICOLON
               and self.symbol.type != self.scanner.EOF):
            self.symbol = self.scanner.get_symbol()
        self.set_new_line_word()
        return self.symbol.type

    def increment_phase(self):
        """increment phase and set new line and expected
        symbol type accordingly"""
        self.phase += 1
        self.new_line = False
        self.expect_type = self.scanner.SEMICOLON

    def handle_error(self, error_code, error_type, 
                     front=False, start_of_sen=False):
        """Function to show the error"""
        self.scanner.error.error_code = error_code
        print(self.scanner.print_error_message(self.symbol, 
                                               error_type, 
                                               front=front, 
                                               start_of_sen=start_of_sen))

    def restart_and_get_symbol(self):
        """take the cursor to the start of the file
        and get the first symbol"""
        self.scanner.restart()
        self.symbol = self.scanner.get_symbol()

    def check_structure(self):
        """Check if for structural errors in the files.
        this includes missing start mark eg. CONNECT
        and missing sentences in phases"""
        self.symbol = self.scanner.get_symbol()
        self.expect_type = self.scanner.INIT
        self.phase = 1
        pos = 1
        init_pos = 0
        connect_pos = None
        monitor_pos = None
        error = False
        if self.symbol.type != self.expect_type:  # Check for INIT
            self.scanner.restart()
            error = True
        else:
            init_pos = 1

        # Loop through file for crude checking of file structure
        while self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()
            pos += 1
            if self.symbol.type == self.scanner.CONNECT:
                if self.phase == 1:
                    self.phase = 2
                    connect_pos = pos

            if self.symbol.type == self.scanner.MONITOR:
                if self.phase in [1,2]:
                    self.phase = 3
                    monitor_pos = pos

        if init_pos == 0:
            self.restart_and_get_symbol()
            self.handle_error(self.scanner.error.MISS_START_MARK,
                              self.scanner.error.SYNTAX, start_of_sen=True)
            error = True
        if connect_pos is None:
            self.restart_and_get_symbol()
            while (self.symbol.type != self.scanner.MONITOR 
                    and self.symbol.type != self.scanner.EOF):
                self.symbol = self.scanner.get_symbol()
            self.handle_error(self.scanner.error.MISS_START_MARK,
                              self.scanner.error.SYNTAX, front=True)
            error = True
        if monitor_pos is None:
            self.restart_and_get_symbol()
            while self.symbol.type != self.scanner.EOF:
                self.symbol = self.scanner.get_symbol()
            self.handle_error(self.scanner.error.MISS_START_MARK,
                              self.scanner.error.SYNTAX)
            error = True

        if connect_pos is not None:
            if connect_pos - init_pos < 3:
                self.restart_and_get_symbol()
                self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                  self.scanner.error.SYNTAX)
                error = True
        if connect_pos is not None and monitor_pos is not None:
            if monitor_pos - connect_pos < 3:
                self.restart_and_get_symbol()
                while self.symbol.type != self.scanner.CONNECT:
                    self.symbol = self.scanner.get_symbol()
                self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                  self.scanner.error.SYNTAX)
                error = True
        if monitor_pos is not None:
            if pos - monitor_pos < 3:
                self.restart_and_get_symbol()
                while self.symbol.type != self.scanner.MONITOR:
                    self.symbol = self.scanner.get_symbol()
                self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                  self.scanner.error.SYNTAX)
                error = True
        self.restart_and_get_symbol()
        if error:
            return False
        return True

    @staticmethod
    def init_device_holder():
        return {"device_id": None, 
                "device_kind": None, 
                "device_property": None}

    @staticmethod
    def init_connection_holder():
        return {"first_device_id": None,
                "first_port_id": None,
                "second_device_id": None,
                "second_port_id": None}
    
    def parse_semicolon(self):
        """Take care of parsing when we expect a semicolon"""
        err = None
        if self.symbol.type != self.scanner.SEMICOLON:
            self.handle_error(self.scanner.error.MISS_TERMINATION,
                                    self.scanner.error.SYNTAX,
                                    front=True)
            while self.symbol.type != self.scanner.SEMICOLON:
                self.symbol = self.scanner.get_symbol()
                if self.phase == 1:
                    if self.symbol.type == self.scanner.CONNECT:
                        self.increment_phase()
                        break
                elif self.phase == 2:
                    if self.symbol.type == self.scanner.MONITOR:
                        self.increment_phase()
                        break
                # self.symbol = self.scanner.get_symbol() # Dont think we need this
            self.go_to_next_sentece()
            return self.scanner.error.MISS_TERMINATION
        else:
            if self.phase == 1 and self.device_holder["device_id"] is not None:
                err = self.devices.make_device(self.device_holder["device_id"],
                                        self.device_holder["device_kind"],
                                        self.device_holder["device_property"])
                self.device_holder = self.init_device_holder()
                # print(err)
                if err != self.devices.NO_ERROR:
                    self.handle_error(err,
                                      self.scanner.error.SEMANTIC)

            elif (self.phase == 2 
                    and self.connection_holder["first_device_id"] is not None
                    and self.connection_holder["second_device_id"]):
                err = self.network.make_connection(
                    self.connection_holder["first_device_id"]
                    ,self.connection_holder["first_port_id"]
                    ,self.connection_holder["second_device_id"]
                    ,self.connection_holder["second_port_id"])
                self.connection_holder = self.init_connection_holder()
                # print(err)
                if err != self.network.NO_ERROR:
                    self.handle_error(err,
                                      self.scanner.error.SEMANTIC)
            self.set_new_line_word()
            return err

    def handle_unexpected_keyword(self):
        if self.new_line and self.phase != 3:
            if self.phase == 1:
                if self.symbol.type == self.scanner.CONNECT:
                    print("DONE WITH INIT")
                    self.increment_phase()
                    return True, False
                elif self.expect_type == self.scanner.DEVICE_NAME:
                    self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                        self.scanner.error.SYNTAX)
                    self.expect_type = self.scanner.DEVICE_NAME
                    self.go_to_next_sentece()
                    return True, False
                else:
                    self.handle_error(self.scanner.error.INIT_MISS_KEYWORD,
                                        self.scanner.error.SYNTAX)
                    self.go_to_next_sentece()
                    return True, False
            if self.phase == 2:
                if self.symbol.type == self.scanner.MONITOR:
                    print("DONE WITH CONNECT")
                    self.increment_phase()
                    return True, False
            
                elif self.expect_type == self.scanner.DEVICE_OUT:
                    if self.symbol.type != self.scanner.DEVICE_NAME:
                        self.handle_error(self.scanner.error.CONNECT_WRONG_IO,
                                            self.scanner.error.SYNTAX)
                        self.go_to_next_sentece()
                        return True, False
                
                else:
                    print("SYNTAX[Invalid Connection]: Missing keywords")
                    self.go_to_next_sentece()
                    return True, False
        else:
            if self.phase == 1:
                if self.expect_type == self.scanner.NUMBER:
                    self.handle_error(self.scanner.error.INIT_WRONG_SET,
                                        self.scanner.error.SYNTAX)
                    self.go_to_next_sentece()
                    return True, False
                else:
                    self.handle_error(self.scanner.error.INIT_MISS_KEYWORD,
                                        self.scanner.error.SYNTAX,
                                        front=True)
                    self.go_to_next_sentece()
                    return True, False

            elif self.phase == 2:
                if self.expect_type == self.scanner.DEVICE_IN:
                    self.handle_error(self.scanner.error.CONNECT_WRONG_IO,
                                    self.scanner.error.SYNTAX)
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.go_to_next_sentece()
                else:
                    self.handle_error(
                        self.scanner.error.CONNECT_MISS_KEYWORD,
                        self.scanner.error.SYNTAX,
                        front=True)
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.go_to_next_sentece()
                return True, False
            elif self.phase == 3:
                if self.expect_type == self.scanner.DEVICE_OUT:
                    if self.symbol.type == self.scanner.SEMICOLON:
                        self.expect_type = self.scanner.EOF
                        return True, False
                    elif self.symbol.type != self.scanner.DEVICE_NAME:
                        self.handle_error(
                            self.scanner.error.MONITOR_WRONG_POINT,
                            self.scanner.error.SYNTAX)
                        return False, True
        return False, False

    def parse_init(self):
        err = None
        if self.new_line:
            if self.devices.get_device(self.symbol.id) is None:
                self.device_holder["device_id"] = self.symbol.id
                self.expect_type = self.scanner.INIT_IS
                self.new_line = False
                self.current_device = self.symbol.id
            else:
                if self.symbol.id not in self.error_devices:
                    self.error_devices.append(self.current_device)
                self.handle_error(self.devices.DEVICE_PRESENT,
                                self.scanner.error.SYNTAX)
                self.expect_type = self.scanner.DEVICE_NAME
                self.go_to_next_sentece()
                return (self.devices.DEVICE_PRESENT,
                        self.expect_type)

        else:
            if self.symbol.type == self.scanner.INIT_IS:
                self.expect_type = self.scanner.DEVICE_TYPE

            elif self.symbol.type == self.scanner.DEVICE_TYPE:
                self.sentence_type = self.names.get_name_string(self.symbol.id)
                if self.sentence_type == "XOR":
                    self.device_holder["device_kind"] = self.devices.XOR
                    self.expect_type = self.scanner.SEMICOLON
                elif self.sentence_type == "DTYPE":
                    self.device_holder["device_kind"] = self.devices.D_TYPE
                    self.expect_type = self.scanner.SEMICOLON
                elif self.sentence_type == "SWITCH":
                    self.device_holder["device_kind"] = self.devices.SWITCH
                    self.expect_type = self.scanner.INIT_SWITCH
                elif self.sentence_type == "NAND":
                    self.device_holder["device_kind"] = self.devices.NAND
                    self.expect_type = self.scanner.INIT_WITH
                elif self.sentence_type == "AND":
                    self.device_holder["device_kind"] = self.devices.AND
                    self.expect_type = self.scanner.INIT_WITH
                elif self.sentence_type == "NOR":
                    self.device_holder["device_kind"] = self.devices.NOR
                    self.expect_type = self.scanner.INIT_WITH
                elif self.sentence_type == "OR":
                    self.device_holder["device_kind"] = self.devices.OR
                    self.expect_type = self.scanner.INIT_WITH
                elif self.sentence_type == "CLOCK":
                    self.device_holder["device_kind"] = self.devices.CLOCK
                    self.expect_type = self.scanner.INIT_CLK

            elif self.symbol.type == self.scanner.INIT_SWITCH:
                self.expect_type = self.scanner.NUMBER
            
            elif self.symbol.type == self.scanner.INIT_WITH:
                self.expect_type = self.scanner.NUMBER

            elif self.symbol.type == self.scanner.INIT_CLK:
                self.expect_type = self.scanner.NUMBER
            
            elif self.symbol.type == self.scanner.NUMBER:
                if self.sentence_type == "SWITCH":
                    if (self.names.get_name_string(self.symbol.id) 
                        not in {'0','1'}):
                        self.handle_error(self.scanner.error.INIT_WRONG_SET,
                                            self.scanner.error.SYNTAX)
                        self.error_devices.append(self.current_device)
                        self.expect_type = self.scanner.DEVICE_NAME
                        self.go_to_next_sentece()
                        return (self.scanner.error.INIT_WRONG_SET,
                                self.expect_type)
                    else:
                        self.device_holder["device_property"] = int(
                            self.names.get_name_string(self.symbol.id))
                    self.expect_type = self.scanner.SEMICOLON

                elif self.sentence_type in {"NAND", "AND", "NOR", "OR"}:
                    if (int(self.names.get_name_string(self.symbol.id)) 
                        not in range(1, 17)):
                        self.handle_error(self.devices.INVALID_QUALIFIER,
                                        self.scanner.error.SEMANTIC)
                        self.expect_type = self.scanner.DEVICE_NAME
                        self.go_to_next_sentece()
                        return (self.devices.INVALID_QUALIFIER,
                                self.expect_type)
                    self.device_holder["device_property"] = int(
                        self.names.get_name_string(self.symbol.id))
                    self.expect_type = self.scanner.INIT_GATE

                elif self.sentence_type == "CLOCK":
                    if (int(self.names.get_name_string(self.symbol.id)) 
                        <= 0):
                        self.handle_error(self.devices.INVALID_QUALIFIER,
                                        self.scanner.error.SEMANTIC)
                        self.expect_type = self.scanner.DEVICE_NAME
                        self.error_devices.append(self.current_device)
                        self.go_to_next_sentece()
                        return (self.devices.INVALID_QUALIFIER,
                                self.expect_type)
                    self.device_holder["device_property"] = int(
                        self.names.get_name_string(self.symbol.id))
                    self.expect_type = self.scanner.SEMICOLON
            elif self.symbol.type == self.scanner.INIT_GATE:
                self.expect_type = self.scanner.SEMICOLON
        return err, self.expect_type

    def parse_connect(self):
        err = None
        if self.new_line:
            if self.symbol.type == self.scanner.DEVICE_OUT:
                output_name = self.names.get_name_string(self.symbol.id)
                gate_name, output = output_name.split(".")
                self.connection_holder["first_device_id"] = self.names.query(gate_name)
                self.connection_holder["first_port_id"] = self.names.query(output)
            else:
                self.connection_holder["first_device_id"] = self.symbol.id
            self.expect_type = self.scanner.CONNECTION
            self.new_line = False

        else:
            if self.symbol.type == self.scanner.CONNECTION:
                self.expect_type = self.scanner.DEVICE_IN
            if self.symbol.type == self.scanner.DEVICE_IN:
                input_name = self.names.get_name_string(self.symbol.id)
                gate_name, input = input_name.split(".")
                self.connection_holder["second_device_id"] = self.names.query(gate_name)
                self.connection_holder["second_port_id"] = self.names.query(input)
                self.expect_type = self.scanner.SEMICOLON

        return err, self.expect_type

    def parse_monitor(self):
        err = None
        if self.symbol.type == self.scanner.INIT_MONITOR:
            self.expect_type = self.scanner.DEVICE_OUT
            self.new_line = False
        elif self.symbol.type == self.scanner.DEVICE_OUT:
            output_name = self.names.get_name_string(self.symbol.id)
            gate_name, output = output_name.split(".")
            err = self.monitors.make_monitor(self.names.query(gate_name), self.names.query(output))
            # print(err)
        elif self.symbol.type == self.scanner.DEVICE_NAME:
            err = self.monitors.make_monitor(self.symbol.id, None)
            # print(err)
        return err, self.expect_type

    def parse_network(self):
        """Parse the circuit definition file."""

        if not self.check_structure():
            return False
        self.expect_type = self.scanner.SEMICOLON
        self.sentence_type = None
        self.phase = 1
        self.device_name = False

        self.device_holder = self.init_device_holder()
        self.connection_holder =  self.init_connection_holder()
        self.new_line = False

        while True:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.EOF:
                if self.expect_type == self.scanner.EOF:
                    print("DONE WITH MONITOR")
                else:
                    if self.phase == 3:
                        self.handle_error(self.scanner.error.MISS_TERMINATION,
                                          self.scanner.error.SYNTAX)
                break
            if self.symbol.type == self.scanner.ERROR:
                if self.phase == 1:
                    if self.expect_type == self.scanner.DEVICE_NAME:
                        self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                  self.scanner.error.SYNTAX)
                    else:
                        self.handle_error(self.scanner.error.KEYWORD_NOT_FOUND,
                                  self.scanner.error.SYNTAX)
                elif self.phase == 3:
                    if self.expect_type == self.scanner.DEVICE_OUT:
                        self.handle_error(self.scanner.error.KEYWORD_NOT_FOUND,
                                          self.scanner.error.SYNTAX)
                        break
                else:
                    self.handle_error(self.scanner.error.KEYWORD_NOT_FOUND,
                                      self.scanner.error.SYNTAX)
                self.go_to_next_sentece()
                self.device_holder = self.init_device_holder()
                self.connection_holder = self.init_connection_holder()
                continue

            if self.expect_type == self.scanner.SEMICOLON:
                self.parse_semicolon()
                continue

            if self.expect_type != self.symbol.type:
                continue_break = self.handle_unexpected_keyword()
                if continue_break[1]:
                    break
                elif continue_break[0]:
                    continue
                else:
                    pass

            # Check INIT
            if self.phase == 1:
                self.parse_init()

            # Check for CONNECT
            elif self.phase == 2:
                self.parse_connect()

            # Check for MONITOR
            elif self.phase == 3:
                self.parse_monitor()

        return True


if __name__ == "__main__":
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner('parser_test_file.txt', names, devices, network)

    test_parser = Parser(names, devices, network, monitors, scanner)

    test_parser.parse_network()


