import os
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
        response = requests.get(link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        os.makedirs("excel", exist_ok=True)
        os.makedirs("doc", exist_ok=True)

        target_div = soup.find("div", id="bx_2339888724_97994")

        if not target_div:
            LogInConsole("[!] Error: Не найден целевой div блок.")
            time.sleep(3600)
            continue

        urls = []

        for a in target_div.find_all("a", href=True):
            href = a['href']
            if '/univers/shedule/download' in href:
                full_url = 'https://www.sevsu.ru' + href
                urls.append(full_url)

        try:
            with open("doc/URLFile.txt", "r", encoding='utf-8') as file:
                old_urls = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            old_urls = []

        new_urls = []
        downloaded_count = 0

        for i, url in enumerate(urls):
            new_urls.append(url)

            if i >= len(old_urls) or url != old_urls[i]:
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()

                    if 'Content-Disposition' in response.headers:
                        filename = response.headers['Content-Disposition'].split('filename=')[1].strip('"')
                    else:
                        filename = os.path.basename(url.split("?")[0])
                        if not filename.endswith(".xls") and not filename.endswith("xlsx"):
                            filename = f"schedule_{i+1}.xlsx"
                    filepath = os.path.join("excel", filename)
                    with open(filepath, "wb") as excelFile:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                excelFile.write(chunk)
                    try:
                        ExcelToSql(filename)
                        downloaded_count += 1
                    except Exception as e:
                        LogInConsole(f"      [!] Ошибка обработки {filename}: {str(e)}")
                except Exception as e:
                    LogInConsole(f"      [!] Ошибка скачивания {url}: {str(e)}")

        try:
            with open("doc/URLFile.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(new_urls))
        except Exception as e:
            LogInConsole(f"   [!] Ошибка записи URL файла: {str(e)}")

        if downloaded_count > 0:
            LogInConsole(f"[>] Скачано {downloaded_count} новых файлов!")
        else:
            LogInConsole("[>] Изменений не обнаружено")
        LogInConsole("[>] Цикл верификации расписания успешно пройден!")
        time.sleep(3600)
