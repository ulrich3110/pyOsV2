#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import json
import tkinter
from einstPyOsV2 import *

'''
pyosv2.py - Dokumentation und Kontrolle von Datei-Strukturen
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


def f_log(in_nr, tx_t, vl_w):
    '''
    Gibt auf dem Bildschirm eine Nachricht mit fortlaufender Nummer,
    einem Text und dem Wert aus. Am Ende wird die Nummer zurück gegeben.
    '''
    # Nummer hochzählen
    in_nr += 1
    # Text mit vorangestellter Hex-Dez Nummber ausgeben
    tx_wert = str(vl_w)
    if len(tx_wert) > IN_LOGLEN:
        tx_wert = "{}..".format(tx_wert[:IN_LOGLEN])
    print("# {0:X} - {1} - {2} #".format(
        in_nr,
        tx_t,
        tx_wert))
    # Nummer zurückgeben
    return(in_nr)


def f_savejson(tx_pfad, dc_verz):
    '''
    Schreibe Verzeichnis <dc_verz> als JSON Datei mit <tx_pfad>
    '''
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    try:
        with open(tx_pfad, 'w', encoding='utf-8',
                  errors='ignore') as ob_jsonfile:
            json.dump(dc_verz, ob_jsonfile)
    except Exception as ob_err:
        # Fehlermeldung erzeugen und als Error Text Datei speichern
        dc_err = {
            'TITEL': "Fehler",
            'PFAD': tx_pfad,
            'ERROR': str(ob_err)
        }
        with open(tx_pfad, 'w') as ob_errfile:
            json.dump(dc_err, ob_errfile)


def f_loadjson(tx_pfad):
    '''
    Lade eine JSON Datei mit <tx_pfad> und gib diese zurück als <dc_verz>
    '''
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    try:
        with open(tx_pfad) as ob_f:
            dc_verz = json.load(ob_f)
    except Exception as ob_err:
        # Fehlermeldung ausgeben und leeres Verzeichnis erzeugen
        tx_t = "# FEHLER ## PFAD: {0} ## Error: {1} #".format(
            tx_pfad,
            str(ob_err)
        )
        print(tx_t)
        dc_verz = {}
    return(dc_verz)


def f_savetext(tx_pfad, tx_text):
    '''
    Speichert den <tx_text> beim <tx_pfad> ab.
    '''
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    try:
        ob_datei = open(
            tx_pfad,
            'w',
            encoding='utf-8',
            errors='ignore'
        )
        ob_datei.write(tx_text)
        ob_datei.close()
    except Exception as ob_err:
        tx_t = "# FEHLER ## PFAD: {0} ## Error: {1} #".format(
            tx_pfad,
            str(ob_err)
        )
        tx_errpfad = "{0}___error.txt".format(tx_pfad)
        ob_errfile = open(tx_errpfad, 'w')
        ob_errfile.write(tx_t)
        ob_errfile.close()


def f_ausnahme(tx_name):
    '''
    Prüft ob die Datei zu den Ausnahmen gehört.
    Gibt True oder False zurück.
    '''
    bl_ausn = False
    if tx_name in LS_AUSNAHMEN:
        # In der Auswahlliste enthalten
        bl_ausn = True
    if not bl_ausn:
        # Noch keine Ausnahme
        for i in LS_AUSN_START:
            if tx_name.startswith(i):
                # In den Ausnahmen für Dateianfang enthalten
                bl_ausn = True
                break
    if not bl_ausn:
        # Noch keine Ausnahme
        for i in LS_AUSN_ENDE:
            if tx_name.endswith(i):
                # In den Ausnahmen für Dateiende enthalten
                bl_ausn = True
                break
    return(bl_ausn)


def f_verzdirs(tx_stamm):
    '''
    Mit os.walk() das aktuelle Verzeichnis und alle Unterverzeichnisse
    durchsuchen. Das Ergbnis in der Verzeichnis-Liste und der
    Datei-Liste zurückgeben.
      tx_pfad = 'pfad'
      dc_dirs = {
        'datum': 'jjjj-mm-tt HH:MM:SS',     # Datum / Zeit
        'stamm': 'pfad',                    # Absoluer Pfad
        'dateien': {
            'sub-pfad': {                   # Ralativer Pfad zu 'stamm'
                'name': (                   # Dateiname inkl. Erweiterung
                    'jjjj-mm-tt HH:MM:SS',  # Datum / Zeit
                    grösse                  # Grösse in Bytes
                )
            },
        }
      }
    '''
    ls_datei = []
    ls_verzeichn = []
    tx_stamm = os.path.normcase(os.path.normpath(tx_stamm))
    for tx_root, ob_dirs, ob_files in os.walk(tx_stamm, topdown=False):
        for tx_name in ob_files:
            ls_datei.append(os.path.join(tx_root, tx_name))
        for tx_name in ob_dirs:
            ls_verzeichn.append(os.path.join(tx_root, tx_name))
    # dc_dirs bilden
    tx_datum = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    tx_absstamm = os.path.abspath(tx_stamm)
    dc_dirs = {'datum': tx_datum, 'stamm': tx_absstamm, 'dateien': {}}
    for tx_i in ls_datei:
        if os.path.isfile(tx_i):
            # Das Element ist eine Datei
            # Datum lesen
            ob_datum = os.path.getmtime(tx_i)
            tx_datum = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(ob_datum)
            )
            # Grösse lesen
            in_groe = os.path.getsize(tx_i)
            # Dateiname
            tx_name = os.path.normcase(os.path.basename(tx_i))
            # Pfad
            tx_pfad = os.path.normcase(os.path.dirname(tx_i))
            # Relativer Pfad zu Stamm
            tx_rel = tx_pfad.replace(tx_absstamm, '.')
            tx_rel = os.path.normcase(os.path.normpath(tx_rel))
            if tx_rel not in dc_dirs['dateien'].keys():
                # Relativer Pfad noch nicht vorhanden
                dc_dirs['dateien'][tx_rel] = {
                    tx_name: (tx_datum, in_groe)
                }
            else:
                # Relativer Pfad bereits vorhanden
                dc_dirs['dateien'][tx_rel][tx_name] = (
                    tx_datum,
                    in_groe
                )
    # dc_dirs zurückgeben
    return(dc_dirs)


def f_compverz(dc_quell, dc_ziel):
    '''
    Vergleicht das Ziel-Verzeichnis mit dem Quell-Verzeichnis
    und gibt die Unterschiede in einem Verzeichnis zurück.
    - dc_quell / dc_ziel = <f_verzdirs()>
    - dc_untersch = {
        'datum': 'jjjj-mm-tt',              # Datum / Zeit
        'quellstamm': 'pfad',               # Absoluter Pfad
        'zielstamm': 'pfad',                # Absoluter Pfad
        'unterschiede': {
            'sub-pfad': {
                'name': (                   # Dateiname inkl. Erweiter.
                    'True/False',           # In der Quelle vorhanden
                    'jjjj-mm-tt HH:MM:SS',  # Datum / Zeit Quelle
                    grösse,                 # Grösse Quelle in Bytes
                    'True/False',           # Im Ziel vorhanden
                    'jjjj-mm-tt HH:MM:SS',  # Datum / Zeit Ziel
                    grösse                  # Grösse Ziel in Bytes
                )
            },
        }
      }
    '''
    # dc_untersch bilden
    tx_datum = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    dc_untersch = {
        'datum': tx_datum,
        'quellstamm': dc_quell['stamm'],
        'zielstamm': dc_ziel['stamm'],
        'unterschiede': {}
    }
    # Menge bilden mit den Zieldateien
    mn_ziel = set()
    for tx_subpfad, dc_dateien in dc_ziel['dateien'].items():
        for tx_name in dc_dateien.keys():
            # Ausnahmen prüfen
            if not f_ausnahme(tx_name):
                # Jede einzelne Datei mit relativem Pfad hinzufügen
                mn_ziel.add(os.path.join(tx_subpfad, tx_name))
    # Menge bilden mit den Quelldatein
    mn_quelle = set()
    for tx_subpfad, dc_dateien in dc_quell['dateien'].items():
        for tx_name in dc_dateien.keys():
            # Ausnahmen prüfen
            if not f_ausnahme(tx_name):
                # Jede einzelne Datei mit relativem Pfad hinzufügen
                mn_quelle.add(os.path.join(tx_subpfad, tx_name))
    # nicht vorhandene Dateien im Ziel Verzeichnis
    mn_nicht_ziel = mn_quelle - mn_ziel
    # zuviel vorhandene Dateien im Ziel Verzeichnis
    mn_zuviel_ziel = mn_ziel - mn_quelle
    # vorhandene Dateien mit unterschiedlichen Informationen
    gemeinsam = mn_quelle & mn_ziel
    # Unterschriebe ausgeben
    # Nicht im Ziel vorhanden
    for tx_i in mn_nicht_ziel:
        # Dateiname und relaitver Pfad
        tx_verz = os.path.dirname(tx_i)
        tx_name = os.path.basename(tx_i)
        # Datum und Grösse der Quelle
        tx_datum = dc_quell['dateien'][tx_verz][tx_name][0]
        in_groe = dc_quell['dateien'][tx_verz][tx_name][1]
        # Informationen:
        # in Qelle, Grösse, Datum, in Ziel, Grösse, Datum
        tp_info = (True, tx_datum, in_groe, False, None, None)
        if tx_verz not in dc_untersch['unterschiede'].keys():
            # Relativer Pfad noch nicht vorhanden
            dc_untersch['unterschiede'][tx_verz] = {tx_name: tp_info}
        else:
            # Relativer Pfad bereits vorhanden
            dc_untersch['unterschiede'][tx_verz][tx_name] = tp_info
    # Zuviel im Ziel vorhanden
    for tx_i in mn_zuviel_ziel:
        # Dateiname und relaitver Pfad
        tx_verz = os.path.dirname(tx_i)
        tx_name = os.path.basename(tx_i)
        # Datum und Grösse des Ziels
        tx_datum = dc_ziel['dateien'][tx_verz][tx_name][0]
        in_groe = dc_ziel['dateien'][tx_verz][tx_name][1]
        # Informationen:
        # in Qelle, Grösse, Datum, in Ziel, Grösse, Datum
        tp_info = (False, None, None, True, tx_datum, in_groe)
        if tx_verz not in dc_untersch['unterschiede'].keys():
            # Relativer Pfad noch nicht vorhanden
            dc_untersch['unterschiede'][tx_verz] = {tx_name: tp_info}
        else:
            # Relativer Pfad bereits vorhanden
            dc_untersch['unterschiede'][tx_verz][tx_name] = tp_info
    # Gemeinsame Dateien
    for i in gemeinsam:
        tx_verz = os.path.dirname(i)
        tx_name = os.path.basename(i)
        # Datum und Grösse der Quelle
        tx_qdatum = dc_quell['dateien'][tx_verz][tx_name][0]
        tx_qgroe = dc_quell['dateien'][tx_verz][tx_name][1]
        # Datum und Grösse des Ziels
        tx_zdatum = dc_ziel['dateien'][tx_verz][tx_name][0]
        tx_zgroe = dc_ziel['dateien'][tx_verz][tx_name][1]
        # Prüfen auf Unterschiede:
        if tx_qdatum != tx_zdatum or tx_qgroe != tx_zgroe:
            # Informationen:
            # in Qelle, Grösse, Datum, in Ziel, Grösse, Datum
            tp_info = (
                True, tx_qdatum, tx_qgroe, True, tx_zdatum, tx_zgroe
            )
            if tx_verz not in dc_untersch['unterschiede'].keys():
                # Relativer Pfad noch nicht vorhanden
                dc_untersch['unterschiede'][tx_verz] = {
                    tx_name: tp_info
                }
            else:
                # Relativer Pfad bereits vorhanden
                dc_untersch['unterschiede'][tx_verz][tx_name] = tp_info
    # Unterschiede zurückgeben
    return(dc_untersch)


def f_makejson(in_log):
    '''
    Anhand von <DC_DIRS> Datei-Strukturen lesen und als Json speichern
      in_log = Variable für Log Meldungen
    '''
    for tx_id, tp_pfade in DC_DIRS.items():
        # Verzeicnis erstellen
        dc_quell = f_verzdirs(tp_pfade[0])
        # Log-Meldung
        in_log = f_log(in_log, "Quelle gelesen", tp_pfade[0])
        # Als JSON speichern
        f_savejson(tp_pfade[1], dc_quell)
        # Log-Meldung
        in_log = f_log(in_log, "JSON gespeichert", tp_pfade[1])
    return(in_log)


def f_showjson(in_log):
    '''
    Abgespeicherte Json aus <DC_DIRS> laden und anzeigen
      in_log = Variable für Log Meldungen
    '''
    for tx_id, tp_pfade in DC_DIRS.items():
        # Verzeichnis laden
        dc_json = f_loadjson(tp_pfade[1])
        # Log-Meldung
        in_log = f_log(in_log, "JSON geladen", tp_pfade[1])
        # Schön formatierter Text
        tx_text = json.dumps(dc_json, indent=2, sort_keys=True)
        # Bildschirmausgabe
        tx_titel = "{0}: {1}".format(tx_id, tp_pfade[1])
        tx_linie = "-" * len(tx_titel)
        print(tx_titel.upper())
        print(tx_linie)
        print(tx_text)
        # Taste
        tx_input = input("Bitte [Enter] drücken ..")
        print("\n")
    return(in_log)


def f_checkcomp(in_log):
    '''
    Die JSON Quell- und Ziel Dateiverzeichnisse von <DC_COMP>
    prüfen und das Resultat zurückgeben als Verzeichnis:
      {'ID': {'quelle': [<p>, <v>, <d>], 'ziel': <p>, [<v>, <d>]}, }
      ID = Id für die Paarung von Quelle und Ziel
      <p> = pfad/name.json
      <v> = True / False
      <d> = Datumtext ('jjjj-mm-tt HH:MM:SS')
    '''
    # Resultat Verzeichnis erstellen
    dc_result = {}
    for tx_id, tp_json in DC_COMP.items():
        # Pfade normalisieren
        tx_quellpfad = os.path.normcase(os.path.normpath(tp_json[0]))
        tx_zielpfad = os.path.normcase(os.path.normpath(tp_json[1]))
        # Log-Meldung
        tx_text = "{0} / {1}".format(
            os.path.basename(tx_quellpfad),
            os.path.basename(tx_zielpfad)
        )
        in_log = f_log(in_log, "Zu prüfende JSON", tx_text)
        # Prüf Verzeichnis erstellen
        dc_pruef = {'quelle': tx_quellpfad, 'ziel': tx_zielpfad}
        # Temporäres Verzeichnis für die Ergebnisse
        dc_temp = {
            'quelle': [tx_quellpfad, None, None],
            'ziel': [tx_zielpfad, None, None]}
        # Jsons prüfen
        for tx_pruefid, tx_jsonpfad in dc_pruef.items():
            tx_jsonpfad = tx_jsonpfad.lower()
            if (os.path.isfile(tx_jsonpfad) and
               tx_jsonpfad.endswith(".json")):
                # Scheint eine Json Datei zu sein, Json laden
                dc_json = f_loadjson(tx_jsonpfad)
                # Datum lesen
                if 'datum' in dc_json.keys():
                    # Alles gelesen OK
                    dc_temp[tx_pruefid][1] = True
                    dc_temp[tx_pruefid][2] = dc_json['datum']
                else:
                    # Probleme, nicht OK
                    dc_temp[tx_pruefid][1] = False
                    dc_temp[tx_pruefid][2] = ''
            else:
                # Scheint keine Json Datei zu sein
                dc_temp[tx_pruefid][1] = False
                dc_temp[tx_pruefid][2] = ''
        # Ergebnis dem Resultat Verzeichnis hinzufügen
        dc_result[tx_id] = dc_temp
        # Log-Meldung
        in_log = f_log(in_log, "Ergebnis", dc_result)
    # Resultat Verzeichnis zurückgeben
    return(in_log, dc_result)


def f_makecomp(in_log):
    '''
    Die JSON Paare, definiert von <DC_COMP> prüfen und die
    Unterschiede als Differenz JSON definiert in <DC_COMP> speichern
    '''
    # JSON prüfen
    # {'ID': {'quelle': [<v>, <d>], 'ziel': [<v>, <d>]}, }
    in_log, dc_result = f_checkcomp(in_log)
    in_log = f_log(in_log, "Json geprüft", dc_result)
    # JSON vergleichen
    for tx_id, tp_json in DC_COMP.items():
        quell_status = dc_result[tx_id]['quelle'][1]
        ziel_status = dc_result[tx_id]['ziel'][1]
        if quell_status and ziel_status:
            # Pfade normalisieren
            tx_quellpfad = os.path.normcase(
                os.path.normpath(tp_json[0])
            )
            tx_zielpfad = os.path.normcase(
                os.path.normpath(tp_json[1])
            )
            tx_diffpfad = os.path.normcase(
                os.path.normpath(tp_json[2])
            )
            # Log-Meldung
            tx_text = "{0} / {1} / {2}".format(
                os.path.basename(tx_quellpfad),
                os.path.basename(tx_zielpfad),
                os.path.basename(tx_diffpfad)
            )
            in_log = f_log(
                in_log,
                "Quelle / Ziel / Unterschiede",
                tx_text
            )
            # Quell Verzeichnis lesen
            dc_quell = f_loadjson(tx_quellpfad)
            # Log-Meldung
            in_log = f_log(in_log, "Quell-JSON gelesen", tx_quellpfad)
            # Ziel Verzeichnis lesen
            dc_ziel = f_loadjson(tx_zielpfad)
            # Log-Meldung
            in_log = f_log(in_log, "Ziel-JSON gelesen", tx_zielpfad)
            # Unterschiede ermitteln
            dc_diff = f_compverz(dc_quell, dc_ziel)
            # Log-Meldung
            in_log = f_log(in_log, "Unterschiede emittelt", dc_diff)
            # Unterschiede als JSON speichern
            f_savejson(tx_diffpfad, dc_diff)
            # Log-Meldung
            in_log = f_log(in_log, "Diff-JSON gespeichert", tx_diffpfad)
        else:
            in_log = f_log(
                in_log,
                "Nicht alle JSON vorhanden",
                tx_id
            )
    return(in_log)


def f_htmldok(dc_verz):
    '''
    Erstellt aus dem Datei-Verzeichnis ein HTML Dokument als Text
      dc_verz = <f_verzdirs>
      html_txt = HTML Text
    '''
    # Head
    html_txt = "".join([
        '<!DOCTYPE html><html>',
        '<head>',
        '<style>th, td {padding: 3px;}',
        '#left {text-align: left;}',
        '#right {text-align: right;}</style>',
        '</head>'
    ])
    # Body, Überschrift, Pfad, Datum
    html_txt = "".join([
        html_txt,
        '<body>',
        '<h1>Dateistruktur: ', dc_verz['stamm'], '</h1>',
        '<p>Datum: ', dc_verz['datum'], '</p>'
    ])
    # Verzeichnisse, Dateien mit Informationen auflisten
    for tx_pfad, dateien in dc_verz['dateien'].items():
        # Relativer Pfad und Datei-Verzeichnis
        html_txt = "".join([
            html_txt,
            '<br><h3>Verzeichnis: ', tx_pfad, '</h3>',
            '<table><tr>',
            '<th id="left">Dateiname</th>',
            '<th id="left"><small>Datum/Uhrzeit</small></th>',
            '<th id="right"><small>Grösse (bytes)</small></th>',
            '</tr>'
        ])
        for tx_name, inf in dateien.items():
            # Dateiname mit Informationen
            html_txt = "".join([
                html_txt,
                '<tr>',
                '<td id="left">', tx_name, '</td>',
                '<td id="left"><small>', inf[0], '</small></td>',
                '<td id="right"><small>', str(inf[1]), '</small></td>',
                '</tr>'
            ])
        # Tabellen Ende
        html_txt = "".join([html_txt, "</table>"])
    # Dokument Ende
    html_txt = "".join([html_txt, "</body></html>"])
    # Rückgabe des HTML Textes
    return(html_txt)


def f_makedok(in_log):
    '''
    Abgespeicherte Json aus <DC_DIRS> laden und als HTML Dokumentation
    ebenfalls aus <DC_DIRS> speichern.
      in_log = Variable für Log Meldungen
    '''
    for tx_id, tp_pfade in DC_DIRS.items():
        # Verzeichnis laden
        dc_json = f_loadjson(tp_pfade[1])
        # Log-Meldung
        in_log = f_log(in_log, "JSON geladen", tp_pfade[1])
        # Schön formatierter Text
        html_txt = f_htmldok(dc_json)
        # HTML speichern
        f_savetext(tp_pfade[2], html_txt)
    return(in_log)


def f_checkdirs(in_log):
    '''
    Die JSON Unterschied Verzeichnisse von <DC_COMP> prüfen und das
    Resultat zurückgeben als Verzeichnis:
      {'ID': {'quelle': [<p>, <v>, <d>], 'ziel': <p>, [<v>, <d>]}, }
      ID = Id für die Paarung von Quelle und Ziel
      <p> = pfad/name.json
      <v> = True / False
      <d> = Datumtext ('jjjj-mm-tt HH:MM:SS')
    '''
    # Resultat Verzeichnis erstellen
    dc_result = {}
    for tx_id, tp_pfade in DC_DIRS.items():
        # Pfade normalisieren
        tx_jsonpfad = os.path.normcase(os.path.normpath(tp_pfade[1]))
        tx_htmlpfad = os.path.normcase(os.path.normpath(tp_pfade[2]))
        # Log-Meldung
        tx_text = "{0} / {1}".format(
            os.path.basename(tx_jsonpfad),
            os.path.basename(tx_htmlpfad)
        )
        in_log = f_log(in_log, "Zu prüfende Dateien", tx_text)
        # Prüf Verzeichnis erstellen
        dc_pruef = {'json': tx_jsonpfad, 'html': tx_htmlpfad}
        # Temporäres Verzeichnis für die Ergebnisse
        dc_temp = {
            'json': [tx_jsonpfad, None, None],
            'html': [tx_htmlpfad, None, None]}
        # Jsons prüfen
        for tx_pruefid, tx_dateipfad in dc_pruef.items():
            tx_dateipfad = tx_dateipfad.lower()
            if (os.path.isfile(tx_dateipfad) and
               tx_dateipfad.endswith(".json")):
                # Scheint eine JSON Datei zu sein, Json laden
                dc_json = f_loadjson(tx_jsonpfad)
                # Datum lesen
                if 'datum' in dc_json.keys():
                    # Alles gelesen OK
                    dc_temp[tx_pruefid][1] = True
                    dc_temp[tx_pruefid][2] = dc_json['datum']
                else:
                    # Probleme, nicht OK
                    dc_temp[tx_pruefid][1] = False
                    dc_temp[tx_pruefid][2] = ''
            elif (os.path.isfile(tx_dateipfad) and
                  tx_dateipfad.endswith(".html")):
                # Scheint eine HTML Datei zu sein, Datei-Info holen
                ob_datum = os.path.getmtime(tx_dateipfad)
                tx_datum = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(ob_datum)
                )
                dc_temp[tx_pruefid][1] = True
                dc_temp[tx_pruefid][2] = tx_datum
            else:
                # Scheint keine JSON oder HTML Datei zu sein
                dc_temp[tx_pruefid][1] = False
                dc_temp[tx_pruefid][2] = ''
        # Ergebnis dem Resultat Verzeichnis hinzufügen
        dc_result[tx_id] = dc_temp
        # Log-Meldung
        in_log = f_log(in_log, "Ergebnis", dc_result)
    # Resultat Verzeichnis zurückgeben
    return(in_log, dc_result)


def f_checkdiff(in_log):
    '''
    Die JSON Verzeichnisse und HTML Dokumentationen von <DC_DIRS>
    prüfen und das Resultat zurückgeben als Verzeichnis:
      {'ID': ['pfad', True/False, 'jjjj-mm-tt HH:MM:SS'], }
    '''
    # Resultat Verzeichnis erstellen
    dc_result = {}
    for tx_id, tp_pfade in DC_COMP.items():
        # Pfade normalisieren
        tx_pfad = os.path.normcase(os.path.normpath(tp_pfade[2]))
        # Log-Meldung
        tx_text = "{0}".format(os.path.basename(tx_pfad))
        in_log = f_log(in_log, "Zu prüfende Datei", tx_text)
        # Jsons prüfen
        tx_pfad = tx_pfad.lower()
        if (os.path.isfile(tx_pfad) and
           tx_pfad.endswith(".json")):
            # Scheint eine JSON Datei zu sein, Json laden
            dc_json = f_loadjson(tx_pfad)
            # Datum lesen
            if 'datum' in dc_json.keys():
                # Alles gelesen OK
                bl_v = True
                tx_d = dc_json['datum']
            else:
                # Probleme, nicht OK
                bl_v = False
                tx_d = ''
        else:
            # Scheint keine JSON oder HTML Datei zu sein
            bl_v = False
            tx_d = ''
        # Ergebnis dem Resultat Verzeichnis hinzufügen
        dc_result[tx_id] = [tx_pfad, bl_v, tx_d]
        # Log-Meldung
        in_log = f_log(in_log, "Ergebnis", dc_result)
    # Resultat Verzeichnis zurückgeben
    return(in_log, dc_result)


if __name__ == '__main__':
    # Json Dateiverzeichnis einlesen
    # Log-Nummer setzen
    in_log = 0
    # Quell Json Verzeichnis lesen und Json schreiben
    in_log = f_makejson(in_log)
    # Json laden und anzeigen
    in_log = f_showjson(in_log)
    # Json zum Vergleichen prüfen
    in_log, dc_result = f_checkcomp(in_log)
    print("Ergebnis COMPARE Prüfung")
    print("------------------------")
    print(dc_result)
    # Taste
    tx_input = input("Bitte [Enter] drücken ..")
    print("\n")
    # Json vergleichen
    in_log = f_makecomp(in_log)
    # Verzeichnisse als HTML ablegen
    in_log = f_makedok(in_log)
    # Json erfasster Strukturen prüfen
    in_log, dc_result = f_checkdirs(in_log)
    print("Ergebnis DIRS Prüfung")
    print("---------------------")
    print(dc_result)
    # Json Unerschiede prüfen
    in_log, dc_result = f_checkdiff(in_log)
    print("Ergebnis DIFF Prüfung")
    print("---------------------")
    print(dc_result)
    '''
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
