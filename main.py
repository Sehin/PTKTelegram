import misc
import requests
import json
import configuration

token = misc.token
URL = 'https://api.telegram.org/bot'


def getUpdates():
    url = URL + token + '/getupdates'
    answer = requests.get(url)
    return answer.json()

def getMessage():
    data = getUpdates()
    chatId = data["result"][-1]["message"]["chat"]["id"]
    text = data["result"][-1]["message"]["text"]
    message = {'chatId': chatId, "text": text}
    return message

def sendMessage(chat_id, text):
    url = URL + token + '/sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)

def main():
    #message = getMessage()
    #sendMessage(message["chatId"], "О, привет!")

    configManager = configuration.Configuration()
    a = configManager.readConfigFile()
    print(a)

    '''
    d = getUpdates()
    with open('updates.json', 'w') as file:
        json.dump(d, file, indent=2, ensure_ascii=False)
    '''



if __name__ == '__main__':
    main()



'''
1. Определение пользователей у которых есть доступ к рассылке (с помошью класса configuration - запись и чтение cfg файла)
2. 
'''
