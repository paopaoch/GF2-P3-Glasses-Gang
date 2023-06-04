# # -*- coding: utf-8 -*-
# """
# This will generate the .pot and .mo files for the application domain and
# languages defined below.

# The .po and .mo files are placed as per convention in

# "appfolder/locale/lang/LC_MESSAGES"

# The .pot file is placed in the locale folder.

# This script or something similar should be added to your build process.

# The actual translation work is normally done using a tool like poEdit or
# similar, it allows you to generate a particular language catalog from the .pot
# file or to use the .pot to merge new translations into an existing language
# catalog.

# """

# import subprocess
# import sys
# import os
# import app_const as appC

# # we remove English as source code strings are in English
# supportedLang = []
# for l in appC.supLang:
#     if l != u"en":
#         supportedLang.append(l)


# appFolder = os.getcwd()

# # setup some stuff to get at Python I18N tools/utilities

# pyExe = sys.executable
# pyFolder = os.path.split(pyExe)[0]
# pyToolsFolder = os.path.join(pyFolder, 'Tools')
# pyI18nFolder = os.path.join(pyToolsFolder, 'i18n')
# pyGettext = os.path.join(pyI18nFolder, 'pygettext.py')
# pyMsgfmt = os.path.join(pyI18nFolder, 'msgfmt.py')
# outFolder = os.path.join(appFolder, 'locale')

# # build command for pygettext
# gtOptions = '-a -d %s -o %s.pot -p %s %s'
# tCmd = pyExe + ' ' + pyGettext + ' ' + (gtOptions % (appC.langDomain,
#                                                      appC.langDomain,
#                                                      outFolder,
#                                                      appFolder))
# print("Generating the .pot file")
# print("cmd: %s" % tCmd)
# rCode = subprocess.call(tCmd)
# print("return code: %s\n\n" % rCode)

# for tLang in supportedLang:
#     # build command for msgfmt
#     langDir = os.path.join(appFolder, ('locale\%s\LC_MESSAGES' % tLang))
#     poFile = os.path.join(langDir, appC.langDomain + '.po')
#     tCmd = pyExe + ' ' + pyMsgfmt + ' ' + poFile

#     print("Generating the .mo file")
#     print("cmd: %s" % tCmd)
#     rCode = subprocess.call(tCmd)
#     print("return code: %s\n\n" % rCode)
# import os
# import subprocess
# import polib

# appFolder = os.getcwd()
# outFolder = os.path.join(appFolder, 'locale')

# # Build command for xgettext (gettext)
# xgtOptions = '--language=Python --keyword=_u -o {outpot} {sourcefile}'
# xgtCmd = 'xgettext ' + xgtOptions.format(outpot=os.path.join(
#     outFolder, 'logsim_translated.pot'), sourcefile=os.path.join(appFolder, 'gui.py'))

# print("Generating the .pot file")
# print("cmd: %s" % xgtCmd)
# rCode = subprocess.call(xgtCmd, shell=True)
# print("return code: %s\n\n" % rCode)

# # Generate .mo files for each language
# supportedLang = ['fr_FR', 'es_ES']

# for lang in supportedLang:
#     langDir = os.path.join(outFolder, lang, 'LC_MESSAGES')
#     os.makedirs(langDir, exist_ok=True)

#     # Build command for msgfmt
#     poFile = os.path.join(outFolder, 'logsim_translated.po')
#     moFile = os.path.join(langDir, 'logsim_translated.mo')
#     msgfmtCmd = f'msgfmt -o {moFile} {poFile}'

#     print("Generating the .mo file for language:", lang)
#     print("cmd:", msgfmtCmd)
#     rCode = subprocess.call(msgfmtCmd, shell=True)
#     print("return code:", rCode)
#     print()

# # Load the .pot file and create a new .po file for translation
# potFile = os.path.join(outFolder, 'logsim_translated.pot')
# try:
#     po = polib.pofile(potFile)
#     po.save(os.path.join(outFolder, 'es_ES', 'LC_MESSAGES', 'logsim_translated.po'))
#     print("Successfully created the .po file for translation.")
# except Exception as e:
#     print("Error occurred while processing the .pot file:", str(e))
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
    outFolder, 'logsim_translated.pot'), sourcefile=os.path.join(appFolder, 'gui.py'))

print("Generating the .pot file")
print("cmd: %s" % xgtCmd)
rCode = subprocess.call(xgtCmd, shell=True)
print("return code: %s\n\n" % rCode)

# # Generate .mo files for each language
# supportedLang = ['fr_FR', 'es_ES']

# for lang in supportedLang:
#     langDir = os.path.join(outFolder, lang, 'LC_MESSAGES')
#     os.makedirs(langDir, exist_ok=True)

#     # Build paths for .po and .mo files
#     poFile = os.path.join(outFolder, 'logsim_translated.po')
#     moFile = os.path.join(langDir, 'logsim_translated.mo')

#     # Read the .po file
#     po = read_po(poFile)

#     # Write the .mo file
#     with open(moFile, 'wb') as f:
#         write_mo(f, po)

#     print("Successfully generated the .mo file for language:", lang)

# print()
# print("Translation files generated successfully.")
