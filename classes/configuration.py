class Configuration:
    def __init__(self):
        pass

    def updateConfigFile(self, users):
        with open('config.cfg', 'w') as file:
            for user in users:
                file.write(str(user) + '\n')
        file.close()

    def readConfigFile(self):
        users = set()
        with open('config.cfg', 'r') as file:
            for line in file.readlines():
                users.add(line.rstrip())
        return users
