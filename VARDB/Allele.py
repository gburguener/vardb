# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:43:43 2017

@author: gburguener
"""


import os
import sys
from peewee import ForeignKeyField, Model, CharField, FloatField
from VARDB.Variant import Variant
from VARDB import mysql_db




class Allele(Model):
    variant =  ForeignKeyField(Variant, related_name='alleles', 
                                          db_column="variant_fk")  
    alt = CharField()
       
  
    
    class Meta:
        database = mysql_db
        
        
if __name__ == '__main__':
    Allele.create_table()