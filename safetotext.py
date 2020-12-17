#!/usr/bin/env python

import sqlite3

# global variables
dbname = 'templog.db'

# safes the contents of the database in a textfile


def safealltotext():
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    f = open('data.txt', 'w')
    for row in curs.execute("SELECT * FROM temps"):
        datestr = str(row[0])
        tempstr = str(row[1])
        f.write(datestr + ";" + tempstr + "\n")
    conn.close()
    f.close()


# starting point
if __name__ == "__main__":
    safealltotext()
