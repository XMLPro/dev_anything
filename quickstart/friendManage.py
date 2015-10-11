__author__ = 'Admin'


# coding:utf-8
class friend(object):
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def friendAdd(self, userName, friendName):
        data = (userName, friendName)
        self.dbc.execute("INSERT INTO friend VALUES(?,?);", data)
        self.db.commit()

    def entrySerch(self, userName):
        friends = self.dbc.execute("select * from friend where userName = ?", (userName,))
        entries = [dict(userName=row[0], friendName=row[1]) for row in
                   friends.fetchall()]
        return entries

    def friendSerch(self, key, value):
        friends = self.dbc.execute("select * from friend where ? = ?", (key, value))
        return friends

    def deleteFriend(self, friendName):
        data = friendName
        self.dbc.execute("delete * from friend WHERE ? = ?", data)
        self.db.commit()
