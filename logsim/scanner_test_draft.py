from scanner import Scanner,Symbol
from names import Names
import re
names2 = Names()
symbol_type_list = ["ERROR", "INIT", "CONNECT", 
                    'MONITOR', 'DEVICE_TYPE', 
                    'NUMBER', 'DEVICE_NAME', 
                    'DEVICE_IN', 'DEVICE_OUT', 
                    'INIT_IS', 'INIT_WITH', 
                    'INIT_GATE', 'INIT_SWITCH', 
                    'INIT_CLK', 'CONNECTION', 
                    'INIT_MONITOR', 'SEMICOLON', 'EOF']
scanner2 = Scanner('scanner_test_draft.txt',names2)

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
for i in range(2):
    scanner2.get_symbol()
sym = scanner2.get_symbol()
sym_id = sym.id
sym_type = symbol_type_list[sym.type]
print(scanner2.names.get_name_string(sym_id))
#test NAND
scanner2.get_symbol()
sym = scanner2.get_symbol()
sym_id = sym.id
sym_type = symbol_type_list[sym.type]
print(scanner2.names.get_name_string(sym_id))




