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
        self.eof_reached = False

        self.new_line = True
        self.expect_type = None
        self.sentence_type = None
        self.error_devices = []  # tracks any devices with errors
        self.current_device = None


    def set_new_line_word(self):
        """Set the expected type of symbol depending on the phase"""
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
        self.phase += 1
        self.new_line = False
        self.expect_type = self.scanner.SEMICOLON


    def handle_error(self, error_code, error_type, 
                     front=False, start_of_sen=False, 
                     behind=False, optional_mess=""):
        """Function to show the error"""
        self.scanner.error.error_code = error_code
        print(self.scanner.print_error_message(self.symbol,
                                               error_type, 
                                               front=front, 
                                               start_of_sen=start_of_sen,
                                               behind=behind,
                                               optional_mess=optional_mess))
        print("\n---------------------------------------------------------\n")


    def restart_and_get_symbol(self):
        self.scanner.restart()
        self.symbol = self.scanner.get_symbol()


    def check_structure(self):
        """Check if for structural errors in the files.

        This includes missing start mark and it's
        coresponding semicolon eg. CONNECT
        and missing sentences in phases
        """
        self.symbol = self.scanner.get_symbol()
        self.expect_type = self.scanner.INIT
        self.phase = 1
        pos = 1
        init_pos = 0
        connect_pos = None
        monitor_pos = 0
        error = False
        if self.symbol.type != self.expect_type:  # Check for INIT
            self.scanner.restart()
            error = True
        else:
            init_pos = pos

        # Loop through file for crude checking of file structure
        while self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()
            
            if self.symbol.type == self.scanner.CONNECT:
                if self.phase == 1:
                    self.phase = 2
                    connect_pos = pos

            if self.symbol.type == self.scanner.MONITOR:
                if self.phase in [1,2]:
                    self.phase = 3
                    monitor_pos = pos
            pos += 1

        # check for INIT
        if init_pos == 0:
            self.restart_and_get_symbol()
            self.handle_error(self.scanner.error.MISS_START_MARK,
                              self.scanner.error.SYNTAX, 
                              start_of_sen=True,
                              optional_mess="INIT")
            error = True
        # check for CONNECT
        if connect_pos is None:
            self.restart_and_get_symbol()
            while (self.symbol.type != self.scanner.MONITOR 
                    and self.symbol.type != self.scanner.EOF):
                self.symbol = self.scanner.get_symbol()
            self.handle_error(self.scanner.error.MISS_START_MARK,
                              self.scanner.error.SYNTAX,
                              start_of_sen=True,
                              optional_mess="CONNECT")
            error = True

        # Check for INIT sentence
        if connect_pos is not None:
            if connect_pos - init_pos < 2:
                self.restart_and_get_symbol()
                self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                  self.scanner.error.SYNTAX,
                                  optional_mess="for INIT")
                error = True
        
        # Check for CONNECT sentence
        if connect_pos is not None:
            if monitor_pos == 0:
                if pos - connect_pos < 4:
                    self.restart_and_get_symbol()
                    while self.symbol.type != self.scanner.CONNECT:
                        self.symbol = self.scanner.get_symbol()
                    self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                        self.scanner.error.SYNTAX,
                                        optional_mess="for CONNECT")
                    error = True
            else:
                if monitor_pos - connect_pos < 3:
                    self.restart_and_get_symbol()
                    while self.symbol.type != self.scanner.CONNECT:
                        self.symbol = self.scanner.get_symbol()
                    self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                    self.scanner.error.SYNTAX,
                                    optional_mess="for CONNECT")
                    error = True

        # Check for monitoring sentence
        if monitor_pos != 0:
            if pos - monitor_pos < 4:
                self.restart_and_get_symbol()
                while self.symbol.type != self.scanner.MONITOR:
                    self.symbol = self.scanner.get_symbol()
                self.handle_error(self.scanner.error.MISS_DESCRIPTION,
                                  self.scanner.error.SYNTAX,
                                  optional_mess="for MONITOR")
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
            # Handle error when a semicolon is not found
            self.handle_error(self.scanner.error.MISS_TERMINATION,
                                    self.scanner.error.SYNTAX,
                                    front=True)
            while self.symbol.type != self.scanner.SEMICOLON:
                if self.phase == 1:
                    if self.symbol.type == self.scanner.CONNECT:
                        self.increment_phase()
                        break
                elif self.phase == 2:
                    if self.symbol.type == self.scanner.MONITOR:
                        self.increment_phase()
                        break
                elif self.phase == 3:
                    if (self.symbol.type == self.scanner.EOF):
                        self.expect_type = self.scanner.SEMICOLON
                        self.eof_reached = True
                        break
                self.symbol = self.scanner.get_symbol()
            self.go_to_next_sentece()
            return self.scanner.error.MISS_TERMINATION
        
        else:
            if (self.phase == 1 
                and self.device_holder["device_id"] is not None):
                err = self.devices.make_device(
                    self.device_holder["device_id"],
                    self.device_holder["device_kind"],
                    self.device_holder["device_property"])
                self.device_holder = self.init_device_holder()
                if err != self.devices.NO_ERROR:
                    self.handle_error(err,
                                      self.scanner.error.SEMANTIC)

            elif (self.phase == 2 
                    and self.connection_holder["first_device_id"] is not None
                    and self.connection_holder["second_device_id"] is not None):
                err = self.network.make_connection(
                    self.connection_holder["first_device_id"]
                    ,self.connection_holder["first_port_id"]
                    ,self.connection_holder["second_device_id"]
                    ,self.connection_holder["second_port_id"])
                self.connection_holder = self.init_connection_holder()
                if err != self.network.NO_ERROR:
                    self.handle_error(err,
                                      self.scanner.error.SEMANTIC,
                                      behind=True)
            self.set_new_line_word()
            return err


    def handle_unexpected_keyword(self):
        """Handles the case when the symbol receive has an unexpected type"""
        if self.new_line:
            if self.phase == 1:
                if self.symbol.type == self.scanner.CONNECT:
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
                    self.increment_phase()
                    return True, False
                elif self.expect_type == self.scanner.DEVICE_OUT:
                    if self.symbol.type != self.scanner.DEVICE_NAME:
                        self.handle_error(self.scanner.error.CONNECT_WRONG_IO,
                                            self.scanner.error.SYNTAX)
                        self.go_to_next_sentece()
                        return True, False
                    
            else:
                if self.expect_type == self.scanner.EOF:
                    optional_mess = "EOF"
                else:
                    optional_mess = ""
                self.handle_error(self.scanner.error.MONITOR_MISS_KEYWORD,
                                        self.scanner.error.SYNTAX,
                                        front=True,
                                        optional_mess=optional_mess)
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
                        if self.monitors.monitors_dictionary == {}:
                            self.handle_error(
                                self.scanner.error.MONITOR_MISS_KEYWORD,
                                self.scanner.error.SYNTAX,
                                front=True)
                            return False, True
                        else:
                            self.expect_type = self.scanner.EOF
                            return True, False
                    if self.symbol.type == self.scanner.DEVICE_NAME:
                        return False, False
                    else:
                        self.handle_error(
                            self.scanner.error.MONITOR_MISS_KEYWORD,
                            self.scanner.error.SYNTAX,
                            front=True)
                        return False, True
        return False, False


    def parse_init(self):
        """Take care of handling an initialisation sentence
        
        If type is as expected and in phase 1 and not a semicolon
        then this function is run.
        """
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
                                self.scanner.error.SEMANTIC)
                self.expect_type = self.scanner.DEVICE_NAME
                self.go_to_next_sentece()
                return (self.devices.DEVICE_PRESENT,
                        self.expect_type)

        else:
            if self.symbol.type == self.scanner.INIT_IS:
                self.expect_type = self.scanner.DEVICE_TYPE

            elif self.symbol.type == self.scanner.DEVICE_TYPE:
                self.sentence_type = (self
                                      .names
                                      .get_name_string(self.symbol.id))
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
                # Maintenance
                elif self.sentence_type == "RC":
                    self.device_holder["device_kind"] = self.devices.RC
                    self.expect_type = self.scanner.INIT_CLK
                elif self.sentence_type == "SIGGEN":
                    self.device_holder["device_kind"] = self.devices.SIGGEN
                    self.expect_type = self.scanner.INIT_WITH

            elif self.symbol.type == self.scanner.INIT_SWITCH:
                self.expect_type = self.scanner.NUMBER
            
            elif self.symbol.type == self.scanner.INIT_CLK:
                self.expect_type = self.scanner.NUMBER

            elif self.symbol.type == self.scanner.INIT_WITH:
                if self.sentence_type == "SIGGEN":
                    self.expect_type = self.scanner.SIGGEN_WAVE
                else:
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

                # Maintenance
                elif self.sentence_type == "RC":
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

            elif self.symbol.type == self.scanner.SIGGEN_WAVE:
                self.device_holder["device_property"] = str(
                    self.names.get_name_string(self.symbol.id))
                self.expect_type = self.scanner.SEMICOLON

            elif self.symbol.type == self.scanner.INIT_GATE:
                self.expect_type = self.scanner.SEMICOLON
        return err, self.expect_type


    def parse_connect(self):
        """Take care of handling an connection sentence
        
        If type is as expected and in phase 2 and not a semicolon
        then this function is run.
        """
        err = None
        if self.new_line:
            if self.symbol.type == self.scanner.DEVICE_OUT:
                output_name = self.names.get_name_string(self.symbol.id)
                gate_name, output = output_name.split(".")
                device_id = self.names.query(gate_name)
                if self.devices.get_device(device_id) is not None:
                    port_id = self.names.query(output)
                    self.connection_holder["first_device_id"] = device_id
                    self.connection_holder["first_port_id"] = port_id
                else:
                    if device_id not in self.error_devices:
                        self.handle_error(self.network.DEVICE_ABSENT,
                                        self.scanner.error.SEMANTIC)
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.go_to_next_sentece()
                    return self.network.DEVICE_ABSENT, self.expect_type

            else:
                if self.devices.get_device(self.symbol.id) is not None:
                    self.connection_holder["first_device_id"] = self.symbol.id
                else:
                    if self.symbol.id not in self.error_devices:
                        self.handle_error(self.network.DEVICE_ABSENT,
                                            self.scanner.error.SEMANTIC)
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.go_to_next_sentece()
                    return self.network.DEVICE_ABSENT, self.expect_type
            self.expect_type = self.scanner.CONNECTION
            self.new_line = False

        else:
            if self.symbol.type == self.scanner.CONNECTION:
                self.expect_type = self.scanner.DEVICE_IN
            if self.symbol.type == self.scanner.DEVICE_IN:
                self.expect_type = self.scanner.SEMICOLON
                input_name = self.names.get_name_string(self.symbol.id)
                gate_name, input = input_name.split(".")
                # Check clock input to Dtype clock
                device_id = self.names.query(gate_name)
                device = self.devices.get_device(device_id)
                if device is not None:
                    if (device.device_kind == self.devices.D_TYPE
                        and input == "CLK"):
                        first_device = self.devices.get_device(
                            self.connection_holder["first_device_id"])
                        if (first_device.device_kind
                            != self.devices.CLOCK):
                            err = self.scanner.error.NOT_CLOCK_TO_CLK
                            self.handle_error(err,
                                            self.scanner.error.SEMANTIC)
                            self.connection_holder = (self
                                                .init_connection_holder())
                    
                    # Maintenance
                    first_device = self.devices.get_device(
                            self.connection_holder["first_device_id"])
                    if first_device is not None:
                        if first_device.device_kind == self.devices.RC:
                            second_device = self.devices.get_device(device_id)
                            if (second_device.device_kind 
                                != self.devices.D_TYPE
                                or (second_device.device_kind 
                                    == self.devices.D_TYPE
                                    and input not in ["CLEAR", "SET"])):
                                err = self.scanner.error.NOT_RC_TO_D_TYPE
                                self.handle_error(err,
                                                self.scanner.error.SEMANTIC)
                                self.connection_holder = (self
                                                    .init_connection_holder())
                else:
                    err = self.network.DEVICE_ABSENT
                    self.handle_error(err,
                                    self.scanner.error.SEMANTIC)
                    self.connection_holder = (self
                                    .init_connection_holder())

                port_id = self.names.query(input)
                self.connection_holder["second_device_id"] = device_id
                self.connection_holder["second_port_id"] = port_id
        return err, self.expect_type


    def parse_monitor(self):
        """Take care of handling a monitor sentence

        If type is as expected and in phase 3 and not a semicolon
        then this function is run.
        """
        err = None
        if self.symbol.type == self.scanner.INIT_MONITOR:
            self.expect_type = self.scanner.DEVICE_OUT
            self.new_line = False
        elif self.symbol.type == self.scanner.DEVICE_OUT:
            output_name = self.names.get_name_string(self.symbol.id)
            gate_name, output = output_name.split(".")
            err = self.monitors.make_monitor(self.names.query(gate_name), 
                                             self.names.query(output))
        elif self.symbol.type == self.scanner.DEVICE_NAME:
            err = self.monitors.make_monitor(self.symbol.id, None)

        if err != self.monitors.NO_ERROR and err is not None:
            self.handle_error(err, self.scanner.error.SEMANTIC)
            return err, self.expect_type
        return None, self.expect_type


    def print_end_message(self):
        print("Failed to compile definition file")
        print("Syntax error count:", self.scanner.error.syntax_error_count)
        print("Semantic error count:", 
                self.scanner.error.semantic_error_count)


    def parse_network(self):
        """Parse the circuit definition file.
        
        It first checks the structure of the file. If there are
        no errors then the file is restarted and each symbol 
        is parsed individually. The function takes care of an error,
        semicolon, and unexpected symbol first before parsing sentences
        according to the phase it is in"""
        if not self.check_structure():
            self.print_end_message()
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

            # Stopping criterion
            if self.symbol.type == self.scanner.EOF:
                if self.expect_type == self.scanner.EOF:
                    pass
                else:
                    if self.phase == 3 and self.eof_reached:
                        self.handle_error(self.scanner.error.MISS_TERMINATION,
                                          self.scanner.error.SYNTAX)
                    elif (self.phase == 3 and 
                          self.expect_type == self.scanner.DEVICE_OUT):
                        self.handle_error(self.scanner.error.MISS_TERMINATION,
                                          self.scanner.error.SYNTAX)
                break

            # Deal with error symbols
            if self.symbol.type == self.scanner.ERROR:
                if self.phase == 1:
                    if self.expect_type == self.scanner.DEVICE_NAME:
                        self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                  self.scanner.error.SYNTAX)
                    else:
                        self.handle_error(self.scanner
                                            .error
                                            .KEYWORD_NOT_FOUND,
                                        self.scanner
                                            .error
                                            .SYNTAX)
                elif self.phase == 3:
                    if self.expect_type == self.scanner.DEVICE_OUT:
                        self.handle_error(self.scanner
                                          .error
                                          .KEYWORD_NOT_FOUND,
                                          self.scanner
                                          .error
                                          .SYNTAX)
                        break
                    else:
                        self.handle_error(self.scanner
                                          .error
                                          .KEYWORD_NOT_FOUND,
                                        self.scanner
                                        .error
                                        .SYNTAX)
                        break
                else:
                    self.handle_error(self.scanner.error.KEYWORD_NOT_FOUND,
                                      self.scanner.error.SYNTAX)
                self.go_to_next_sentece()
                self.device_holder = self.init_device_holder()
                self.connection_holder = self.init_connection_holder()
                continue

            # Deals with a semicolon
            if self.expect_type == self.scanner.SEMICOLON:
                self.parse_semicolon()
                continue

            # Deals with an unexpected symbol
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

        # Run whole circuit semantic checks if no previous errors
        if (self.scanner.error.semantic_error_count == 0
            and self.scanner.error.syntax_error_count == 0):
            # Check if all inputs are connected
            if self.network.check_network():
                # Check if net work oscillate
                if self.network.execute_network():
                    print("File compiled successfully!")
                    return True
                else:
                    self.restart_and_get_symbol()
                    self.handle_error(self.scanner.error.OSCILLATE,
                                self.scanner.error.SEMANTIC)
                    return False
            else:
                self.restart_and_get_symbol()
                self.handle_error(self.scanner.error.UNUSED_INPUTS,
                                self.scanner.error.SEMANTIC)
                return False
        else:
            self.print_end_message()
            return False