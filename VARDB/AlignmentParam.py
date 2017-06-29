# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:31:20 2017

@author: gburguener
"""

from peewee import ForeignKeyField, Model, CharField, FloatField


from  VARDB.VariantCollection import sqldb
from VARDB.Alignment import Alignment
 
        

class AlignmentParam(Model):
      
    aln =  ForeignKeyField(Alignment, related_name='params', 
                                          db_column="alignment_fk") 
    name = CharField()
    value = FloatField()
    
    class Meta:
        database = sqldb


if __name__ == '__main__':
    ""
        
    AlignmentParam.create_table()
          
