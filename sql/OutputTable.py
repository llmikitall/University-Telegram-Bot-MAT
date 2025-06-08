import sqlite3


def OutputTable(table):
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM " + table)
    return cur.fetchall()
