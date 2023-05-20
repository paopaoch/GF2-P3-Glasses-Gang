"""Map variable names and string names to unique integers.

Used in the Logic Simulator project. Most of the modules in the project
use this module either directly or indirectly.

Classes
-------
Names - maps variable names and string names to unique integers.
"""


class Names:

    """Map variable names and string names to unique integers.

    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
                                               error codes.

    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        """Initialise names list."""
        self.error_code_count = 0  # how many error codes have been declared
        self.names = []

    def unique_error_codes(self, num_error_codes):
        """Return a list of unique integer error codes."""
        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")
        self.error_code_count += num_error_codes
        return range(self.error_code_count - num_error_codes,
                     self.error_code_count)
    

    def query(self, name_string):
        """Return the corresponding name ID for name_string.

        If the name string is not present in the names list, return None.
        """
        if not isinstance(name_string, str):
            raise TypeError("Name string must be a string")
        
        if not name_string.isalnum():
            raise SyntaxError("Name string must be alphanumeric")
        elif name_string.isdigit():
            raise SyntaxError("Name string must contain an alphabet")
        elif name_string.isalpha():
            raise SyntaxError("Name string must contain a digit")
        elif name_string in self.names:
            return self.names.index(name_string)
        else:
            return None


    def lookup(self, name_string_list):
        """Return a list of name IDs for each name string in name_string_list.

        If the name string is not present in the names list, add it.
        """
        if not isinstance(name_string_list, list):
            return TypeError("Input must be a list")
        
        id_list = []
        for name_string in name_string_list:
            if name_string not in self.names:
                self.names.append(name_string)
                id_list.append(self.names.index(name_string))
            else:
                id_list.append(self.names.index(name_string))
            return id_list
        

    def get_name_string(self, name_id):
        """Return the corresponding name string for name_id.

        If the name_id is not an index in the names list, return None.
        """
        if not isinstance(name_id, int):
            return TypeError("Name ID must be an integer")
        
        if name_id < 0:
            raise ValueError
        
        try:
            return self.names[name_id]
        except IndexError:
            return None
