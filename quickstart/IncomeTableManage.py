__author__ = 'Owner'
from datetime import date, datetime


class IncomeTableManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, userName, itemName, money, day, text):
        self.dbc.execute("INSERT INTO income VALUES(null,?,?,?,?,?);", (userName, itemName, money, day, text,))
        self.db.commit()

    def entrySerch(self, userName):
        userData = self.dbc.execute("select * from income where userName = ?", (userName,))
        entries = [dict(id=row[0], itemName=row[2], money=row[3], day=row[4], text=row[5]) for row in
                   userData.fetchall()]
        return entries

    def entryDelete(self,id):
        print(type(id))
        self.dbc.execute("delete from income where id == ?", (int(id),))
        self.db.commit()

    def entryUpdate(self, id, userName, itemName, money, day, text):
        data = (itemName, money, day, text, id)
        print userName
        print itemName
        print money
        print day
        print text
        print id
        self.dbc.execute("UPDATE income SET itemName=? ,money=?,daydata=?,text=? WHERE id = ?;", data)
        self.db.commit()
