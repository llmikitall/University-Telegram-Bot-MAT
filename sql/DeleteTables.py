import sqlite3
from sql.CreateTables import CreateTableUsersList, CreateTableUserOfSetting, CreateTableGroupList, \
    CreateTableScheduleList, CreateTableHistorySetting
from MessageLog import LogInConsole


def DeleteTables(table):
    if table in ("groupList", "scheduleList"):
        con = sqlite3.connect("sql/db/schedule.db")
    else:
        con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    try:
        cur.execute("DROP TABLE " + table + ";")
        con.commit()
        LogInConsole("Таблица " + table + " была удалена.")
    except sqlite3.OperationalError:
        return f"Таблицы '{table}' не существует..."
    if table == "usersList":
        CreateTableUsersList()
    elif table == "userOfSetting":
        CreateTableUserOfSetting()
    elif table == "scheduleList":
        CreateTableScheduleList()
    elif table == "groupList":
        CreateTableGroupList()
    elif table == "historySetting":
        CreateTableHistorySetting()

    return f"Таблица '{table}' была пересоздана."


def DeleteAll():
    tables = ["usersList", "userOfSetting", "historySetting", "scheduleList", "groupList"]
    for table in tables:
        DeleteTables(table)
