#!/usr/bin/python3

import argparse
import sqlite3

db_name = '/home/pi/logger/templog.db'
conn = sqlite3.connect(db_name)


def create_tables():
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS temps (timestamp DATETIME, temp NUMERIC)")
    curs.execute("CREATE TABLE IF NOT EXISTS vibrations (timestamp DATETIME, vibration BOOL)")

    try:
        curs.execute("CREATE TABLE series (number INTEGER)")
    except Exception:
        # table exists
        pass
    else:
        values = [f"({x})" for x in range(0, 1000)]
        curs.execute(f"INSERT INTO series(number) VALUES {','.join(values)}")

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
        VALUES (datetime('now', 'localtime'), ?)
    """, [is_vibrating])
    conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The command to execute",
                        choices=["create", "clear"], default="create")
    args = parser.parse_args()

    if args.command == "create":
        create_tables()
    elif args.command == "clear":
        clear_tables()
    else:
        print(f"Unknown command: {args.command}")
