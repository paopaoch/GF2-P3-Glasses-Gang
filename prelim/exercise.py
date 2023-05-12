#!/usr/bin/env python3
"""Preliminary exercises for Part IIA Project GF2."""
import sys
import os
from mynames import MyNames


def open_file(path):
    """Open and return the file specified by path."""
    try:
        f = open(path, "r")
        return f
    except IOError:
        print ("Error: can\'t find file or read data")


def get_next_character(input_file):
    """Read and return the next character in input_file."""
    try:
        character = input_file.read(1)
        if character:
            return character
        else:
            return ""
    except IOError:
        print ("Error: can\'t find file or read data")



def get_next_non_whitespace_character(input_file):
    """Seek and return the next non-whitespace character in input_file."""
    try:
        while True:
            character = input_file.read(1)
            if not character:
                return ""
            elif not character.isspace():
                return character
    except IOError:
        print ("Error: can\'t find file or read data")        
    


def get_next_number(input_file):
    """Seek the next number in input_file.

    Return the number (or None) and the next non-numeric character.
    """
    try:
        number = ''
        while True:
            character = input_file.read(1)
            if not character:
                if not number:
                    return None
                else:
                    return [int(number), '']
            elif character.isdigit():
                number += character
            else:
                if number:
                    return [int(number), character]
                
        return None
    except IOError:
        print ("Error: can\'t find file or read data") 


def get_next_name(input_file):
    """Seek the next name string in input_file.

    Return the name string (or None) and the next non-alphanumeric character.
    """
    try:
        name = ""
        char = input_file.read(1)
        while char and not char.isalpha():
            char = input_file.read(1)
        if not char:
            return [None, ""]

        name += char
        char = input_file.read(1)
        while char and char.isalnum():
            name += char
            char = input_file.read(1)

        if not char:
            return [name, ""]
        else:
            return [name, char]
        
    except IOError:
        print ("Error: can\'t find file or read data") 



def main():
    """Preliminary exercises for Part IIA Project GF2."""

    # Check command line arguments
    arguments = sys.argv[1:]
    path = sys.argv[1]

    if len(arguments) != 1:
        print("Error! One command line argument is required.")
        sys.exit()

    else: 
        print("\nNow opening file...")
        # Print the path provided and try to open the file for reading
        print(path)
        fo = open_file(path)

        print("\nNow reading file...")
        # Print out all the characters in the file, until the end of file
        # Iterate over the characters in the file
        while True:
            char = get_next_character(fo)
            if not char:
                break
            print(char, end='')

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        # Reset the file pointer to the beginning of the file
        fo.seek(0)

        # Iterate over the non-whitespace characters in the file
        while True:
            char = get_next_non_whitespace_character(fo)
            if not char:
                break
            print(char, end='')

        print("\nNow reading numbers...")
        # Print out all the numbers in the file
        # Reset the file pointer to the beginning of the file
        fo.seek(0)

        # Iterate over the numbers in the file
        while True:
            number = get_next_number(fo)
            if not number:
                break
            print(number[0], end=' ')  # print the integer representation of the number
            if number[1] == '':
                break

        print("\nNow reading names...")
        # Print out all the names in the file
        fo.seek(0)  # reset file pointer to beginning of file
        name, char = get_next_name(fo)
        while name is not None:
            print(name)
            name, char = get_next_name(fo)

        print("\nNow censoring bad names...")
        # Print out only the good names in the file
        
        # Reset the file pointer to the beginning of the file
        fo.seek(0)
        name, char = get_next_name(fo)

        name_table = MyNames()
        bad_name_ids = [name_table.lookup("Terrible"), name_table.lookup("Horrid"),
                        name_table.lookup("Ghastly"), name_table.lookup("Awful")]
        
        while name is not None:
            name_id = name_table.lookup(name)
            if name_id not in bad_name_ids:
                print(name_table.get_string(name_id))

            name, char = get_next_name(fo)
        # Close the file
        fo.close()


if __name__ == "__main__":
    main()
