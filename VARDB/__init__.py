from peewee import MySQLDatabase, Model

from peewee import Proxy
from playhouse.shortcuts import RetryOperationalError
import json


from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type %s not serializable" % type(obj))

class VARDBBase(Model):
    def __str__(self):
        return json.dumps(self._data,default=json_serial)

    def __repr__(self):
        return self.__str__()

sqldb =  Proxy() 

def connect_to_db(database='vardb',user='root',password='',engine=MySQLDatabase):
    class MyRetryDB(RetryOperationalError, engine):
        pass
    from VARDB.Effect import Effect
    from VARDB.Allele import DeferredEffect
    DeferredEffect.set_model(Effect)
    mysqldb = MyRetryDB(database, user=user, password=password)
    sqldb.initialize(mysqldb)
    
    