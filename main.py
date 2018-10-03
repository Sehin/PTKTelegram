import misc
import requests
import classes.message as msg
import time
import classes.configuration as cfg

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
    if data["result"]!=[]:
        global offsetId
        offsetId = int(data["result"][-1]["update_id"]) + 1
    return messages



def sendMessage(chat_id, text):
    url = URL + token + '/sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)

def checkPasswordInput(chat_id, text, users):
    if text == '/password':
        sendMessage(chat_id, 'Чтобы получать рассылку по инцидентам смены ПТК - пришлите мне пароль! Чтобы остановить рассылку - команда /stop.')
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



def main():
    configuration = cfg.Configuration()
    users = configuration.readConfigFile()
    #sendMsgToAllUsers("Бот активирован! Ожидайте рассылку", users)

    while 1:
        for message in getMessages():

            # -----------------------------
            # ОСНОВНАЯ ОБРАБОТКА СОБЩЕНИЙ!!!
            # -----------------------------
            print(message.text)

            # Все, что связано с подпиской
            q = checkPasswordInput(message.chatId, message.text, users)
            if q != None:
                users.add(q)
                configuration.updateConfigFile(users)

            # Все, что связано с отпиской
            q = checkStopInput(message.chatId, message.text, users)
            if q!= None:
                users.remove(q)
                configuration.updateConfigFile(users)




        time.sleep(repeatRequestTime)


    '''
    configManager = configuration.Configuration()
    a = configManager.readConfigFile()
    print(a)
    '''

    '''
    d = getUpdates()
    with open('updates.json', 'w') as file:
        json.dump(d, file, indent=2, ensure_ascii=False)
    '''

def test():
    print('yeah')

if __name__ == '__main__':
    main()



'''
1. Определение пользователей у которых есть доступ к рассылке (с помошью класса configuration - запись и чтение cfg файла)
2. 
'''
