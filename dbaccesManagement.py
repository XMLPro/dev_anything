__author__ = 'Owner'

class dbaccesManagement(object):
    def __init__(self, database):
        self.db = database
        self.dbc = self.db.cursor()
        self.tableName = None

    def setTableName(self, name):
        self.tableName = name

    def addEntry(self, *words):
        value = "','".join(words)
        print("(%s)" % value)
        print(self.tableName)
        self.dbc.execute(
            "INSERT INTO %(tablename)s VALUES('%(value)s');" % {'tablename': self.tableName, 'value': value})
        self.db.commit()

    def serchEntry(self, culumname, word):
        value = self.dbc.execute(
            "select * from %(tablename)s where %(culumname)s = '%(word)s';" % {"tablename": self.tableName,
                                                                                   "culumname": culumname,
                                                                                   "word": word})
        return value

    def closeConect(self):
        self.dbcc = getattr(self.db, 'db', None)
        if self.dbcc is not None:
             self.dbcc.close()
