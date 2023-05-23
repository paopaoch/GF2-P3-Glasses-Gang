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

sym = symbol_type_list[scanner2.get_symbol().type]
print(sym)
while sym != "EOF" :
    sym = symbol_type_list[scanner2.get_symbol().type]
    print(sym)





