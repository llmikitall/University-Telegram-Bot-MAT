import sqlite3


def SearchAny(userID, table, title):
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("SELECT " + title + " FROM " + table + " WHERE userID = (?);", ([f"{userID}"]))
    memory = cur.fetchall()
    con.close()
    if len(memory) == 0:
        return None
    return memory[0][0]
