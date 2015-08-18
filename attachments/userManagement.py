__author__ = 'Owner'
from dbaccesManagement import dbaccesManagement
class userManagement(dbaccesManagement):
    def __init__(self, db):
        super(userManagement, self).__init__(db)
        super(userManagement, self).setTableName(u"users")
        self.tableName = u"users"
        self.culum = ("userName", "password")

    def userAdd(self, userName, password):
        super(userManagement, self).addEntry(userName, password)

    def userVerif(self, userName, password):
        users = super(userManagement, self).serchEntry(self.culum[0], userName)
        print(type(users))
        for user in users:
            print(userName)
            print(user)
            print(type(user))
            print(type(userName))
            print(type(user[0]))
            print(user[1])
            # if(user != userName):
            # print(user[0],u"tuppleの1" + "\n")
            # print(isinstance(userName,str))
            # return True
            if (user[1] != password):
                print(password)
                return True
            else:
                return False
        return True
