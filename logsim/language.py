import wx
import os
import sys
import builtins
from wx.lib.mixins.inspection import InspectionMixin

builtins.__dict__["_"] = wx.GetTranslation
languages = [wx.LANGUAGE_ENGLISH, wx.LANGUAGE_JAPANESE]


def OnInit(self):

        self.Init()
        language = wx.Locale.GetSystemLanguage()

        if language in languages:
            sel_lang = language
        else:
            sel_lang = wx.LANGUAGE_DEFAULT  # English

        # Create locale
        self.locale = wx.Locale(sel_lang)

        if self.locale.IsOk():
            basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
            localedir = os.path.join(basepath, "locale")
            domain = "messages_jp"  # .mo and .po files containing the translations
            self.locale.AddCatalogLookupPathPrefix(localedir)
            self.locale.AddCatalog(domain)
        else:
            self.locale = None

        return True