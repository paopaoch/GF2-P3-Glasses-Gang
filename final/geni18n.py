# -*- coding: utf-8 -*-
"""
This will generate the .pot and .mo files for the application domain and
languages defined below.

The .po and .mo files are placed as per convention in

"appfolder/locale/lang/LC_MESSAGES"

The .pot file is placed in the locale folder.

This script or something similar should be added to your build process.

The actual translation work is normally done using a tool like poEdit or
similar, it allows you to generate a particular language catalog from the .pot
file or to use the .pot to merge new translations into an existing language
catalog.

"""

import os
import subprocess
import polib
from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo

appFolder = os.getcwd()
outFolder = os.path.join(appFolder, 'locale')

# Build command for xgettext (gettext)
xgtOptions = '--language=Python --keyword=_u -o {outpot} {sourcefile}'
xgtCmd = 'xgettext ' + xgtOptions.format(outpot=os.path.join(
    outFolder, 'logsim_translated.pot'),
    sourcefile=os.path.join(appFolder, 'gui.py'))

print("Generating the .pot file")
print("cmd: %s" % xgtCmd)
rCode = subprocess.call(xgtCmd, shell=True)
print("return code: %s\n\n" % rCode)
