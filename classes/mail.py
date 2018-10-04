import imaplib
import email
import classes.incident as incident

class MailWorker:
    connection = ""
    SENDER = "smenaptk@rzd.gvc.ru"
    def __init__(self):
        global connection
        connection = imaplib.IMAP4_SSL('imap.gmail.com')
        connection.login('pyteleg@gmail.com', 'Da14011402')
        pass

    def getAllFiles(self):
        status, msgs = connection.select('INBOX')
        assert status == 'OK'
        typ, data = connection.search(None, 'FROM', 'smenaptk@gvc.rzd.ru')
        print(data)
        for num in data[0].split():
            typ, message_data = connection.fetch(num, '(RFC822)')
            print(data)
            print('Message %s\n%s\n' % (num, message_data[0][1]))
        connection.close()
        connection.logout()

        mail = email.message_from_bytes(message_data[0][1])

        if mail.is_multipart():
            for part in mail.walk():
                content_type = part.get_content_type()
                filename = part.get_filename()
                if filename:
                    # Нам плохого не надо, в письме может быть всякое барахло
                    x = part.get_payload(decode=True).decode('utf-8')
                    print(x)
                    #text = text.encode('UTF-8')
                    #with open(part.get_filename(), 'wb') as new_file:
                    #    new_file.write(part.get_payload(decode=True))
        pass

    def getAllIncidents(self):
        incs = set()


        status, msgs = connection.select('INBOX')
        assert status == 'OK'
        typ, data = connection.search(None, 'FROM', 'smenaptk@gvc.rzd.ru')
        print(data)
        for num in data[0].split():
            typ, message_data = connection.fetch(num, '(RFC822)')
            #print(data)
            #print('Message %s\n%s\n' % (num, message_data[0][1]))
            print(num)


            mail = email.message_from_bytes(message_data[0][1])

            if mail.is_multipart():
                for part in mail.walk():
                    filename = part.get_filename()
                    if filename:
                        x = part.get_payload(decode=True).decode('utf-8')
                        z = str(x).split('\r')
                        for i in z:
                            i = i.split(';')
                            if len(i)==4:
                                inc = incident.Incident(i[0], i[1], i[2], i[3])
                                incs.add(inc)
                            elif len(i)==3:
                                inc = incident.Incident(i[0], i[1], i[2])
                                incs.add(inc)

            # Удаление сообщений
            connection.store(num, '+FLAGS', '\\Deleted')
            connection.expunge()


        connection.close()
        connection.logout()
        return incs