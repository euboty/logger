#!/usr/bin/python3

import argparse
import sqlite3

savetill = '-3 month'

db_name = '/home/pi/logger/templog.db'
conn = sqlite3.connect(db_name)


def create_tables():
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS temps (timestamp INTEGER, temp NUMERIC)")
    curs.execute("CREATE TABLE IF NOT EXISTS vibrations (timestamp INTEGER, vibration BOOL)")
    conn.commit()


def clear_tables():
    curs = conn.cursor()
    curs.execute("DELETE FROM temps")
    curs.execute("DELETE FROM vibrations")
    conn.commit()


def save_vibration(is_vibrating):
    curs = conn.cursor()
    curs.execute("""
        INSERT INTO vibrations(timestamp, vibration)
        VALUES (strftime('%s','now'), ?)
    """, [is_vibrating])
    conn.commit()

def save_temperature(temp):
    curs = conn.cursor()
    curs.execute("""
        INSERT INTO temps 
        values(strftime('%s','now'), (?))
    """, (temp,))
    conn.commit()

def delete_old_temps():
    """deletes entrys older than savetill"""
    curs = conn.cursor()
    curs.execute(
        "DELETE FROM temps WHERE timestamp <= strftime('%s',date('now', (?)))", (savetill,))
    conn.commit()

def delete_old_vibrations():
    """deletes entrys older than savetill"""
    curs = conn.cursor()
    curs.execute(
        "DELETE FROM vibrations WHERE timestamp <= strftime('%s',date('now', (?)))", (savetill,))
    conn.commit()

def display_temps():
    curs = conn.cursor()
    print("Last 100 measurements:")
    for row in curs.execute("""
        SELECT strftime('%Y-%m-%d %H:%M:%S', timestamp, 'unixepoch'), 
        temp FROM temps ORDER BY timestamp DESC LIMIT 100
        """):
        print(str(row[0])+"	"+str(row[1]))

def display_vibrations():
    curs = conn.cursor()
    print("Last 100 measurements:")
    for row in curs.execute("""
            SELECT strftime('%Y-%m-%d %H:%M:%S', timestamp, 'unixepoch'), 
            vibration FROM vibrations ORDER BY timestamp DESC LIMIT 100
        """):
        print(str(row[0])+"	"+str(row[1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The command to execute",
                        choices=["create", "clear", "displaytemps", "displayvibrations"], default="create")
    args = parser.parse_args()

    if args.command == "create":
        create_tables()
    elif args.command == "clear":
        clear_tables()
    elif args.command == "displaytemps":
        display_temps()
    elif args.command == "displayvibrations":
        display_vibrations()
    else:
        print(f"Unknown command: {args.command}")
