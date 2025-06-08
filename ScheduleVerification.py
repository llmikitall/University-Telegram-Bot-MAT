import time

import requests

import xlrd3
from bs4 import BeautifulSoup
from ExcelReader import ExcelToSql
from MessageLog import LogInConsole


def ScheduleVerification():
    time.sleep(5)
    LogInConsole("[>] Запуск цикла верификации расписания:")
    while True:
        link = "https://www.sevsu.ru/univers/shedule/"
        responce = requests.get(link).text

        soup = BeautifulSoup(responce, "html.parser")
        try:
            URLFile = open("doc/URLFile.txt", "r")
        except FileNotFoundError:
            print("Опс")
            URLFile = open("doc/URLFile.txt", "w")
            URLFile.close()
            URLFile = open("doc/URLFile.txt", "r")
        OldURL = URLFile.read().split('\n')
        URLFile.close()
        URLText = ""
        i = 0
        for div in soup.find_all(class_='document-link__group'):
            for a in div.find_all('a'):
                try:
                    if a.get('href').find('/univers/shedule/download') != -1:
                        url = 'https://www.sevsu.ru' + a.get('href')
                        URLText = URLText + url + "\n"
                        filename = None
                        try:
                            if OldURL[i] == url:
                                i = i + 1
                                continue
                        except IndexError:
                            LogInConsole(f"   [!] Error: Ссылка №{str(i)} отсутствует. Исправляем...")
                        try:
                            query = requests.get(url)
                            filename = query.headers.get('Content-Disposition')
                            if filename is None:
                                LogInConsole(f"      [!] [{i}] Error: Ошибка, bad URL.")
                            filename = filename.split("filename=")[1]
                            file = open("excel/" + filename, "wb")
                            file.write(query.content)
                            file.close()
                            ExcelToSql(filename)
                        except xlrd3.biffh.XLRDError:
                            LogInConsole(f"      [!] [{filename}] Error: Ошибка со считыванием файла.")
                        except requests.exceptions.ChunkedEncodingError:
                            LogInConsole(f"      [!] [{filename}] Error: Ошибка со скачиванием файла.")
                        except AttributeError:
                            LogInConsole(f"      [!] [{filename}] Error: Серьёзная ошибка... Файл отличается.")
                        except PermissionError:
                            LogInConsole(f"      [!] [{filename}] Error: Книга используется.")
                        except IndexError:
                            LogInConsole(f"      [!] [{filename}] Error: Ошибка в коде.")
                        i = i + 1
                except AttributeError:
                    LogInConsole("      [!] Error: Ошибка...")

        # Запись новой ссылки
        URLFile = open('doc/URLFile.txt', "w")
        URLFile.write(URLText)
        URLFile.close()

        LogInConsole("[>] Цикл верификации расписания успешно пройден!")
        time.sleep(3600)
