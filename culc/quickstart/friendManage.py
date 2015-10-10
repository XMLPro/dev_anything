__author__ = 'Admin'

# coding:utf-8
class friend:
    def __init__(self, db):
        self.db =db
        self.dbc = self.db.cursor()

    def friendAdd(self, userName, friendName):
        data = (userName, friendName)
        self.dbc.execute("INSERT INTO friend VALUES(?,?)", data)
        self.db.commit()

    def karifriendAdd(self, userName, friendName):
        data = (userName, friendName)
        self.dbc.execute("INSERT INTO notfication VALUES(?,?)", data)
        self.db.commit()

    def friendSerch(self, userName):
        friendData = self.dbc.execute("select friendName from friend where userName = ? and"
                                          " friendName = friendName", (userName,))
        for friend in friendData:
            return friend[0]
        return None

    def userSerch(self, userName):
        userData = self.dbc.execute("select userName from users where userName = ?", (userName,))
        for karifriend in userData:
            return karifriend[0]
        return None

    def karifriendSerch(self, userName):
        karifriendData = self.dbc.execute("select friendName from notfication where userName = ? and"
                                          " friendName = friendName", (userName,))
        for karifriend in karifriendData:
            return karifriend[0]
        return None

    def karideleteFriend(self, userName, friendName):
        data = (userName, friendName)
        self.dbc.execute("delete from notfication WHERE userName = ? and friendName = ?", data)
        self.db.commit()

    def deleteFriend(self, userName, friendName):
        data = (userName, friendName)
        self.dbc.execute("delete from friend WHERE (userName,friendName) = (?,?)", data)
        self.db.commit()
