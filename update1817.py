#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from pprint import pprint

import mechanize
from BeautifulSoup import BeautifulSoup

FILENAME = "/home/jochen/python/sishandball/sisdb.sdb3"

def update_tabelle(conn, zeile):
    sql = """
    UPDATE Tabelle1817 
    SET Platz = ?, Spiele = ?, Siege = ?, Unentschieden = ?, 
        Niederlagen = ?, Toref = ?, ToreG = ?, Tordiff = ?, 
        Punktef = ?, Punkteg = ? 
    WHERE Mannschaft = ?
    """
    conn.execute(sql, zeile)
    conn.commit()

def update_platz(conn, zeile):
    sql = """
    UPDATE Tabelle1817 
    SET Platz = ? 
    WHERE Mannschaft = ?
    """
    conn.execute(sql, zeile)
    conn.commit()

def update_ergebnisse(conn, spiela):
    sql = """
    UPDATE Spiele1817
    SET ToreH = ?, ToreG = ?, Ergebnis = ? 
    WHERE Spiel = ?
    """
    conn.execute(sql, spiela)
    conn.commit()

def update_spiele(conn, spielb):
    sql = """
    UPDATE Spiele1817
    SET Schiri = ?, Angesetzt = ?
    WHERE Spiel = ?
    """
    conn.execute(sql, spielb)
    conn.commit()

def select_spiele(conn):
    sql = """
    SELECT Spiel
    FROM Spiele1817
    WHERE Angesetzt = '0'
    ORDER by Spiel
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def select_ergebnis(conn):
    sql = """
    SELECT Spiel
    FROM Spiele1817
    WHERE Ergebnis = '0'
    ORDER by Spiel
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def select_tabelle(conn):
    sql = """
    SELECT Platz, Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Toref, Toreg, Tordiff, Punktef, Punkteg
    FROM Tabelle1817
    ORDER by Platz
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def main():
   
    # Zum TESTEN -- Alte DB löschen
    #if os.path.isfile(FILENAME):
    #    os.remove(FILENAME)
   
    # SQLite-Connection
    conn = sqlite3.connect(FILENAME)
   
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
    adr_cursor = select_tabelle(conn)
    adr_list = list(adr_cursor)
    for row in table.findAll('tr')[1:]:		
        col = row.findAll('td')
        team = row.findAll('a')	
        try:
            col[1]
        except IndexError:
            continue
        platz = col[1].string
        mann = team[0].string
        spiele = col[3].string
        siege = col[4].string
        unent = col[5].string
        nied = col[6].string
        Tore = col[7].string.split(":")
        toref = Tore[0]
        toreg = Tore[1]
        tordiff = col[8].string
        Punkte = col[9].string
        p = Punkte.split(":")
        pktf = p[0]
        pktg = p[1]
        zeile = (platz, spiele, siege, unent, nied, toref, toreg, tordiff, pktf, pktg, mann)
        zeiplatz = (platz, mann)
        for Platz, Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Toref, Toreg, Tordiff, Punktef, Punkteg in adr_list:
            if mann is Mannschaft:
                if spiele is not Spiele:
                    print zeile
                    update_tabelle(conn, zeile)
                elif platz is not Platz:
                    print zeiplatz
                    update_platz(conn, zeiplatz)
    adr_cursor = select_ergebnis(conn)
    adr_list = list(adr_cursor)
    for row2 in table2.findAll('tr')[1:]:		
        col2 = row2.findAll('td')
        team2 = row2.findAll('a')
        try:
            col2[1]
        except IndexError:
            continue
        spiel = team2[0].string
        Ergebnis = col2[6].string
        t = Ergebnis.split(":")
        toreH = t[0]
        toreG = t[1]
        erg = True
        spiela = (toreH, toreG, erg, spiel)
        for Spiel in adr_list:
            if int(spiel) is Spiel:
                print spiela
                update_ergebnisse(conn, spiela)
    adr_cursor = select_spiele(conn)
    adr_list = list(adr_cursor)
    for row3 in table3.findAll('tr')[1:]:		
        col3 = row3.findAll('td')
        team3 = row3.findAll('a')
        try:
            col3[3]
        except IndexError:
            continue
        Spielt3 = team3[0].string
        spiel = Spielt3.split(" ")[1]
        schiri = col3[6].string
        ang = True
        if 'noch nicht' in schiri:
            continue
        spielb = (schiri, ang, spiel)
        for Spiel in adr_list:
            if int(spiel) is Spiel:
                print spielb
                update_spiele(conn, spielb)
    conn.close()


if __name__ == "__main__":
    main()


