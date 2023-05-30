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
            # print(self.count)
            self.count += 1
        self.set_new_line_word()
        # print("Found new sentence")

    def increment_phase(self):
        self.phase += 1
        self.new_line = False
        self.expect_type = self.scanner.SEMICOLON

    def handle_error(self, error_code, error_type, front=False, start_of_sen=False):
        self.scanner.error.error_code = error_code
        err = self.scanner.print_error_message(self.symbol, 
                                               error_type, 
                                               front=front, 
                                               start_of_sen=start_of_sen)
        print(err)

    def restart_and_get_symbol(self):
        self.scanner.restart()
        self.symbol = self.scanner.get_symbol()

    def check_structure(self):
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

    def parse_network(self):
        """Parse the circuit definition file."""

        if not self.check_structure():
            return False
        self.count = 0
        self.expect_type = self.scanner.SEMICOLON
        self.count += 1
        self.sentence_type = None
        self.phase = 1
        self.device_name = False

        self.device_holder = self.init_device_holder()
        self.connection_holder =  self.init_connection_holder()
        self.new_line = False

        while True:
            # print(self.symbol.type, self.scanner.EOF)
            # print(self.scanner.DEVICE_NAME)
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.EOF:
                if self.expect_type == self.scanner.EOF:
                    print("DONE WITH MONITOR")
                else:
                    if self.phase == 3:
                        self.handle_error(self.scanner.error.MISS_TERMINATION,
                                          self.scanner.error.SYNTAX)
                    # else:
                    #     print("SYNTAX[Incomplete]: File is incompleted") # I think this is redundant
                break
            # print(self.count)
            self.count += 1
            if self.symbol.type == self.scanner.ERROR:
                if self.phase == 1:
                    if self.expect_type == self.scanner.DEVICE_NAME:
                        self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                  self.scanner.error.SYNTAX)
                    else:
                        self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                  self.scanner.error.SYNTAX)
                else:
                    self.handle_error(self.scanner.error.KEYWORD_NOT_FOUND,
                                    self.scanner.error.SYNTAX)
                self.go_to_next_sentece()
                self.device_holder = self.init_device_holder()
                self.connection_holder = self.init_connection_holder()
                continue

            if self.expect_type == self.scanner.SEMICOLON:
                if self.symbol.type != self.scanner.SEMICOLON:
                    self.handle_error(self.scanner.error.MISS_TERMINATION,
                                          self.scanner.error.SYNTAX)
                    while self.symbol.type != self.scanner.SEMICOLON:
                        if self.phase == 1:
                            if self.symbol.type == self.scanner.CONNECT:
                                self.increment_phase()
                                break
                        elif self.phase == 2:
                            if self.symbol.type == self.scanner.MONITOR:
                                self.increment_phase()
                                break
                        self.symbol = self.scanner.get_symbol()
                    self.go_to_next_sentece()
                else:
                    if self.phase == 1 and self.device_holder["device_id"] is not None:
                        err = self.devices.make_device(self.device_holder["device_id"]
                                                 , self.device_holder["device_kind"]
                                                 , self.device_holder["device_property"])
                        self.device_holder = self.init_device_holder()
                        print(err)
                    elif (self.phase == 2 
                          and self.connection_holder["first_device_id"] is not None
                          and self.connection_holder["second_device_id"]):
                        err = self.network.make_connection(self.connection_holder["first_device_id"]
                                                           , self.connection_holder["first_port_id"]
                                                           , self.connection_holder["second_device_id"]
                                                           , self.connection_holder["second_port_id"])
                        self.connection_holder =  self.init_connection_holder()
                        print(err)
                    self.set_new_line_word()
                continue

            if self.expect_type != self.symbol.type:
                if self.new_line and self.phase != 3:
                    if self.phase == 1:
                        if self.symbol.type == self.scanner.CONNECT:
                            print("DONE WITH INIT")
                            self.increment_phase()
                            continue
                        elif self.expect_type == self.scanner.DEVICE_NAME:
                            self.handle_error(self.scanner.error.INIT_WRONG_NAME,
                                              self.scanner.error.SYNTAX)
                            self.expect_type = self.scanner.DEVICE_NAME
                            self.go_to_next_sentece()
                            continue
                        else:
                            self.handle_error(self.scanner.error.INIT_MISS_KEYWORD,
                                              self.scanner.error.SYNTAX)
                            self.go_to_next_sentece()
                            continue
                    if self.phase == 2:
                        if self.symbol.type == self.scanner.MONITOR:
                            print("DONE WITH CONNECT")
                            self.increment_phase()
                            continue
                    
                        elif self.expect_type == self.scanner.DEVICE_OUT:
                            if self.symbol.type != self.scanner.DEVICE_NAME:
                                self.handle_error(self.scanner.error.CONNECT_WRONG_IO,
                                                  self.scanner.error.SYNTAX)
                                self.go_to_next_sentece()
                                continue
                        
                        else:
                            print("SYNTAX[Invalid Connection]: Missing keywords")
                            self.go_to_next_sentece()
                            continue
                else:
                    if self.phase == 1:
                        if self.expect_type == self.scanner.NUMBER:
                            self.handle_error(self.scanner.error.INIT_WRONG_SET,
                                              self.scanner.error.SYNTAX)
                            self.go_to_next_sentece()
                            continue
                        else:
                            self.handle_error(self.scanner.error.INIT_MISS_KEYWORD,
                                              self.scanner.error.SYNTAX,
                                              front=True)
                            self.go_to_next_sentece()
                            continue

                    elif self.phase == 2:
                        if self.expect_type == self.scanner.DEVICE_IN:
                            self.handle_error(self.scanner.error.CONNECT_WRONG_IO,
                                          self.scanner.error.SYNTAX)
                            self.expect_type = self.scanner.DEVICE_NAME
                            self.go_to_next_sentece()
                        else:
                            self.handle_error(self.scanner.error.CONNECT_MISS_KEYWORD,
                                            self.scanner.error.SYNTAX,
                                            front=True)
                            self.expect_type = self.scanner.DEVICE_NAME
                            self.go_to_next_sentece()
                        continue
                    elif self.phase == 3:
                        if self.expect_type == self.scanner.DEVICE_OUT:
                            if self.symbol.type == self.scanner.SEMICOLON:
                                self.expect_type = self.scanner.EOF
                                continue
                            elif self.symbol.type != self.scanner.DEVICE_NAME:
                                print("SYNTAX[Invalid Monitor]: Missing keywords expected a device output")
                                continue
                    else:
                        print("SYNTAX[Invalid Keyword]: Missing keywords")
                        # print("expected", self.names.get_name_string(self.symbol.id))
                        # print("got", self.symbol.type)
                        self.go_to_next_sentece()
                        continue

            # Check INIT
            if self.phase == 1:
                if self.new_line:
                    self.device_holder["device_id"] = self.symbol.id
                    self.expect_type = self.scanner.INIT_IS
                    self.new_line = False
  
                else:
                    if self.symbol.type == self.scanner.INIT_IS:
                        self.expect_type = self.scanner.DEVICE_TYPE

                    elif self.symbol.type == self.scanner.DEVICE_TYPE:
                        self.sentence_type = self.names.get_name_string(self.symbol.id)
                        # print("device", self.names.get_name_string(self.symbol.id))
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
                            if self.names.get_name_string(self.symbol.id) not in {'0','1'}:
                                self.handle_error(self.scanner.error.INIT_WRONG_SET,
                                                  self.scanner.error.SYNTAX)
                            else:
                                self.device_holder["device_property"] = int(self.names.get_name_string(self.symbol.id))
                            self.expect_type = self.scanner.SEMICOLON
                        elif self.sentence_type in {"NAND", "AND", "NOR", "OR"}:
                            self.device_holder["device_property"] = int(self.names.get_name_string(self.symbol.id))
                            self.expect_type = self.scanner.INIT_GATE
                        elif self.sentence_type == "CLOCK":
                            self.device_holder["device_property"] = int(self.names.get_name_string(self.symbol.id))
                            self.expect_type = self.scanner.SEMICOLON
                    elif self.symbol.type == self.scanner.INIT_GATE:
                        self.expect_type = self.scanner.SEMICOLON

            # Check for CONNECT
            elif self.phase == 2:
                if self.new_line:
                    if self.symbol.type == self.scanner.DEVICE_OUT:
                        output_name = self.names.get_name_string(self.symbol.id)
                        gate_name, output = output_name.split(".")
                        # print(gate_name, output)
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
                        # print(self.connection_holder)

            elif self.phase == 3:
                if self.symbol.type == self.scanner.INIT_MONITOR:
                    self.expect_type = self.scanner.DEVICE_OUT
                    self.new_line = False
                elif self.symbol.type == self.scanner.DEVICE_OUT:
                    output_name = self.names.get_name_string(self.symbol.id)
                    gate_name, output = output_name.split(".")
                    err = self.monitors.make_monitor(self.names.query(gate_name), self.names.query(output))
                    print(err)
                elif self.symbol.type == self.scanner.DEVICE_NAME:
                    err = self.monitors.make_monitor(self.symbol.id, None)
                    print(err)

        return True


if __name__ == "__main__":
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner('parser_test_file.txt', names, devices, monitors)

    test_parser = Parser(names, devices, network, monitors, scanner)

    test_parser.parse_network()


