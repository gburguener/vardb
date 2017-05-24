# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:02:26 2017

@author: gburguener
"""

from peewee import *

mysql_db = MySQLDatabase('vardb', user='root', passwd='root')

class VariantCollection(Model):
    ref = CharField()
    sample = CharField()
    description = CharField()    
    modified_date = DateField()

    class Meta:
        database = mysql_db 
        
        
if __name__ == '__main__':
    VariantCollection.create_table()
          
