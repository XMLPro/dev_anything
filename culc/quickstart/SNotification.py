__author__ = 'Owner'


class SNotification:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, sender, recipient, itemName, itemID):
        data = (sender, recipient, itemName, itemID)
        self.dbc.execute("INSERT INTO snotification VALUES(?,?,?,?);", data)
        self.db.commit()

    def entrySerch(self, recipient):
        userData = self.dbc.execute("select * from snotification where recipient = ?", (recipient,))
        entries = [dict(sender=row[0], recipient=row[1], itemName=row[2], itemID=row[3]) for row in
                   userData.fetchall()]
        return entries

    def entryUniqueSerch(self, id):
        userData = self.dbc.execute("select * from snotification where id=?",  (id,))
        entries = [dict(sender=row[0], recipient=row[1], itemName=row[2], itemID=row[3]) for row in
                   userData.fetchall()]
        return entries

    def entryDelete(self, itemID):
        self.dbc.execute("delete from snotification where id == ?",(itemID,))
        self.db.commit()



    def entryUpdate(self, sender, recipient, itemName, itemID):
        data = (itemName, sender,recipient, itemID,)
        self.dbc.execute("UPDATE snotification SET sender=? ,recipient=? itemName=?, itemID WHERE id = ? and userName=?;", data)
        self.db.commit()
