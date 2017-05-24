# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:43:43 2017

@author: gburguener
"""


import os
import sys
from peewee import *

sys.path.append("/home/gburguener/Documentos/Academico/WORK_UBA/Pipelines/vardb/")

from  VARDB.Variant import *

mysql_db = MySQLDatabase('vardb', user='root', passwd='root')

class Allele(Model):
    variant =  ForeignKeyField(Variant, related_name='alleles', 
                                          db_column="variant_fk")  
    alt = CharField()
       
    qual = FloatField()
    evidence = CharField()
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    Allele.create_table()