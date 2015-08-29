__author__ = 'Owner'


class userTableManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()
        self.tableName = u"users"
        self.culum = ("userName", "password")

    def userAdd(self, userName, password):
        data = (userName, password)
        self.dbc.execute("INSERT INTO users VALUES(null,?,?);", data)
        self.db.commit()

    def userVerif(self, userName, password):
        users = self.dbc.execute("select * from users where userName = ?", (userName,))
        print(type(users))
        for user in users:
            print(userName)
            print(user)
            print(type(user))
            print(type(userName))
            print(type(user[0]))
            print(user[1])
            if (user[2] != password):
                print(password)
                return True
            else:
                return False
        return True