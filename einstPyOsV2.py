'''
einstPyOsV2.py - Einstellungen für pyosv2.py und startPyOsV2.pyw
Copyright (c) Jan. 2021: Andreas Ulrich
<http://erasand.ch>, <andreas@erasand.ch>
'''

# Definition der zu lesenden Verzeichnisse ,JSON Dateien und
# HTML Dokumentation. Über eine ID werden der Quell-Pfad, die zu
# speichernde JSON Datei und die HTML Dokumentation gepaart.
#   {'ID': ('quell/pfad', 'pfad/datei.json', 'pfad/doku.html'), }
# Bei Windows Pfaden mit "\" ist der Zeichenkette ein r voranzustellen:
# r"LW:\pfad\datei.erw"
DC_DIRS = {
    "github": (
        "/home/andreas/github/pyOsTools",
        "./Json/github.json",
        "./Html/github.html"
    ),
    "development": (
        "/home/andreas/Dropbox/1_Ich/2_Projekte/pyOsV2",
        "./Json/development.json",
        "./Html/development.html"
    )
}
# Definition der zu vergleichenden Dateistrukturen anhand von JSON
# Dateien. Über eine ID werden die Quell-, die Ziel- und die
# Unterschied JSON Dateien
# geppart.
#   {'ID': ('pfad/quell.json', 'pfad/ziel.json', 'pfad/diff.json'), }
# Bei Windows Pfaden mit "\" ist der Zeichenkette ein r voranzustellen:
# r"LW:\pfad\datei.erw"
DC_COMP = {
    "dev-git": (
        "./Json/development.json",
        "./Json/github.json",
        "./Json/diff_github.json"
    ),
    "error": (
        "./nicht/quelle.json",
        "./123/nicht/ziel.json",
        "./diff_nicht_da.json"
    )
}
# Ausnahmeliste mit Dateinamen, welche ignoriert werden
LS_AUSNAHMEN = ["Thumbs", ".DS_Store"]
# Ausnahme mit Dateinamen Anfang, welche ignoriert werden
LS_AUSN_START = ["~$", "."]
# Ausnahme mit Dateinamen Ende, welche ignoriert werden
LS_AUSN_ENDE = [".lnk", ".tmp"]
# Wie lange sind die Log-Meldungen am Bildschirm
IN_LOGLEN = 50
# Fenstergrösse
INT_GUI_W = 800
INT_GUI_H = 560
INT_GUI_S = "{0}x{1}".format(INT_GUI_W, INT_GUI_H)
# Spaltenbreiten für die Tabelle Strukturen erfassen
INT_DIRS_W1 = 120
INT_DIRS_W3 = 120
INT_DIRS_W5 = 120
INT_DIRS_W2 = INT_GUI_W - INT_DIRS_W1 - INT_DIRS_W3 - INT_DIRS_W5 - 60
INT_DIRS_W2 = INT_DIRS_W2 // 2
INT_DIRS_W4 = INT_DIRS_W2
# Buttonbreite für Strukturen erfassen, in Anzahl Zeichen
DIRS_BUTTON_W = 24
# Spaltenbreiten für die Tabelle Strukturen vergleichen
INT_COMP_W1 = 60
INT_COMP_W2 = (INT_GUI_W - INT_COMP_W1 - 40) // 4
INT_COMP_W3 = INT_COMP_W2
INT_COMP_W4 = INT_COMP_W2
INT_COMP_W5 = INT_COMP_W2
# Spaltenbreiten für die Tabelle Strukturunterschiede prüfen
INT_DIFF_W1 = 60
INT_DIFF_W3 = 60
INT_DIFF_W4 = 60
INT_DIFF_W5 = 60
INT_DIFF_W6 = 60
INT_DIFF_W7 = 60
INT_DIFF_W8 = 60
INT_DIFF_W2 = INT_GUI_W - INT_DIFF_W1 - INT_DIFF_W3 - INT_DIFF_W4
INT_DIFF_W2 = INT_DIFF_W2 - INT_DIFF_W5 - INT_DIFF_W6
INT_DIFF_W2 = INT_DIFF_W2 - INT_DIFF_W7 - INT_DIFF_W8 - 40
# Maximale Textlänge bei den Pfadinformationen der Strukturunterschiede
INT_DIFF_MAX_PFAD = 44
# Dateimanager:
# "WINDOWS" = Windows Explorer
# "THUNAR" = Linux XFCE Thunar
# "NAUTILUS" = Linux Gnome Nautilus
# "NEMO" = Linux Cinnamon Nemo
TXT_FILEMAN = "THUNAR"
