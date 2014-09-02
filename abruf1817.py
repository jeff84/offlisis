#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from pprint import pprint

import mechanize
from BeautifulSoup import BeautifulSoup

FILENAME = "/home/jochen/python/sishandball/sisdb.sdb3"


def create_db_structure(conn):
    sql = "DROP TABLE Tabelle1817"
    conn.execute(sql)
    conn.commit()
    sql = "DROP TABLE Spiele1817"
    conn.execute(sql)
    conn.commit()
    sql = """
    CREATE TABLE Tabelle1817 (
      id INTEGER PRIMARY KEY,
      Platz INTEGER,
      Mannschaft TEXT,
      Spiele TEXT,
      Siege INTEGER,
      Unentschieden INTEGER,
      Niederlagen INTEGER,
      Toref INTEGER,
      Toreg INTEGER,
      Tordiff INTEGER,
      Punktef INTEGER,
      Punkteg INTEGER
    )
    """
    conn.execute(sql)
    conn.commit()
    sql = """
    CREATE TABLE Spiele1817 (
      id INTEGER PRIMARY KEY,
      Spiel INTEGER,
      Datum TEXT,
      DatumS TEXT,
      Uhrzeit TEXT,
      Heim TEXT,
      Gast TEXT,
      ToreH INTEGER,
      ToreG INTEGER,
      Schiri TEXT,
      Ergebnis BOOLEAN,
      Angesetzt BOOLEAN
    )
    """
    conn.execute(sql)
    conn.commit()
    sql = """
    CREATE INDEX ix_Tabelle_Mannschaft ON Tabelle1817 (Mannschaft)
    """
    conn.execute(sql)
    conn.commit()
   
def insert_tabelle(conn, zeile):
    sql = """
    INSERT INTO Tabelle1817 (
      Platz, Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Toref, Toreg, Tordiff, Punktef, Punkteg
    ) VALUES (
      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    conn.execute(sql, zeile)
    conn.commit()

def insert_ergebnisse(conn, zeile2):
    sql = """
    INSERT INTO Spiele1817 (
      Spiel, Datum, DatumS, Uhrzeit, Heim, Gast, ToreH, ToreG, Ergebnis, Angesetzt
    ) VALUES (
      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    conn.execute(sql, zeile2)
    conn.commit()

def insert_spiele(conn, zeile3):
    sql = """
    INSERT INTO Spiele1817 (
      Spiel, Datum, DatumS, Uhrzeit, Heim, Gast, Schiri, Ergebnis, Angesetzt
    ) VALUES (
      ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    conn.execute(sql, zeile3)
    conn.commit()

def main():
   
    # Zum TESTEN -- Alte DB löschen
    #if os.path.isfile(FILENAME):
    #    os.remove(FILENAME)
   
    # SQLite-Connection
    conn = sqlite3.connect(FILENAME)
   
    # Tabelle erstellen und mit Werten füllen
    create_db_structure(conn)
    
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 '
        '(X11; U; Linux i686; de; rv:1.9.1.2) '
        'Gecko/20090729 Firefox/3.5.2')]
    #url = 'http://www.sis-handball.de/web/Default.aspx?view=Tabelle&Liga=001510504503503000000000000000000003000'
    urlta = 'http://www.sis-handball.de/web/Tabelle/?view=Tabelle&Liga=001511504503503000000000000000000003000'
    urlsp = 'http://www.sis-handball.de/web/AlleSpiele/?view=AlleSpiele&Liga=001511504503503000000000000000000003000'
    soupta = BeautifulSoup(br.open(urlta).read())
    soupsp = BeautifulSoup(br.open(urlsp).read())
    #r = br.open(url).read()
    tabeig = {
        "cellpadding" : "0",
        "cellspacing" : "0",
        "style" : "font-family:Lucida Sans, Verdana, Arial;color: #272829; "
            "font-size: 14px; text-align:center; margin-left: auto; "
            "margin-right: auto; width: 95%; margin-top: 5px; "
            "margin-bottom: 5px;"
        }
    tab2eig = {
        "style" : "font-size: 14px; font-family:Lucida Sans, Verdana, Arial; "
            "color:#272829; text-align: left; margin-left:auto; margin-right:auto; width: 95%;"
        }
    tab3eig = {
        "style" : "font-size: 12px; color:#272829; font-family:Lucida Sans, Verdana, Arial; "
            "text-align: left; margin-left:auto; margin-right:auto; "
            "empty-cells:show; width: 98%;",
        "cellpadding" : "0",
        "cellspacing" : "0"
        }
    tables = soupta.findAll("table", tabeig)
    table2 = soupsp.find("table", tab2eig)
    table3 = soupsp.find("table", tab3eig)
    table = tables[1]
    #table2 = tables2[0]
    for row in table.findAll('tr')[1:]:		
        col = row.findAll('td')
        team = row.findAll('a')	
        try:
            col[1]
        except IndexError:
            continue
        Platz = col[1].string
        Mannschaft = team[0].string
        Spiele = col[3].string
        Siege = col[4].string
        Unentschieden = col[5].string
        Niederlagen = col[6].string
        Tore = col[7].string
        t = Tore.split(":")
        Toref = t[0]
        Toreg = t[1]
        Tordiff = col[8].string
        Punkte = col[9].string
        p = Punkte.split(":")
        Punktef = p[0]
        Punkteg = p[1] 
        zeile = (Platz, Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Toref, Toreg, Tordiff, Punktef, Punkteg)
        insert_tabelle(conn, zeile)
    for row2 in table2.findAll('tr')[1:]:		
        col2 = row2.findAll('td')
        team2 = row2.findAll('a')
        try:
            col2[1]
        except IndexError:
            continue
        Spiel = team2[0].string
        d2 = col2[1].string
        Datum = d2[1:]
        Datumsp = Datum.split(".")
        Uhrzeit = col2[2].string[1:]
        Uhrs = Uhrzeit.split(":")
        DatumS = Datumsp[2]+"_"+Datumsp[1]+"_"+Datumsp[0]+"_"+Uhrs[0]+"_"+Uhrs[1]
        Heim = team2[1].string
        Gast = team2[2].string
        Ergebnis = col2[6].string
        t = Ergebnis.split(":")
        ToreH = t[0]
        ToreG = t[1]
        Ergeb = True
        Ang = True
        zeile2 = (Spiel, Datum, DatumS, Uhrzeit, Heim, Gast, ToreH, ToreG, Ergeb, Ang)
        insert_ergebnisse(conn, zeile2)
    for row3 in table3.findAll('tr')[1:]:		
        col3 = row3.findAll('td')
        team3 = row3.findAll('a')
        try:
            col3[3]
        except IndexError:
            continue
        Spielt3 = team3[0].string
        Spiel3 = Spielt3.split(" ")[1]
        d3 = col3[2].string
        Datum3 = d3[1:]
        Datumsp3 = Datum3.split(".")
        Uhrzeit3 = col3[3].string[1:]
        Uhrs3 = Uhrzeit3.split(":")
        DatumS3 = Datumsp3[2]+"_"+Datumsp3[1]+"_"+Datumsp3[0]+"_"+Uhrs3[0]+"_"+Uhrs3[1]
        Heim3 = team3[1].string
        Gast3 = team3[2].string
        Schiri = col3[6].string
        Ang = True
        Erg = False
        if 'noch nicht' in Schiri:
            Schiri = ""
            Ang = False
        zeile3 = (Spiel3, Datum3, DatumS3, Uhrzeit3, Heim3, Gast3, Schiri, Erg, Ang)
        insert_spiele(conn, zeile3)
    conn.close()


if __name__ == "__main__":
    main()


