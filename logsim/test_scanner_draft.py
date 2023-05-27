from scanner import Scanner,Symbol
from names import Names
import re
from error import Error
names2 = Names()

symbol_type_list = ["ERROR", "INIT", "CONNECT", 
                    'MONITOR', 'DEVICE_TYPE', 
                    'NUMBER', 'DEVICE_NAME', 
                    'DEVICE_IN', 'DEVICE_OUT', 
                    'INIT_IS', 'INIT_WITH', 
                    'INIT_GATE', 'INIT_SWITCH', 
                    'INIT_CLK', 'CONNECTION', 
                    'INIT_MONITOR', 'SEMICOLON', 'EOF']
f = 'test_scanner_draft.txt'
scanner2 = Scanner(f,names2)

# test Error class
e = Error(names2)
e.error_type = e.SYNTAX
e.error_code = e.INIT_WRONG_NAME
scanner2.get_symbol()
scanner2.get_symbol()
sym = scanner2.get_symbol()
print(scanner2.print_error_message(sym, e, f, front=False))
e.error_code = e.INIT_MISS_KEYWORD
print(scanner2.print_error_message(sym, e, f, front=True))



# test symbol.type
'''
sym = symbol_type_list[scanner2.get_symbol().type]
print(sym)
while sym != "EOF" :
    sym = symbol_type_list[scanner2.get_symbol().type]
    print(sym)
'''

# test symbol.id
# test G1
'''
for i in range(2):
    scanner2.get_symbol()
sym = scanner2.get_symbol()
sym_id = sym.id
sym_type = symbol_type_list[sym.type]
print(scanner2.names.get_name_string(sym_id))
'''
#test NAND
'''
scanner2.get_symbol()
sym = scanner2.get_symbol()
sym_id = sym.id
sym_type = symbol_type_list[sym.type]
print(scanner2.names.get_name_string(sym_id))
'''
# test get_sentence(symbol,path)
'''
scanner2.get_symbol()
sym = scanner2.get_symbol()
print(scanner2.get_sentence(sym,f)=="INIT;")
scanner2.get_symbol()
scanner2.get_symbol()
scanner2.get_symbol()
sym = scanner2.get_symbol()
print(scanner2.get_sentence(sym,f)=="G1 is NAND with")
'''

# test print error message
'''
scanner2.get_symbol()
scanner2.get_symbol()
scanner2.get_symbol()
scanner2.get_symbol()

sym = scanner2.get_symbol() # test for symbol in between sentence and remove comment
print(scanner2.print_error_message(sym,"",f,front=False))
print(scanner2.print_error_message(sym,"",f,front=True))

sym = scanner2.get_symbol() # test for ;
print(scanner2.print_error_message(sym,"",f,front=False))
print(scanner2.print_error_message(sym,"",f,front=True))

sym = scanner2.get_symbol() # test for symbol at the start of a sentence
print(scanner2.print_error_message(sym,"",f,front=False))
print(scanner2.print_error_message(sym,"",f,front=True))
'''