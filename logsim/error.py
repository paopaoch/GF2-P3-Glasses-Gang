"""Store error types and error messages

Used in scanner and parser to indicate the error type hence print the
corresponding error message.

Classes
-------
Error - store error type and its corresponding error message.
"""

from names import Names
from network import Network
from devices import Devices


class Error:
    """Store error type.

    Parameters
    ----------
    names: instance of the names.Names() class.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self, names, network, devices):
        """Initialise error properties."""
        self.names = names
        self.network = network
        self.devices = devices
        # self.error_type = None    # either syntax or semantic
        self.error_type_list = [self.SYNTAX, self.SEMANTIC] = range(2)
        self.error_code = None
        self.syntax_error_list = [self.INIT_MISS_KEYWORD, 
                                  self.INIT_WRONG_NAME,
                                  self.INIT_WRONG_SET, 
                                  self.CONNECT_MISS_KEYWORD,
                                  self.CONNECT_WRONG_IO,
                                  self.MONITOR_MISS_KEYWORD,
                                  self.MONITOR_WRONG_POINT,
                                  self.MISS_DESCRIPTION,
                                  self.MISS_START_MARK,
                                  self.MISS_TERMINATION,
                                  self.KEYWORD_NOT_FOUND,
                                  self.INVALID_COMMENT] = self.names.unique_error_codes(12)
    
        #self.semantic_error_list = [] = self.names.unique_error_codes()
        self.syntax_error_count = 0
        self.semantic_error_count = 0

    def add_error(self, error_type):
        if error_type != self.SYNTAX and error_type !=self.SEMANTIC:
            raise TypeError("there is no error type.")
        if error_type == self.SYNTAX:
            self.syntax_error_count += 1
        elif error_type == self.SEMANTIC:
            self.semantic_error_count += 1

    def error_message(self, error_type, optional_mess=""):
        if error_type != self.SYNTAX and error_type !=self.SEMANTIC:
            raise TypeError("there is no error type.")
        error_mes = ""
        if error_type == self.SYNTAX:
            if self.error_code == self.INIT_MISS_KEYWORD:
                error_mes = f"SYNTAX[Invalid Initialisation]: Missing keywords {optional_mess}"
            elif self.error_code == self.INIT_WRONG_NAME:
                error_mes = f"SYNTAX[Invalid Initialisation]: Invalid device name {optional_mess}"
            elif self.error_code == self.INIT_WRONG_SET:
                error_mes = f"SYNTAX[Invalid Initialisation]: Invalid setting {optional_mess}"
            elif self.error_code == self.CONNECT_MISS_KEYWORD:
                error_mes = f"SYNTAX[Invalid Connection]: Missing keywords {optional_mess}"
            elif self.error_code == self.CONNECT_WRONG_IO:
                error_mes = f"SYNTAX[Invalid Connection]: Invalid device I/O {optional_mess}"
            elif self.error_code == self.MONITOR_MISS_KEYWORD:
                error_mes = f"SYNTAX[Invalid Monitor]: Missing keywords {optional_mess}"
            elif self.error_code == self.MONITOR_WRONG_POINT:
                error_mes = f"""SYNTAX[Invalid Monitor]: Invalid monitor point {optional_mess}"""
            elif self.error_code == self.MISS_DESCRIPTION:
                error_mes = f"SYNTAX[Incomplete File]: Missing sentences {optional_mess}"
            elif self.error_code == self.MISS_START_MARK:
                error_mes = f"SYNTAX[Incomplete File]: Missing start mark {optional_mess}"
            elif self.error_code == self.MISS_TERMINATION:
                error_mes = f"SYNTAX[No Termination]: Missing termination mark {optional_mess}"
            elif self.error_code == self.KEYWORD_NOT_FOUND:
                error_mes = f"SYNTAX[Keyword Not Found]: Invalid keyword {optional_mess}"
            elif self.error_code == self.INVALID_COMMENT:
                error_mes = f"SYNTAX[Invalid Comment]: Missing end comment mark '*/' {optional_mess}"
        
        elif error_type == self.SEMANTIC:
            if self.error_code == self.devices.INVALID_QUALIFIER: # Checks for the number values
                error_mes = f"SEMANTIC[INIT]: Invalid Device Qualifier {optional_mess}"
            elif self.error_code == self.devices.NO_QUALIFIER: # Check for the whether the number exists
                error_mes = f"SEMANTIC[INIT]: No quaifier inputed {optional_mess}"
            elif self.error_code == self.devices.BAD_DEVICE:
                error_mes = f"SEMANTIC[INIT]: Bad device {optional_mess}" # Dunno what this is
            elif self.error_code == self.devices.QUALIFIER_PRESENT:
                error_mes = f"SEMANTIC[INIT]: Qualfier given but not expected {optional_mess}" # Check
            elif self.error_code == self.devices.DEVICE_PRESENT:
                error_mes = f"SEMANTIC[INIT]: Device is being initialised twice {optional_mess}"

            elif self.error_code == self.network.INPUT_TO_INPUT:
                error_mes = f"SEMANTIC[CONNECT]: Input is connected to an input {optional_mess}"
            elif self.error_code == self.network.OUTPUT_TO_OUTPUT:
                error_mes = f"SEMANTIC[CONNECT]: Output is connected to an output {optional_mess}"
            elif self.error_code == self.network.INPUT_CONNECTED:
                error_mes = f"SEMANTIC[CONNECT]: Input is already connected {optional_mess}"

            elif self.error_code == self.network.PORT_ABSENT:
                error_mes = f"SEMANTIC[REFERENCE]: Referencing to an nonexisting port {optional_mess}"
            elif self.error_code == self.network.DEVICE_ABSENT:
                error_mes = f"SEMANTIC[REFERENCE]: Referencing a nonexisting device {optional_mess}"
        
        self.add_error(error_type)
        return error_mes
        