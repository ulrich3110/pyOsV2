#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter
from tkinter import ttk
from tkinter import messagebox
import pyosv2
from einstPyOsV2 import *

'''
startPyOsV2.pyw - Tkinter GUI für pyosv2.py
Copyright (c) Jan. 2021: Andreas Ulrich
<http://erasand.ch>, <andreas@erasand.ch>

LIZENZ
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

DEUTSCHE ÜBERSETZUNG: <http://www.gnu.de/documents/gpl-3.0.de.html>
'''


def f_filemanager(tx_pfad):
    '''
    Öffnet den Dateimanager definiert in <TXT_FILEMAN> mit dem <pfad>
    '''
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    tx_pfad = os.path.abspath(tx_pfad)
    tx_verz = os.path.dirname(tx_pfad)
    if os.path.isdir(tx_verz):
        # Pfad existiert
        tx_cmd = ""
        if TXT_FILEMAN == "THUNAR":
            tx_cmd = "thunar '{0}'".format(tx_verz)
            print(tx_cmd)
            os.system(tx_cmd)
        elif TXT_FILEMAN == "NAUTILUS":
            tx_cmd = "Nautilus '{0}'".format(tx_verz)
            print(tx_cmd)
            os.system(tx_cmd)
        elif TXT_FILEMAN == "NEMO":
            tx_cmd = "Nemo '{0}'".format(tx_verz)
            print(tx_cmd)
            os.system(tx_cmd)
        elif TXT_FILEMAN == "WINDOWS":
            print("Windows Explorer {0}".format(tx_verz))
            os.startfile(tx_verz)


def f_datum_tmj(tx_datum):
    '''
    Wandelt das Textformat von jjjj-mm-tt HH:MM:SS
                               0123456789012345678
    zu tt.mm.jjjj um
    '''
    tx_j = tx_datum[0:4]
    tx_m = tx_datum[5:7]
    tx_t = tx_datum[8:10]
    tx_tmj = "{0}.{1}.{2}".format(tx_t, tx_m, tx_j)
    return(tx_tmj)


