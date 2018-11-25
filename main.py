import logging

import requests
import time

import classes.db_worker as db
import classes.mail as mail
import classes.message as msg
import misc
from boto.s3.connection import S3Connection

token = misc.token
URL = 'https://api.telegram.org/bot'
offsetId = 1
repeatRequestTime = 5


def getUpdates():
    url = URL + token + '/getupdates?offset=' + str(offsetId)
    answer = requests.get(url)
    return answer.json()


def getMessages():
    # take last msg update id and set it to offsetId + 1
    data = getUpdates()
    messages = list()
    for message in data["result"]:
        messages.append(msg.Message(message["message"]["text"],
                                    str(message["message"]["chat"]["id"]),
                                    message["update_id"]))
    if data["result"] != []:
        global offsetId
        offsetId = int(data["result"][-1]["update_id"]) + 1
    return messages


def sendMessage(chat_id, text):
    url = URL + token + '/sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def checkPasswordInput(chat_id, text, users):
    if text == '/password':
        sendMessage(chat_id,
                    'Чтобы получать рассылку по инцидентам смены ПТК - пришлите мне пароль! Чтобы остановить рассылку - команда /stop.')
        return None
    if text == misc.access_password and chat_id in users:
        sendMessage(chat_id, 'Вы уже в списке рассылки.')
        return None
    if text == misc.access_password and chat_id not in users:
        sendMessage(chat_id, "Пароль правильный, вы добавлены в список рассылки.")
        return chat_id


def checkStopInput(chat_id, text, users):
    if text == "/stop" and chat_id in users:
        sendMessage(chat_id, "Остановка рассылки. Чтобы начать - напишите пароль.")
        return chat_id
    if text == "/stop" and chat_id not in users:
        sendMessage(chat_id, "Рассылка для вас остановлена. Чтобы начать - напишите пароль.")
        return None


def sendMsgToAllUsers(text, users):
    for user in users:
        sendMessage(user, text)


def sendIncidentsToAllUsers(users):
    mailer = mail.MailWorker();
    incidents = mailer.getAllIncidents()

    for user in users:
        for inc in incidents:
            sendMessage(user, inc.ESPPNum + '\n' + inc.EK + '\n' + inc.description + '\n' + inc.date)


def main():
    print(os.environ['access_password'])
    print(os.environ['mail_pass'])
   #s3 = S3Connection(os.environ['access_password'], os.environ['token'], os.environ['mail_pass'])

    dbworker = db.DBworker()
    users = dbworker.selectUsers()

    # configuration = cfg.Configuration()
    # users = configuration.readConfigFile()
    # sendMsgToAllUsers("Бот активирован! Ожидайте рассылку", users)

    while 1:
        for message in getMessages():
            # userLogger.info("User " + str(message.chatId) + " send to bot: " + str(message.text))
            # -----------------------------
            # ОСНОВНАЯ ОБРАБОТКА СОБЩЕНИЙ!!!
            # -----------------------------
            print(message.text)

            # Все, что связано с подпиской
            q = checkPasswordInput(message.chatId, message.text, users)
            if q != None:
                users.add(q)
                dbworker.insertUser(q)
                # infoLogger.info("User add to subscribe " + q)

            # Все, что связано с отпиской
            q = checkStopInput(message.chatId, message.text, users)
            if q != None:
                users.remove(q)
                dbworker.removeUser(q)
                # infoLogger.info("User remove from subscribe " + q)

        # Основной метод рассылки
        sendIncidentsToAllUsers(users)

        time.sleep(repeatRequestTime)


def test():
    for i in range(10, 0, -1):
        print(i)


if __name__ == '__main__':
    # main()
    test()

