# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

from peewee import ForeignKeyField, Model, IntegerField
from VARDB.ProgramRun import ProgramRun

from  VARDB.VariantCollection import mysql_db
        

class Alignment(Model):
    
    
    aln_run =  ForeignKeyField(ProgramRun, related_name='alignments', 
                                          db_column="run_fk") 
    seqs_count = IntegerField(default=1)
    class Meta:
        database = mysql_db


if __name__ == '__main__':
    ""
        
    Alignment.create_table()
          
