import sqlite3
from MessageLog import LogInConsole


def DeleteUser(userID):
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("DELETE from usersList WHERE userID = (?);", ([f"{userID}"]))
    cur.execute("DELETE from userOfSetting WHERE userID = (?);", ([f"{userID}"]))
    cur.execute("DELETE from historySetting WHERE userID = (?);", ([f"{userID}"]))
    con.commit()
    LogInConsole(f"Пользователь {userID} был удалён.")

