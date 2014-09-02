#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
from pprint import pprint

FILENAME = "/home/jochen/python/sishandball/sisdb.sdb3"
#x = int(sys.argv[1])
#y = sys.argv[2]

def select_addresses(conn):
    sql = """
    SELECT Spiel, Schiri
    FROM Spiele05
    WHERE Angesetzt = '0'
    ORDER by Spiel
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def main():
    conn = sqlite3.connect(FILENAME)
    adr_cursor = select_addresses(conn)
    adr_list = list(adr_cursor)
    print adr_list
    for Spiel, Schiri in adr_list:
        print Spiel+" "+Schiri
    conn.close()


if __name__ == "__main__":
    main()
