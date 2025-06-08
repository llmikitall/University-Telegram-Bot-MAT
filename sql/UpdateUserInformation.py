import sqlite3


def UpdateAny(userID, table, title, value):
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("UPDATE " + table + " SET " + title + " = (?) WHERE userID = (?);",
                ([f"{value}", f"{userID}"]))
    con.commit()
    con.close()