class GuiOsTools():
    '''
    Benutzeroberfläche pyOsTools
    '''

    def __init__(self, ob_master):
        '''
        Initalisation, GUI erstellen
         .ob_master = <tkinter.Tk>
         .ob_notebk = <ttk.Notebook>
         .ob_dirs_frm = <ttk.Frame>
         .ob_comp_frm = <ttk.Frame>
         .ob_diff_frm = <ttk.Frame>
         .ob_exit = <ttk.Button>, Beenden
        '''
        # Root
        self.ob_master = ob_master
        # Fenster Titel & Grösse
        self.ob_master.title("pyOsV2")
        self.ob_master.geometry(INT_GUI_S)
        # Notebook
        self.ob_notebk = ttk.Notebook(self.ob_master)
        self.ob_notebk.pack(padx=5, pady=5, expand=True)
        # Register definieren
        self.ob_dirs_frm = ttk.Frame(
            self.ob_notebk,
            width=INT_GUI_W - 10,
            height=INT_GUI_H - 80
        )
        self.ob_comp_frm = ttk.Frame(
            self.ob_notebk,
            width=INT_GUI_W - 10,
            height=INT_GUI_H - 80
        )
        self.ob_diff_frm = ttk.Frame(
            self.ob_notebk,
            width=INT_GUI_W - 10,
            height=INT_GUI_H - 80
        )
        self.ob_dirs_frm.pack(fill='both', expand=True)
        self.ob_comp_frm.pack(fill='both', expand=True)
        self.ob_diff_frm.pack(fill='both', expand=True)
        # Register dem Notebook hinzufügen
        self.ob_notebk.add(
            self.ob_dirs_frm,
            text='Verzeichnis Strukturen erstellen'
        )
        self.ob_notebk.add(
            self.ob_comp_frm,
            text='Verzeichnis Strukturen vergleichen'
        )
        self.ob_notebk.add(
            self.ob_diff_frm,
            text='Prüf Resultat Ziel Struktur'
        )
        # Elemente für .dirs_frame
        self.m_dirs_setgui()
        # Elemente für .comp_frame
        self.m_comp_setgui()
        # Elemente für .diff_frame
        self.m_diff_setgui()
        # Beenden()
        self.ob_exit = ttk.Button(
            self.ob_master,
            text="Beenden",
            command=self.ob_master.quit
        )
        self.ob_exit.pack(side=tkinter.RIGHT, padx=5, pady=5)

    def m_gui_update(self):
        '''
        Das gesamte GUI anhand der neuen Werte aktualisieren
        '''
        # Dirs Einträge löschen
        self.m_dirs_delitems()
        # Aktuelle Dirs Einträge hinzufügen
        self.m_dirs_additems()
        # Dirs Progressbar zurückseten
        self.ob_dirs_progr.config(value=0)
        # Comp Einträge löschen
        self.m_comp_delitems()
        # Aktuelle Comp Einträge hinzufügen
        self.m_comp_additems()
        # Comp Progressbar zurückseten
        self.ob_comp_progr.config(value=0)
        # Diff Einträge löschen
        self.m_diff_delitems()
        # Aktuelle Diff Einträge hinzufügen
        self.m_diff_additems()
        # Aktualisiere die Diff Combobox
        self.m_diff_combovalues()

    def m_dirs_setgui(self):
        '''
        Abschnitt Strukturen erassen
         .tx_dirs_id = Id von Dirs
         .dc_dirs_check = check_dirs Resultat Verzeichnis
         .ob_dirs_titel = <ttk.Label>, Titel
         .ob_dirs_table = <ttk.Treeview>, Tabelle
         .ob_dirs_info = <ttk.Button>, Informationen
         .ob_dirs_jsonmake = <ttk.Button>, Json erstellen
         .ob_dirs_jsonopen = <ttk.Button>, Json zeigen
         .ob_dirs_htmlmake = <ttk.Button>, Html erstellen
         .ob_dirs_htmlopen = <ttk.Button>, Html zeigen
         .ob_dirs_update = <ttk.Button>, aktualisieren
        '''
        # Id von Dirs und check_dirs Resultat Verzeichnis
        self.tx_dirs_id = ''
        self.dc_dirs_check = {}
        # Titel
        self.ob_dirs_titel = ttk.Label(
            self.ob_dirs_frm,
            text="Strukturen erfassen"
        )
        # Tabelle
        self.ob_dirs_table = ttk.Treeview(
            self.ob_dirs_frm,
            columns=('#1', '#2', '#3', '#4', '#5'),
            show='headings'
        )
        # Tabelle berschriften
        self.ob_dirs_table.heading('#1', text='ID')
        self.ob_dirs_table.heading('#2', text='JSON-Datei')
        self.ob_dirs_table.heading('#3', text='JSON-Datum')
        self.ob_dirs_table.heading('#4', text='HTML-Datei')
        self.ob_dirs_table.heading('#5', text='HTML-Datum')
        # Tabelle Spaltenbreiten
        self.ob_dirs_table.column('#1', width=INT_DIRS_W1)
        self.ob_dirs_table.column('#2', width=INT_DIRS_W2)
        self.ob_dirs_table.column('#3', width=INT_DIRS_W3)
        self.ob_dirs_table.column('#4', width=INT_DIRS_W4)
        self.ob_dirs_table.column('#5', width=INT_DIRS_W5)
        # Füge Einträge zur Tabelle hinzu
        self.m_dirs_additems()
        # Tabelle Event definieren
        self.ob_dirs_table.bind(
            '<<TreeviewSelect>>',
            self.m_dirs_ontable
        )
        # Info anzeigen
        self.ob_dirs_info = ttk.Button(
            self.ob_dirs_frm,
            text="Informationen",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_oninfo
        )
        # JSON erfassen
        self.ob_dirs_jsonmake = ttk.Button(
            self.ob_dirs_frm,
            text="JSON Erfassen",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_onjsonmake
        )
        # JSON im Dateimanager zeigen
        self.dirs_json_open = ttk.Button(
            self.ob_dirs_frm,
            text="Erfasste JSON Zeigen",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_onjsonopen
        )
        # Erfasste JSON dokumentieren
        self.ob_dirs_htmlmake = ttk.Button(
            self.ob_dirs_frm,
            text="HTML Dokumentation",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_onhtmlmake
        )
        # HTML im Dateimanager zeigen
        self.ob_dirs_htmlopen = ttk.Button(
            self.ob_dirs_frm,
            text="Dokumentationen zeigen",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_onhtmlopen
        )
        # Aktualisiere Tabelle
        self.ob_dirs_update = ttk.Button(
            self.ob_dirs_frm,
            text="Aktualisieren",
            width=DIRS_BUTTON_W,
            command=self.m_dirs_onupdate
        )
        # Fortschrittsanzeige
        self.ob_dirs_progr = ttk.Progressbar(
            self.ob_dirs_frm,
            orient="horizontal",
            mode="determinate",
            value=0,
            maximum=100
        )
        # Grid Layout
        self.ob_dirs_titel.grid(
            column=0, row=0, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_dirs_table.grid(
            column=0, row=1, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_dirs_info.grid(
            column=0, row=2,
            sticky=tkinter.W, padx=10, pady=5
            )
        self.ob_dirs_jsonmake.grid(
            column=1, row=2,
            padx=10, pady=5
            )
        self.dirs_json_open.grid(
            column=2, row=2,
            sticky=tkinter.E, padx=10, pady=5
            )
        self.ob_dirs_update.grid(
            column=0, row=3,
            sticky=tkinter.W, padx=10, pady=5
            )
        self.ob_dirs_htmlmake.grid(
            column=1, row=3,
            padx=10, pady=5
            )
        self.ob_dirs_htmlopen.grid(
            column=2, row=3, columnspan=3,
            sticky=tkinter.E, padx=10, pady=5
            )
        self.ob_dirs_progr.grid(
            column=0, row=4, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )

    def m_dirs_delitems(self):
        '''
        Lösche alle Einträge in .ob_dirs_table
        '''
        for vl_i in self.ob_dirs_table.get_children():
            self.ob_dirs_table.delete(vl_i)

    def m_dirs_additems(self):
        '''
        Füge Einträge zu .ob_dirs_table hinzu
        '''
        # Hole Daten aus pyosv2
        in_log = 0
        # DC_DIRS prüfen, result =
        # {'ID': {'json': [<p>, <v>, <d>], 'html': <p>, [<v>, <d>]}, }
        in_log, self.dc_dirs_check = pyosv2.f_checkdirs(in_log)
        # Daten Tabelle
        ls_d = []
        # Ergebnis Verzeichnis auslesen
        for tx_i in self.dc_dirs_check.keys():
            # Von allen ID die Werte holen
            dc_w = self.m_dirs_chkvalues(tx_i)
            # An Daten Liste anhängen: id_, json, datum, html, datum
            ls_d.append((
                tx_i,
                dc_w['json_pfad'],
                dc_w['json_datum'],
                dc_w['html_pfad'],
                dc_w['html_datum']
            ))
        # Daten der Tabelle hinzufügen
        for vl_w in ls_d:
            self.ob_dirs_table.insert('', tkinter.END, values=vl_w)

    def m_dirs_ontable(self, event):
        '''
        Klick auf Dirs Tabelle
        '''
        for ob_selected in self.ob_dirs_table.selection():
            # dictionary
            ob_i = self.ob_dirs_table.item(ob_selected)
            # list
            vl_w = ob_i['values']
            # ID lesen
            self.tx_dirs_id = str(vl_w[0])

    def m_dirs_oninfo(self):
        '''
        Klick auf Informationen
        '''
        if self.tx_dirs_id:
            # Werte holen
            dc_i = self.m_dirs_chkvalues(self.tx_dirs_id)
            # Info Feld updaten
            tx_m = "".join([
                "ID: ", self.tx_dirs_id, "\n\n",
                "JSON Status: ", str(dc_i['json_status']), "\n\n",
                "JSON PfAD: ", dc_i['json_pfad'], "\n\n",
                "JSON Datum: ", dc_i['json_datum'], "\n\n",
                "HTML Status: ", str(dc_i['html_status']), "\n\n",
                "HTML PfAD: ", dc_i['html_pfad'], "\n\n",
                "HTML Datum: ", dc_i['html_datum'], "\n\n"
            ])
            tx_t = "Detailinformationen"
            vl_v = messagebox.showinfo(message=tx_m, title=tx_t)

    def m_dirs_onjsonmake(self):
        '''
        Klick auf JSON Erstellen
        Anhand von <DC_DIRS> Datei-Strukturen lesen und als
        Json speichern
        '''
        # Initalwert Log
        in_log = 0
        # Initalwerte Prgrogressbar
        in_anz = len(DC_DIRS)
        in_progstep = 100 // in_anz
        in_curr = in_progstep
        for id_, tx_pfade in DC_DIRS.items():
            # Verzeichnis erstellen
            dc_quell = pyosv2.f_verzdirs(tx_pfade[0])
            # Log-Meldung
            in_log = pyosv2.f_log(
                in_log,
                "Quelle gelesen",
                tx_pfade[0]
            )
            # Als JSON speichern
            pyosv2.f_savejson(tx_pfade[1], dc_quell)
            # Log-Meldung
            in_log = pyosv2.f_log(
                in_log,
                "JSON gespeichert",
                tx_pfade[1]
            )
            # Progressbar aktualisieren
            in_curr += in_progstep
            self.ob_dirs_progr.after(
                100,
                self.m_dirs_progress(in_curr)
            )
            self.ob_dirs_progr.update()
        # GUI updaten
        self.m_gui_update()
        # Mitteilung
        tx_m = "Die JSON wurden erfasst"
        tx_t = "Mitteilung"
        vl_v = messagebox.showinfo(message=tx_m, title=tx_t)

    def m_dirs_onjsonopen(self):
        '''
        Klick auf JSON Zeigen
        '''
        if self.tx_dirs_id:
            # Werte holen
            dc_v = self.m_dirs_chkvalues(self.tx_dirs_id)
            # Dateimanager öffnen
            f_filemanager(dc_v['json_pfad'])

    def m_dirs_onhtmlmake(self):
        '''
        Klick auf HTML Dokumentation
        Abgespeicherte Json aus <DC_DIRS> laden und als
        HTML Dokumentation ebenfalls aus <DC_DIRS> speichern.
        '''
        # Initalwert Log
        in_log = 0
        # Initalwerte Prgrogressbar
        in_anz = len(DC_DIRS)
        in_progstep = 100 // in_anz
        in_curr = in_progstep
        for id_, pfade in DC_DIRS.items():
            # Verzeichnis laden
            dc_json = pyosv2.f_loadjson(pfade[1])
            # Log-Meldung
            in_log = pyosv2.f_log(
                in_log,
                "JSON geladen",
                pfade[1]
            )
            # Schön formatierter Text
            html_txt = pyosv2.f_htmldok(dc_json)
            # HTML speichern
            pyosv2.f_savetext(pfade[2], html_txt)
            # Progressbar aktualisieren
            in_curr += in_progstep
            self.ob_dirs_progr.after(
                100,
                self.m_dirs_progress(in_curr)
            )
            self.ob_dirs_progr.update()
        # GUI updaten
        self.m_gui_update()
        # Mitteilung
        tx_m = "Die HTML Dukumentationen wurden erstellt"
        tx_t = "Mitteilung"
        vl_v = messagebox.showinfo(message=tx_m, title=tx_t)

    def m_dirs_onhtmlopen(self):
        '''
        Klick auf HTML Dokumentation
        '''
        if self.tx_dirs_id:
            # Werte holen
            dc_v = self.m_dirs_chkvalues(self.tx_dirs_id)
            # Dateimanager öffnen
            f_filemanager(dc_v['html_pfad'])

    def m_dirs_onupdate(self):
        '''
        Klick auf dirs Update
        '''
        self.m_gui_update()

    def m_dirs_chkvalues(self, tx_id):
        '''
        Holt die Werte aus .dc_dirs_check mit tx_id
        Gibt ein Verzeichnis mit Texten zurück:
        {
            'json_status': True oder False,
            'json_pfad': 'pfad' oder '--',
            'json_datum': 'tt.mm.jjjj' oder '',
            'html_status': True oder False,
            'html_pfad': 'pfad' oder '--',
            'html_datum': 'tt.mm.jjjj' oder '',
        }
        '''
        dc_a = {
            'json_status': False,
            'json_pfad': '--',
            'json_datum': '--',
            'html_status': False,
            'html_pfad': '--',
            'html_datum': '--',
        }
        # Daten lesen
        if tx_id in self.dc_dirs_check.keys():
            # Id ist vorhanden
            dc_v = self.dc_dirs_check[tx_id]
            # Json Status
            dc_a['json_status'] = dc_v['json'][1]
            # Json Pfad
            if dc_a['json_status']:
                dc_a['json_pfad'] = dc_v['json'][0]
            # Json Datum
            if dc_v['json'][2]:
                dc_a['json_datum'] = f_datum_tmj(dc_v['json'][2])
            # Html Status
            dc_a['html_status'] = dc_v['html'][1]
            # Html Pfad
            if dc_a['html_status']:
                dc_a['html_pfad'] = dc_v['html'][0]
            # Html Datum
            if dc_v['html'][2]:
                dc_a['html_datum'] = f_datum_tmj(dc_v['html'][2])
        # Verzeichnis zurückgeben
        return(dc_a)

    def m_dirs_progress(self, in_curr):
        '''
        Fortschritt in .ob_dirs_progr anzeigen
        '''
        self.ob_dirs_progr.config(value=in_curr)

    def m_comp_setgui(self):
        '''
        Abschnitt Strukturen vergleichen
         .tx_comp_id = Id von Dirs
         .dc_comp_check = check_compjson Resultat Verzeichnis
         .ob_comp_titel = <ttk.Label>, Titel
         .ob_comp_table = <ttk.Treeview>, Tabelle mit Ziel / Quelle
         .ob_comp_info = <ttk.Button>, Informationen
         .ob_comp_compare = <ttk.Button>, vergleichen
        '''
        # Id von Comp und check_compjson Resultat Verzeichnis
        self.tx_comp_id = ''
        self.dc_comp_check = {}
        # Titel
        self.ob_comp_titel = ttk.Label(
            self.ob_comp_frm,
            text="Strukturen vergleichen"
        )
        # Tabelle
        self.ob_comp_table = ttk.Treeview(
            self.ob_comp_frm,
            columns=('#1', '#2', '#3', '#4', '#5'),
            show='headings'
        )
        # Tabelle berschriften
        self.ob_comp_table.heading('#1', text='ID')
        self.ob_comp_table.heading('#2', text='Quell-JSON')
        self.ob_comp_table.heading('#3', text='Datum')
        self.ob_comp_table.heading('#4', text='Ziel-JSON')
        self.ob_comp_table.heading('#5', text='Datum')
        # Tabelle Spaltenbreiten
        self.ob_comp_table.column('#1', width=INT_COMP_W1)
        self.ob_comp_table.column('#2', width=INT_COMP_W2)
        self.ob_comp_table.column('#3', width=INT_COMP_W3)
        self.ob_comp_table.column('#4', width=INT_COMP_W4)
        self.ob_comp_table.column('#5', width=INT_COMP_W5)
        # Füge Einträge zur Tabelle hinzu
        self.m_comp_additems()
        # Tabelle Event definieren
        self.ob_comp_table.bind(
            '<<TreeviewSelect>>',
            self.m_comp_ontable
        )
        # Info anzeigen
        self.ob_comp_info = ttk.Button(
            self.ob_comp_frm,
            text="Informationen",
            width=DIRS_BUTTON_W,
            command=self.m_comp_oninfo
        )
        # Vergleiche Json
        self.ob_comp_compare = ttk.Button(
            self.ob_comp_frm,
            text="Vergleichen",
            width=DIRS_BUTTON_W,
            command=self.m_comp_oncompare
        )
        # Fortschrittsanzeige
        self.ob_comp_progr = ttk.Progressbar(
            self.ob_comp_frm,
            orient="horizontal",
            mode="determinate",
            value=0,
            maximum=100
        )
        # Layout mit Grid
        self.ob_comp_titel.grid(
            column=0, row=0, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_comp_table.grid(
            column=0, row=1, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_comp_info.grid(
            column=0, row=2,
            sticky=tkinter.W, padx=10, pady=5
            )
        self.ob_comp_compare.grid(
            column=2, row=2,
            sticky=tkinter.E, padx=10, pady=5
            )
        self.ob_comp_progr.grid(
            column=0, row=3, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )

    def m_comp_delitems(self):
        '''
        Lösche alle Einträge in .ob_comp_table
        '''
        for ob_i in self.ob_comp_table.get_children():
            self.ob_comp_table.delete(ob_i)

    def m_comp_additems(self):
        '''
        Füge Einträge zu .ob_comp_table hinzu
        '''
        # Hole Daten aus pyosv2
        in_log = 0
        # DC_DIRS prüfen, result =
        # {'ID': {'json': [<p>, <v>, <d>], 'html': <p>, [<v>, <d>]}, }
        in_log, self.dc_comp_check = pyosv2.f_checkcomp(in_log)
        # Daten Tabelle
        ls_d = []
        # Ergebnis Verzeichnis auslesen
        for tx_i in self.dc_comp_check.keys():
            # Von allen ID die Werte holen
            dc_v = self.m_comp_chkvalues(tx_i)
            # An Daten Liste anhängen: id_, json, datum, html, datum
            ls_d.append((
                tx_i,
                dc_v['quell_pfad'],
                dc_v['quell_datum'],
                dc_v['ziel_pfad'],
                dc_v['ziel_datum']
            ))
        # Daten der Tabelle hinzufügen
        for tp_i in ls_d:
            self.ob_comp_table.insert('', tkinter.END, values=tp_i)

    def m_comp_chkvalues(self, tx_id):
        '''
        Holt die Werte aus .dc_comp_check mit tx_id
        Gibt ein Verzeichnis mit Texten zurück:
        {
            'quell_status': True oder False,
            'quell_pfad': 'pfad' oder '--',
            'quell_datum': 'tt.mm.jjjj' oder '',
            'ziel_status': True oder False,
            'ziel_pfad': 'pfad' oder '--',
            'ziel_datum': 'tt.mm.jjjj' oder '',
        }
        '''
        dc_a = {
            'quell_status': False,
            'quell_pfad': '--',
            'quell_datum': '--',
            'ziel_status': False,
            'ziel_pfad': '--',
            'ziel_datum': '--',
        }
        # Daten lesen
        if tx_id in self.dc_comp_check.keys():
            # Id ist vorhanden
            dc_v = self.dc_comp_check[tx_id]
            # Status Quelle
            dc_a['quell_status'] = dc_v['quelle'][1]
            # Pfad Quelle
            if dc_a['quell_status']:
                dc_a['quell_pfad'] = dc_v['quelle'][0]
            # Datum Quelle
            if dc_v['quelle'][2]:
                dc_a['quell_datum'] = f_datum_tmj(dc_v['quelle'][2])
            # Status Ziel
            dc_a['ziel_status'] = dc_v['ziel'][1]
            # Pfad Ziel
            if dc_a['ziel_status']:
                dc_a['ziel_pfad'] = dc_v['ziel'][0]
            # Datum Ziel
            if dc_v['ziel'][2]:
                dc_a['ziel_datum'] = f_datum_tmj(dc_v['ziel'][2])
        # Verzeichnis zurückgeben
        return(dc_a)

    def m_comp_ontable(self, event):
        '''
        Klick auf Compjson Tabelle
        '''
        for ob_selected in self.ob_comp_table.selection():
            # dictionary
            ob_i = self.ob_comp_table.item(ob_selected)
            # list
            vl_w = ob_i['values']
            # ID lesen
            self.tx_comp_id = str(vl_w[0])

    def m_comp_oninfo(self):
        '''
        Klick auf Json Informationen
        '''
        if self.tx_comp_id:
            # Werte holen
            dc_i = self.m_comp_chkvalues(self.tx_comp_id)
            # Info Feld updaten
            tx_m = "".join([
                "ID: ", self.tx_dirs_id, "\n\n",
                "Quell-JSON Status: ", str(dc_i['quell_status']),
                "\n\n",
                "Quell-JSON PfAD: ", dc_i['quell_pfad'], "\n\n",
                "Quell-JSON Datum: ", dc_i['quell_datum'], "\n\n",
                "Ziel-JSON Status: ", str(dc_i['ziel_status']), "\n\n",
                "Ziel-JSON PfAD: ", dc_i['ziel_pfad'], "\n\n",
                "Ziel-JSON Datum: ", dc_i['ziel_datum'], "\n\n"
            ])
            tx_t = "Detailinformationen"
            vl_v = messagebox.showinfo(message=tx_m, title=tx_t)

    def m_comp_oncompare(self):
        '''
        Klick auf Json vergleichen
        Die Json Paare, definiert von <DC_COMP> prüfen und die
        Unterschiede als Differenz Json definiert in <DC_COMP>
        speichern
        '''
        # Initalwert Log
        in_log = 0
        # Initalwerte Prgrogressbar
        in_anz = len(DC_COMP)
        in_progstep = 100 // (in_anz * 2)
        in_curr = in_progstep
        # JSON vergleichen
        for tx_id, jsons in DC_COMP.items():
            bl_quell = self.dc_comp_check[tx_id]['quelle'][1]
            bl_ziel = self.dc_comp_check[tx_id]['ziel'][1]
            if bl_quell and bl_ziel:
                # Pfade normalisieren
                tx_quellpfad = os.path.normcase(
                    os.path.normpath(jsons[0])
                )
                tx_zielpfad = os.path.normcase(
                    os.path.normpath(jsons[1])
                )
                tx_diffpfad = os.path.normcase(
                    os.path.normpath(jsons[2])
                )
                # Log-Meldung
                tx_t = "{0} / {1} / {2}".format(
                    os.path.basename(tx_quellpfad),
                    os.path.basename(tx_zielpfad),
                    os.path.basename(tx_diffpfad)
                )
                in_log = pyosv2.f_log(
                    in_log,
                    "Quelle / Ziel / Unterschiede",
                    tx_t
                )
                # Quell Verzeichnis lesen
                dc_quell = pyosv2.f_loadjson(tx_quellpfad)
                # Log-Meldung
                in_log = pyosv2.f_log(
                    in_log,
                    "Quell-JSON gelesen",
                    tx_quellpfad
                )
                # Ziel Verzeichnis lesen
                dc_ziel = pyosv2.f_loadjson(tx_zielpfad)
                # Log-Meldung
                in_log = pyosv2.f_log(
                    in_log,
                    "Ziel-JSON gelesen",
                    tx_zielpfad
                )
                # Progressbar aktualisieren
                in_curr += in_progstep
                self.ob_dirs_progr.after(
                    100,
                    self.m_dirs_progress(in_curr)
                )
                # Unterschiede ermitteln
                dc_diff = pyosv2.f_compverz(
                    dc_quell,
                    dc_ziel
                )
                # Log-Meldung
                in_log = pyosv2.f_log(
                    in_log,
                    "Unterschiede emittelt",
                    dc_diff
                )
                # Unterschiede als JSON speichern
                pyosv2.f_savejson(tx_diffpfad, dc_diff)
                # Log-Meldung
                in_log = pyosv2.f_log(
                    in_log,
                    "Diff-JSON gespeichert",
                    tx_diffpfad
                )
                # Progressbar aktualisieren
                in_curr += in_progstep
                self.ob_dirs_progr.after(
                    100,
                    self.m_dirs_progress(in_curr)
                )
            else:
                in_log = pyosv2.f_log(
                    in_log,
                    "Nicht alle JSON vorhanden",
                    tx_id
                )
                # Progressbar aktualisieren
                in_curr += (in_progstep * 2)
                self.ob_dirs_progr.after(
                    100,
                    self.m_dirs_progress(in_curr)
                )
        # Aktualisieren
        self.m_gui_update()
        # Mitteilung
        tx_m = "Die Strukturen wurden verglichen"
        tx_t = "Mitteilung"
        vl_v = messagebox.showinfo(message=tx_m, title=tx_t)

    def m_comp_progress(self, in_curr):
        '''
        Fortschritt in .ob_comp_progr anzeigen
        '''
        self.ob_comp_progr.config(value=in_curr)

    def m_diff_setgui(self):
        '''
        Abschnitt Strukturvergleiche prüfen
         .tx_diff_tableid = Id vom Eintrag der Tabelle
         .tx_diff_comboid = Id von Eintrag der Combobox
         .dc_diff_check = check_diffjson Resultat Verzeichnis
         .ls_diff_combo = Liste mit Einträgen für die Json-Wahl
         .dc_diff_combo = Paarung Eintrag Json-Wahl und Prüf-ID
         .dc_diff_table_info = Tabelleneinträge gepaart mit Informat.
         .ob_diff_titel = <ttk.Label>, Titel
         .ob_diff_combo = <ttk.Combobox>, Unterschiede JSON auswählen
         .ob_diff_datum = <ttk.Label>, Datum
         .ob_diff_quelle = <ttk.Label>, Quellpfad
         .ob_diff_ziel = <ttk.Label>, Zielpfad
         .ob_diff_var_datum = <tkinter.StringVar>, Inhalt Datum
         .ob_diff_var_quelle = <tkinter.StringVar>, Inhalt Quellpfad
         .ob_diff_var_ziel = <tkinter.StringVar>, Inhalt Zielpfad
         .ob_diff_table = <ttk.Treeview>, Tabelle mit Unterschieden
         .ob_diff_open = <ttk.Button>, Dateimanager öffnen
        '''
        # Id von Comp und check_compjson Resultat Verzeichnis
        self.tx_diff_tableid = ''
        self.tx_diff_comboid = ''
        self.dc_diff_check = {}
        # Combobox Einträge und Paarung mit Prüf-ID
        self.ls_diff_combo = []
        self.dc_diff_combo = {}
        # Titel
        self.ob_diff_titel = ttk.Label(
            self.ob_diff_frm,
            text="Struktur-Unterschiede prüfen"
        )
        # Combobox
        self.ob_diff_combo = ttk.Combobox(self.ob_diff_frm)
        self.ob_diff_combo.bind(
            "<<ComboboxSelected>>",
            self.m_diff_oncombo
        )
        # Weise die Unterschiede Json der Combobox zu
        self.m_diff_combovalues()
        # Datum
        self.ob_diff_var_datum = tkinter.StringVar()
        self.ob_diff_datum = ttk.Label(
            self.ob_diff_frm,
            textvariable=self.ob_diff_var_datum
        )
        # Quellpfad
        self.ob_diff_var_quelle = tkinter.StringVar()
        self.ob_diff_quelle = ttk.Label(
            self.ob_diff_frm,
            textvariable=self.ob_diff_var_quelle
        )
        # Zielpfad
        self.ob_diff_var_ziel = tkinter.StringVar()
        self.ob_diff_ziel = ttk.Label(
            self.ob_diff_frm,
            textvariable=self.ob_diff_var_ziel
        )
        # Tabelle
        self.ob_diff_table = ttk.Treeview(
            self.ob_diff_frm,
            columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8'),
            show='headings'
        )
        # Tabelle berschriften
        self.ob_diff_table.heading('#1', text='ID')
        self.ob_diff_table.heading('#2', text='Pfad')
        self.ob_diff_table.heading('#3', text='Zuviel')
        self.ob_diff_table.heading('#4', text='Fehlt')
        self.ob_diff_table.heading('#5', text='Neuer')
        self.ob_diff_table.heading('#6', text='Älter')
        self.ob_diff_table.heading('#7', text='Grösser')
        self.ob_diff_table.heading('#8', text='Kleiner')
        # Tabelle Spaltenbreiten
        self.ob_diff_table.column('#1', width=INT_DIFF_W1)
        self.ob_diff_table.column('#2', width=INT_DIFF_W2)
        self.ob_diff_table.column('#3', width=INT_DIFF_W3)
        self.ob_diff_table.column('#4', width=INT_DIFF_W4)
        self.ob_diff_table.column('#5', width=INT_DIFF_W5)
        self.ob_diff_table.column('#6', width=INT_DIFF_W6)
        self.ob_diff_table.column('#7', width=INT_DIFF_W7)
        self.ob_diff_table.column('#8', width=INT_DIFF_W8)
        # Daten hinzufügen
        self.m_diff_additems()
        # Tabelle Event definieren
        self.ob_diff_table.bind(
            '<<TreeviewSelect>>',
            self.m_diff_ontable
        )
        # Dateimanager öffnen
        self.ob_diff_open = ttk.Button(
            self.ob_diff_frm,
            text="Quelle / Ziel öffnen",
            width=DIRS_BUTTON_W,
            command=self.m_diff_onopen
        )
        # Layout mit Grid
        self.ob_diff_titel.grid(
            column=0, row=0, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_combo.grid(
            column=0, row=1,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_datum.grid(
            column=2, row=1,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_quelle.grid(
            column=0, row=2,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_ziel.grid(
            column=2, row=2,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_table.grid(
            column=0, row=3, columnspan=3,
            sticky=tkinter.EW, padx=10, pady=5
            )
        self.ob_diff_open.grid(
            column=2, row=4,
            sticky=tkinter.E, padx=10, pady=5
            )

    def m_diff_delitems(self):
        '''
        Lösche alle Einträge in .ob_dirs_table
        Setze die Einträge von .ob_diff_var_datum, .ob_diff_var_quelle,
        .ob_diff_var_ziel zurück
        '''
        # Tabelle löschen
        for ob_i in self.ob_diff_table.get_children():
            self.ob_diff_table.delete(ob_i)
        # Informationen zurücksetzen
        self.ob_diff_var_datum.set("--")
        self.ob_diff_var_quelle.set("--")
        self.ob_diff_var_ziel.set("--")

    def m_diff_additems(self):
        '''
        Füge Einträge zu .ob_diff_table hinzu
        Aktualisiere die Inhalte von .ob_diff_var_datum,
        .ob_diff_var_quelle, .ob_diff_var_ziel

        Json Unterschiede = {'datum': 'jjjj-mm-tt',
            'quellstamm': 'pfad', 'zielstamm': 'pfad',
            'unterschiede': {'sub-pfad': {'name': (
                    'True/False', 'jjjj-mm-tt HH:MM:SS', grösse,
                    'True/False', 'jjjj-mm-tt HH:MM:SS', grösse
            )}, }}

        Tabelle:
        ID | Pfad | Zuviel | Fehlt | Neuer | Älter | Grösser | Kleiner

        .dc_diff_table_info = {"###1":
            ("quellstamm/subpfad", "zielstamm/subpfad"), }
        '''
        # Tabelle löschen, Infos zurücksetzen
        self.m_diff_delitems()
        if self.tx_diff_comboid:
            # Es wurde ein json Eintrag angewählt
            tx_pfad = self.dc_diff_check[self.tx_diff_comboid][0]
            dc_json = pyosv2.f_loadjson(tx_pfad)
            # Informationen
            tx_d = "Datum: {0}".format(f_datum_tmj(dc_json['datum']))
            tx_q = "Quelle: {0}".format(dc_json['quellstamm'])
            tx_z = "Ziel: {0}".format(dc_json['zielstamm'])
            if len(tx_q) > INT_DIFF_MAX_PFAD:
                tx_q = tx_q[len(tx_q) - INT_DIFF_MAX_PFAD - 2:]
                tx_q = "..{0}".format(tx_q)
            if len(tx_z) > INT_DIFF_MAX_PFAD:
                tx_z = tx_z[len(tx_z) - INT_DIFF_MAX_PFAD - 2:]
                tx_z = "..{0}".format(tx_z)
            self.ob_diff_var_datum.set(tx_d)
            self.ob_diff_var_quelle.set(tx_q)
            self.ob_diff_var_ziel.set(tx_z)
            # Unterschiede lesen
            dc_diff = dc_json['unterschiede']
            in_id = 0
            # Verzeichnis und Liste bilden
            self.dc_diff_table_info = {}
            ls_d = []
            # Verzeichnisse auslesen
            for tx_subpfad, dc_info in dc_diff.items():
                # Zähler initieren
                in_zuviel = 0
                in_fehlt = 0
                in_neuer = 0
                in_aelter = 0
                in_groesser = 0
                in_kleiner = 0
                # Text-ID bilden
                tx_id = str(in_id)
                tx_id = tx_id.rjust(4, "#")
                # Daeien auslesen
                for tx_name, tp_i in dc_info.items():
                    # Infos lesen
                    bl_status_quell = tp_i[0]
                    tx_datum_quell = tp_i[1]
                    in_groesse_quell = tp_i[2]
                    bl_status_ziel = tp_i[3]
                    tx_datum_ziel = tp_i[4]
                    in_groesse_ziel = tp_i[5]
                    # Status vergleichen
                    if bl_status_ziel and not bl_status_quell:
                        # In Ziel vorhanden aber nicht in Quelle
                        in_zuviel += 1
                    elif not bl_status_ziel and bl_status_quell:
                        # Nicht in Ziel vorhanden aber in Quelle
                        in_fehlt += 1
                    # Datum vergleichen
                    if not tx_datum_ziel or not tx_datum_quell:
                        # Mind. ein Datum fehlt
                        pass
                    elif tx_datum_ziel > tx_datum_quell:
                        # Im Ziel neuer als in Quelle
                        in_neuer += 1
                    elif tx_datum_ziel < tx_datum_quell:
                        # In Ziel älter als in Quelle
                        in_aelter += 1
                    # Grösse vergleichen
                    if not in_groesse_ziel or not in_groesse_quell:
                        # Mind. eine Grösse fehlt
                        pass
                    elif in_groesse_ziel > in_groesse_quell:
                        # In Ziel grösser als in Quelle
                        in_groesser += 1
                    elif in_groesse_ziel < in_groesse_quell:
                        # In Ziel kleiner als in Quelle
                        in_kleiner += 1
                # Eintrag zu Liste hinzufügen
                ls_d.append((
                    tx_id,
                    tx_subpfad,
                    '  {0}'.format(str(in_zuviel)),
                    '  {0}'.format(str(in_fehlt)),
                    '  {0}'.format(str(in_neuer)),
                    '  {0}'.format(str(in_aelter)),
                    '  {0}'.format(str(in_groesser)),
                    '  {0}'.format(str(in_kleiner))
                    ))
                # Pfade in Verzeichnis einfügen
                tx_quellpfad = os.path.join(
                    dc_json['quellstamm'],
                    tx_subpfad
                )
                tx_zielpfad = os.path.join(
                    dc_json['zielstamm'],
                    tx_subpfad
                )
                self.dc_diff_table_info[tx_id] = (
                    tx_quellpfad,
                    tx_zielpfad
                )
                # ID hochzählen
                in_id += 1
            # Daten der Tabelle hinzufügen
            for tp_i in ls_d:
                self.ob_diff_table.insert('', tkinter.END, values=tp_i)

    def m_diff_combovalues(self):
        '''
        Holt die Werte für die Verzeichnisse der Unterschiede aus
        DC_COMP und bereite die Daten für .ob_diff_combo auf.
        .ls_diff_combo = ['ID: name.json (Datum)', ]
        .dc_diff_combo = {'ID: name.json (Datum)': 'Prüf-ID', }
        .dc_diff_check =
            {'ID': ['pfad', True/False, 'jjjj-mm-tt HH:MM:SS'], }
        '''
        # Hole Daten aus pyosv2
        in_log = 0
        # DC_COMP prüfen, result =
        # {'ID': ['pfad', True/False, 'jjjj-mm-tt HH:MM:SS'], }
        in_log, self.dc_diff_check = pyosv2.f_checkdiff(in_log)
        # Starteintrag definieren
        self.ls_diff_combo = ["---"]
        self.dc_diff_combo["---"] = ''
        # Daten aufbereiten
        for tx_id, tp_w in self.dc_diff_check.items():
            if tp_w[1]:
                # Json vorhanden
                tx_pfad = os.path.normcase(os.path.normpath(tp_w[0]))
                tx_t = "{0}: {1} ({2})".format(
                    tx_id,
                    tx_pfad,
                    f_datum_tmj(tp_w[2])
                )
                self.ls_diff_combo.append(tx_t)
                self.dc_diff_combo[tx_t] = tx_id
        # Weise die Werte der Combobox zu
        self.ob_diff_combo.config(values=self.ls_diff_combo)
        self.ob_diff_combo.current(0)

    def m_diff_ontable(self, event):
        '''
        Klick auf Unterschied Tabelle
        '''
        for ob_selected in self.ob_diff_table.selection():
            # dictionary
            ob_i = self.ob_diff_table.item(ob_selected)
            # list
            vl_w = ob_i['values']
            # ID lesen
            self.tx_diff_tableid = vl_w[0]
        # print("ID", self.tx_diff_tableid)

    def m_diff_oncombo(self, event):
        '''
        Klick auf die Combobox
        '''
        tx_i = self.ob_diff_combo.get()
        self.tx_diff_comboid = self.dc_diff_combo[tx_i]
        self.m_diff_additems()
        self.tx_diff_tableid = ''

    def m_diff_onopen(self):
        '''
        Klick auf Dateimanager öffnen
        '''
        print("m_diff_onopen")
        if self.tx_diff_tableid:
            # Subpfad holen
            tx_z = self.dc_diff_table_info[self.tx_diff_tableid][1]
            tx_q = self.dc_diff_table_info[self.tx_diff_tableid][0]
            # Dateimanager öffnen
            f_filemanager(tx_q)
            f_filemanager(tx_z)


if __name__ == '__main__':
    '''

    Programmablauf
    --------------
    tkinter.Tk
    GuiOsTools
        __init__
        m_dirs_setgui
            m_dirs_additems
                pyosv2.f_checkdirs
                m_dirs_chkvalues
        m_comp_setgui
            m_comp_additems
                pyosv2.f_checkcomp
                m_comp_chkvalues
        m_diff_setgui
            m_diff_additems
                pyosv2.f_checkdiff
    mainloop()

        m_dirs_onhtmlmake
            pyosv2.f_loadjson
            pyosv2.f_log
            pyosv2.f_htmldok
            pyosv2.f_savetext
            m_gui_update
                m_dirs_delitems
                m_dirs_additems
                    m_dirs_chkvalues
                m_comp_delitems
                m_comp_additems
                    m_comp_chkvalues

        m_dirs_onhtmlopen
           m_dirs_chkvalues

        m_dirs_oninfo
            m_dirs_chkvalues

        m_dirs_onjsonmake
            pyosv2.f_verzdirs
            pyosv2.f_log
            pyosv2.f_savejson
            pyosv2.f_log
            m_gui_update
                m_dirs_delitems
                m_dirs_additems
                    m_dirs_chkvalues
                m_comp_delitems
                m_comp_additems
                    m_comp_chkvalues

        m_dirs_onjsonopen
            m_dirs_chkvalues

        m_dirs_ontable

        m_dirs_onupdate
            m_gui_update
                m_dirs_delitems
                m_dirs_additems
                    m_dirs_chkvalues
                m_comp_delitems
                m_comp_additems
                    m_comp_chkvalues

        m_comp_oncompare
            pyosv2.f_log
            pyosv2.f_loadjson
            pyosv2.f_log
            pyosv2.f_loadjson
            pyosv2.f_log
            pyosv2.f_compverz
            pyosv2.f_log
            pyosv2.f_savejson
            pyosv2.f_log

        m_comp_oninfo
            m_comp_chkvalues

        m_comp_ontable

    Konvention
    ----------
    KONSTANTE
    f_funktion
    Objekt
    m_methode
    in_integer
    fl_float
    tx_text
    dc_dictionairy
    mn_menge
    ls_liste
    ob_objekt
    vl_werte
    bl_bool
    tp_tuple

    '''
    ob_root = tkinter.Tk()
    ob_gui = GuiOsTools(ob_root)
    ob_root.mainloop()
