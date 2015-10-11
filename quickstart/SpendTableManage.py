__author__ = 'Owner'
from datetime import date, datetime


class SpendTableManage:
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()

    def entryAdd(self, userName, itemName, money, day, text):
        self.dbc.execute("INSERT INTO spend VALUES(null,?,?,?,?,?);", (userName, itemName, money, day, text,))
        self.db.commit()

    def entrySerch(self, userName):
        userData = self.dbc.execute("select * from spend where userName = ?", (userName,))
        entries = [dict(id=row[0], itemName=row[2], money=row[3], day=row[4], text=row[5]) for row in
                   userData.fetchall()]
        return entries

    def entryDelete(self,id):
        self.dbc.execute("delete from spend where id == ?", (id,))
        self.db.commit()

    def entryUpdate(self, id, userName, itemName, money, day, text):
        data = (itemName, money, day, text, id, userName,)
        self.dbc.execute("UPDATE spend SET itemName=? ,money=?,daydata=?,text=? WHERE id = ? and userName=?;", data)
        self.db.commit()

    def shareget(self,id):
        userData = self.dbc.execute("select * from spend where id = ?", (id,))
        entries = [dict(id=row[0], itemName=row[2], money=row[3], day=row[4], text=row[5]) for row in
                   userData.fetchall()]
        return entries



    def uniqueSerch(self,id):
       idData= self.dbc.execute("select * from spend where id = ?", (id,))
       for id in idData:
           return id[2]
       else:
           return None
