__author__ = 'Owner'


class userTableManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, userName, password):
        data = (userName, password)
        self.dbc.execute("INSERT INTO users VALUES(null,?,?);", data)
        self.db.commit()

    def entryVerif(self, userName, password):
        users = self.dbc.execute("select * from users where userName = ?", (userName,))
        for user in users:
            if (user[2] == password):
                return True
            else:
                return False
        return False

    def entrySerch(self,userName):
        return self.dbc.execute("select * from users where userName = ?", (userName,))