
class groupTableManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()


    def entryAdd(self, userName, password):
        data = (userName, password)
        self.dbc.execute("INSERT INTO groups VALUES(null,?,?);", data)
        self.db.commit()

    def entryVerif(self, userName, password):
        users = self.dbc.execute("select * from groups where groupname = ?", (userName,))
        for user in users:
            if (user[2] == password):
                return True
        return False

    def userVaild(self,userName):
        users = self.dbc.execute("select groupname, name from groups where groupname = ?;",(userName,))
        for user in users:
            if user is userName:
                return True
        else:
            return True

    def entrySerch(self,userName):
        return self.dbc.execute("select * from groups where groupname = ?", (userName,))