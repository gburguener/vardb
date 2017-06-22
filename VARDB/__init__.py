from peewee import MySQLDatabase, Model

from peewee import Proxy
from playhouse.shortcuts import RetryOperationalError
import json

class VARDBBase(Model):
    def __str__(self):
        return json.dumps(self._data)

    def __repr__(self):
        return self.__str__()

sqldb =  Proxy() 

def connect_to_db(database='vardb',user='root',password='',engine=MySQLDatabase):
    class MyRetryDB(RetryOperationalError, engine):
        pass


    mysqldb = MyRetryDB(database, user=user, password=password)
    sqldb.initialize(mysqldb)