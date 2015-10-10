__author__ = 'Owner'


class SNotification:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, sender, recipient, itemName, itemID):
        data = (sender, recipient, itemName, itemID)
        self.dbc.execute("INSERT INTO spend VALUES(?,?,?,?);", data)
        self.db.commit()

    def entrySerch(self, recipient):
        userData = self.dbc.execute("select * from spend where userName = ?", (recipient,))
        entries = [dict(sender=row[0], recipient=row[1], itemName=row[2], itemID=row[3]) for row in
                   userData.fetchall()]
        return entries

    def entryDelete(self, sender, itemID):
        self.dbc.execute("select * from spend where userName = ? and id = ?", (sender, itemID))

    def entryUpdate(self, sender, recipient, itemName, itemID):
        data = (itemName, money, tag, id, userName,)
        self.dbc.execute("UPDATE spend SET sender=? ,recipient=? itemName=?, itemID WHERE id = ? and userName=?;", data)
        self.db.commit()
