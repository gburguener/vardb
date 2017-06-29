# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:02:26 2017

@author: gburguener
"""


from VARDB import sqldb, VARDBBase
import datetime
from peewee import CharField,  DateTimeField






class VariantCollection(VARDBBase):
    ref_organism = CharField()
    sample = CharField()
    description = CharField(null=True)    
    modified_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            (('ref_organism', 'sample'), True),

        )
        database = sqldb 
    
    def __and__(self, other):
        from VARDB.Query.QueryBuilder import QueryBuilder
        assert self.ref_organism == other.self.ref_organism
        qb = QueryBuilder(self) & other                
        return qb
    
    def __or__(self, other):
        from VARDB.Query.QueryBuilder import QueryBuilder
        assert self.ref_organism == other.self.ref_organism
        qb = QueryBuilder(self) | other                
        return qb
    
    def __add__(self, other):
        from VARDB.Query.QueryBuilder import QueryBuilder
        assert self.ref_organism == other.self.ref_organism
        qb = QueryBuilder(self) + other                
        return qb
    
    def __sub__(self, other):
        from VARDB.Query.QueryBuilder import QueryBuilder
        assert self.ref_organism == other.self.ref_organism
        qb = QueryBuilder(self) - other                
        return qb
     
        
if __name__ == '__main__':
    VariantCollection.create_table()
          
