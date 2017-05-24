# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:27:42 2017

@author: gburguener
"""


import os
import sys
from peewee import *

sys.path.append("/home/gburguener/Documentos/Academico/WORK_UBA/Pipelines/vardb/")

from  VARDB.Effect import *

mysql_db = MySQLDatabase('vardb', user='root', passwd='root')

class VariantAnnotation(Model):
    effect =  ForeignKeyField(Variant, related_name='annotations', 
                                          db_column="effect_fk")  
    source_type = CharField() #DB, prediccion, bibliografia
    source = CharField()
    prop = CharField()
    value = CharField()
    description = CharField()
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    Allele.create_table()