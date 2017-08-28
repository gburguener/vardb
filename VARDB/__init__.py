from datetime import date, datetime
import json

from peewee import MySQLDatabase, Model, SqliteDatabase
from peewee import Proxy
from playhouse.shortcuts import RetryOperationalError

import VARDB


__version__ = "0.0.1"


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
deferredEffectSetted = False


def wiredb(db):
    from VARDB.Effect import Effect
    from VARDB.Allele import DeferredEffect
    if not VARDB.deferredEffectSetted:
        DeferredEffect.set_model(Effect)
        VARDB.deferredEffectSetted = True
    sqldb.initialize(db)

def connect_to_db(database='vardb',user='root',password='',engine=MySQLDatabase):
    class MyRetryDB(RetryOperationalError, engine):
        pass
    db = MyRetryDB(database, user=user, password=password)
    wiredb(db)

def connect_to_test_db():
    db = SqliteDatabase(":memory:")  
    wiredb(db)

def disconnect():
    VARDB.sqldb.close()    
    
    
    