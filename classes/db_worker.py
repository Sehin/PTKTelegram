import pymysql.cursors


class DBworker:
    connection = pymysql.connect(host='db4free.net', user='ptkteleg', password='1234567890', db='ptkteleg',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def __init__(self):
        pass

    def createTable(self):
        with self.connection.cursor() as cursor:
            sql = "create table users (id int (10) AUTO_INCREMENT, user_id int NOT NULL,PRIMARY KEY (id));"
            cursor.execute(sql)
            print(cursor.description)


    def insertUser(self, user_id):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`user_id`) VALUES (%s);"
            cursor.execute(sql, (user_id))
            print(cursor.description)
            self.connection.commit()

    def selectUsers(self):
        users = set()
        with self.connection.cursor() as cursor:
            sql = "select * from users"
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data:
                user_id = rec
                users.add(user_id["user_id"])
        return users

    def removeUser(self, user_id):
        with self.connection.cursor() as cursor:
            sql = "delete from users where user_id = " + str(user_id) + ";"
            cursor.execute(sql)
            self.connection.commit()


