import sqlite3
from MessageLog import LogInConsole


def CreateTableUsersList():
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS usersList(
                        userID TEXT,
                        fullName TEXT,
                        userName TEXT,
                        blocking TEXT,
                        search TEXT);
                """)
    con.commit()
    LogInConsole("Таблица usersList была успешно создана!")


def CreateTableUserOfSetting():
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS userOfSetting(
                        userID TEXT,
                        status TEXT,
                        class TEXT,
                        subgroup TEXT,
                        englishSubgroup TEXT,
                        groupings TEXT,
                        emojiID TEXT,
                        formatToday TEXT,
                        formatDate TEXT);
                """)
    con.commit()
    LogInConsole("Таблица userOfSetting была успешно создана!")


def CreateTableHistorySetting():
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS historySetting(
                        userID TEXT,
                        class TEXT,
                        teacher TEXT,
                        status0 TEXT,
                        status1 TEXT,
                        status2 TEXT,
                        status3 TEXT,
                        status4 TEXT,
                        status5 TEXT,
                        status6 TEXT,
                        status7 TEXT,
                        status8 TEXT,
                        status9 TEXT,
                        status10 TEXT,
                        status11 TEXT,
                        status12 TEXT);
                """)
    con.commit()
    LogInConsole("Таблица historySetting была успешно создана!")


def CreateTableScheduleList():
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS scheduleList(
                            book TEXT,
                            clue TEXT,
                            class TEXT,
                            week TEXT,
                            date TEXT,
                            number TEXT,
                            lesson TEXT,
                            grouping TEXT,
                            firstName TEXT,
                            lastName TEXT,
                            middleName TEXT,
                            cabinet TEXT,
                            view TEXT);
                    """)
    con.commit()
    LogInConsole("Таблица scheduleList была успешно создана!")


def CreateTableGroupList():
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS groupList(
                            book TEXT,
                            clue TEXT,
                            class TEXT,
                            lesson TEXT,
                            grouping TEXT,
                            firstName TEXT,
                            lastName TEXT,
                            middleName TEXT);
                    """)
    con.commit()
    LogInConsole("Таблица groupList была успешно создана!")


def CreateAll():
    CreateTableUsersList()
    CreateTableUserOfSetting()
    CreateTableScheduleList()
    CreateTableGroupList()
    CreateTableHistorySetting()
