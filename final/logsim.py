#!/usr/bin/env python3
"""Parse command line options and arguments for the Logic Simulator.

This script parses options and arguments specified on the command line, and
runs either the command line user interface or the graphical user interface.

Usage
-----
Show help: logsim.py -h
Command line user interface: logsim.py -c <file path>
Graphical user interface: logsim.py <file path>
"""
import getopt
import sys
import builtins
import os
import wx
import gettext

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from userint import UserInterface
from gui import Gui


def main(arg_list):
    """Parse the command line options and arguments specified in arg_list.

    Run either the command line user interface, the graphical user interface,
    or display the usage message.
    """
    usage_message = ("Usage:\n"
                     "Show help: logsim.py -h\n"
                     "Command line user interface: logsim.py -c <file path>\n"
                     "Graphical user interface (Japanese):"
                     "logsim.py -j <file path>\n"
                     "Graphical user interface: logsim.py <file path>")
    try:
        options, arguments = getopt.getopt(arg_list, "hc:j:")
    except getopt.GetoptError:
        print("Error: invalid command line arguments\n")
        print(usage_message)
        sys.exit()

    # Initialise instances of the four inner simulator classes
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    # names = None
    # devices = None
    # network = None
    # monitors = None

    # languages supported
    supLang = {u"en_GB.UTF-8": wx.LANGUAGE_ENGLISH,
               u"ja_JP.UTF-8": wx.LANGUAGE_JAPANESE,
               }

    for option, path in options:
        if option == "-h":  # print the usage message
            print(usage_message)
            sys.exit()
        elif option == "-c":  # use the command line user interface
            scanner = Scanner(path, names, devices, network, monitors)
            parser = Parser(names, devices, network, monitors, scanner)
            if parser.parse_network():
                # Initialise an instance of the userint.UserInterface() class
                userint = UserInterface(names, devices, network, monitors)
                userint.command_interface()
        elif option == "-j":  # Launch GUI in Japanese
            scanner = Scanner(path, names, devices, network, monitors)
            parser = Parser(names, devices, network, monitors, scanner)
            if parser.parse_network():
                app = wx.App()

                # Internationalisation
                builtins._ = wx.GetTranslation
                locale = wx.Locale()

                gettext.install('gui', './locale')
                gettext.translation('gui', './locale',
                                    languages=['jp']).install()

                gui = Gui("Logic Simulator", path, names, devices, network,
                          monitors)
                gui.Show(True)
                app.MainLoop()

    if not options:  # no option given, use the graphical user interface

        if len(arguments) != 1:  # wrong number of arguments
            print("Error: one file path required\n")
            print(usage_message)
            sys.exit()

        [path] = arguments
        scanner = Scanner(path, names, devices, network, monitors)
        parser = Parser(names, devices, network, monitors, scanner)
        if parser.parse_network():
            # Initialise an instance of the gui.Gui() class
            app = wx.App()
            # Internationalisation
            # builtins.__dict__["_"] = wx.GetTranslation
            locale = wx.Locale()
            # If an unsupported language is requested default to English
            try:
                lang = os.environ["LANG"]  # Get LANG variable
            except KeyError:
                lang = None  # Set to None if LANG unset
            if lang in supLang:
                selLang = supLang[lang]
            else:
                selLang = wx.LANGUAGE_ENGLISH

            locale.AddCatalogLookupPathPrefix('./locale')
            locale.Init(selLang)
            locale.AddCatalog('logsim_jp')

            gui = Gui("Logic Simulator", path, names, devices, network,
                      monitors)
            gui.Show(True)
            app.MainLoop()


if __name__ == "__main__":
    main(sys.argv[1:])
