"""Store error types and error messages

Used in scanner and parser to indicate the error type hence print the
corresponding error message.

Classes
-------
Error - store error type and its corresponding error message.
"""


class Error:
    """Store error type.

    Parameters
    ----------
    names: instance of the names.Names() class.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self, names):
        """Initialise error properties."""
        self.names = names
        self.error_type = None    # either syntax or semantic
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

    def add_error(self):
        if not self.error_type:
            raise TypeError("there is no error type.")
        if self.error_type == self.SYNTAX:
            self.syntax_error_count += 1
        elif self.error_type == self.SEMANTIC:
            self.semantic_error_count += 1

    def error_message(self):
        if self.error_type is None:
            raise TypeError("there is no error type.")
        error_mes = ""
        if self.error_type == self.SYNTAX:
            if self.error_code == self.INIT_MISS_KEYWORD:
                error_mes = "SYNTAX[Invalid Initialisation]: Missing keywords"
            elif self.error_code == self.INIT_WRONG_NAME:
                error_mes = "SYNTAX[Invalid Initialisation]: Invalid device name"
            elif self.error_code == self.INIT_WRONG_SET:
                error_mes = "SYNTAX[Invalid Initialisation]: Invalid setting"
            elif self.error_code == self.CONNECT_MISS_KEYWORD:
                error_mes = "SYNTAX[Invalid Connection]: Missing keywords"
            elif self.error_code == self.CONNECT_WRONG_IO:
                error_mes = "SYNTAX[Invalid Connection]: Invalid device I/O"
            elif self.error_code == self.MONITOR_MISS_KEYWORD:
                error_mes = "SYNTAX[Invalid Monitor]: Missing keywords"
            elif self.error_code == self.MONITOR_WRONG_POINT:
                error_mes = "SYNTAX[Invalid Monitor]: Invalid monitor point"
            elif self.error_code == self.MISS_DESCRIPTION:
                error_mes = "SYNTAX[Incomplete File]: Missing sentences"
            elif self.error_code == self.MISS_START_MARK:
                error_mes = "SYNTAX[Incomplete File]: Missing start mark"
            elif self.error_code == self.MISS_TERMINATION:
                error_mes = "SYNTAX[No Termination]: Missing termination mark"
            elif self.error_code == self.KEYWORD_NOT_FOUND:
                error_mes = "SYNTAX[Keyword Not Found]: Invalid keyword"
            elif self.error_code == self.INVALID_COMMENT:
                error_mes = "SYNTAX[Invalid Comment]: Missing '*/'"
        elif self.error_type == self.SEMANTIC:
            pass
        
        return error_mes
        