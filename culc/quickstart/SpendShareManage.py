__author__ = 'Owner'


class SpendShareManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, sender, recipient, itemName, itemID):
        data = (sender, recipient, itemName, itemID)
        self.dbc.execute("INSERT INTO spend VALUES(?,?,?,?);", data)
        self.db.commit()

    def entrySerch(self, userName):
        userData = self.dbc.execute("select * from spend where userName = ?", (userName,))
        entries = [dict(sender=row[0], recipient=row[1], itemName=row[2], itemID=row[3]) for row in
                   userData.fetchall()]
        return entries

    def entryUniqueSercjh(self, userName, id):
        userData = self.dbc.execute("select * from spend where userName = ? and id=id", (userName, id))
        for itemName in userData:
            return itemName[2]
        return None

    def entryDelete(self, userName, id):
        self.dbc.execute("select * from spend where userName = ? and id = ?", (userName, id))

    def entryUpdate(self, id, userName, itemName, money, tag):
        data = (itemName, money, tag, id, userName,)
        self.dbc.execute("UPDATE spend SET itemName=? ,money=? tag=? WHERE id = ? and userName=?;", data)
        self.db.commit()
