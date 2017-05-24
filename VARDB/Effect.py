# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:45:46 2017

@author: gburguener
"""

import os
import sys
from peewee import *

sys.path.append("/home/gburguener/Documentos/Academico/WORK_UBA/Pipelines/vardb/")

from  VARDB.Allele import *

mysql_db = MySQLDatabase('vardb', user='root', passwd='root')

class Effect(Model):
    allele =  ForeignKeyField(Variant, related_name='effects', 
                                          db_column="allele_fk")  
    
    transcript = CharField()
    variant_type = CharField() #SO term, inherited from SO variant type.
    reported = BooleanField()
    predicted_impact = CharField() 
    aa_ref = CharField()
    aa_pos = IntegerField()
    aa_alt = CharField() 
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    Allele.create_table()