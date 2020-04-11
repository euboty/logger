#!/usr/bin/env python

import sqlite3

import os
import time
import glob

# global variables
dbname='templog.db'

# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)

    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()

#starting point
if __name__=="__main__":
    display_data()