from datetime import datetime


# MessageInConsole - метод для вывода сообщений, которые пользователи отправляют боту. Передаётся <message: Message>.
# Выводит: [Время] [ID пользователя] <сообщение>
def MessageInConsole(message):
    time_now = datetime.now().strftime('%H:%M')
    print(f"[{time_now}] [{message.chat.id}] {message.text}")


# LogInConsole - метод для шаблонного вывода сообщений от администратора в консоль. Передаётся <message: String>.
# Выводит: [Время] <сообщение>
def LogInConsole(message):
    time_now = datetime.now().strftime('%H:%M')
    print(f"[{time_now}] {message}")
