'''
Created on Jun 27, 2017

@author: eze
'''
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VariantCollection import VariantCollection
from VARDB import connect_to_db, sqldb
from VARDB.Effect import Effect
from VARDB.Allele import Allele
from VARDB.VariantAnnotation import VariantAnnotation
import MySQLdb


"""
gene filter
quality filter
has,hasnt

"""

start_idx = 5
step_sample = 3

class SameFilter(object):
    
    def __init__(self, *vcs):
        self.vcs = vcs
        
    
    def filter(self,xtuple,samples):
        idxs = [ [i for i,s in enumerate(samples) if s.id == vc.id][0]
                 for vc in self.vcs
               ]
        
        return len(set( [xtuple[start_idx+step_sample*idx] for idx in idxs ]   ) ) == 1  

class SubtractFilter(object):
    
    def __init__(self, *vcs):
        self.vcs = vcs
        
    
    def filter(self,xtuple,samples):
        idxs = [ [i for i,s in enumerate(samples) if s.id == vc.id][0]
                 for vc in self.vcs
               ]
        total_alleles = set([ xtuple[start_idx+step_sample*idx] for idx in range(len(samples)) ]) 
        alleles_to_remove = set([ xtuple[start_idx+step_sample*idx] for idx in idxs ]) 
        return  len ( total_alleles - alleles_to_remove ) != 0        
  

class EffectFilter(object):
    
    def __init__(self, variant_type):
        self.variant_type = variant_type
        
    
    def filter(self,xtuple,samples):
        
        return any(  [ xtuple[ start_idx+step_sample * idx + 2]  == self.variant_type  
                      for idx in range(len(samples))     ] )        

class VariantFilter(object):
    
    def __init__(self, gene_list):
        self.gene_list = gene_list
        
    
    def filter(self,xtuple,samples):
        
        return xtuple[3] in self.gene_list 




class QueryBuilder(object):
    '''
    classdocs
    '''
    
    missense = None
    
    @classmethod
    def genes(cls, *genes):
        pass
    
    @classmethod
    def genes_from(cls, tbdream):
        pass

    template_select = """
        SELECT v.contig AS contig,v.pos AS pos,v.ref AS ref,v.gene AS gene,v.gene_pos AS gene_pos,
        {fields} 
        FROM    variant v
        {joins}
        """
    template_join = """
    LEFT OUTER JOIN variantassignment va{num} ON va{num}.variant_fk = v.id AND va{num}.variant_collection_fk = {variant_col_id}
    LEFT OUTER JOIN allele a{num} ON va{num}.allele_fk = a{num}.id
    LEFT OUTER JOIN effect e{num} ON e{num}.id = a{num}.main_effect_fk 
    """

    def __init__(self,variant_collection=None):
        if variant_collection:
            assert isinstance(variant_collection, VariantCollection)
            self.samples = [variant_collection]
        else:
            self.samples = []
        self.filters = []
       

    
    
    def build_sql(self):
        fields = ""
        joins = ""
        
        for i,sample in enumerate(self.samples):
            fields +=  "a{num}.alt,ifnull(e{num}.aa_alt,v.ref),e{num}.variant_type,".format(num=i)

            joins +=  QueryBuilder.template_join.format(
                variant_col_id=sample.id,num=i
            )
        fields = fields[:-1]
        
        
        sql = QueryBuilder.template_select.format(
            fields = fields, joins = joins
        )
        return sql
    
    def tuples(self):
        sql = self.build_sql() 
    
        cursor = sqldb.execute_sql( sql)
        res = []
        for x in cursor.fetchall():
            if all([f.filter(x,self.samples) for f in  self.filters ]):
                res.append(x)
        return res 
            
    
#     def __and__(self, other):        
#         assert isinstance(other, VariantCollection)
#         self.pipe.append( StepAnd(other) )     
#         return self
#     
#     def __or__(self, other):
#         
#         assert isinstance(other, StepPipe)
#         self.pipe.append( other )     
#         return self
#     
#     def __add__(self, other):
#         
#         assert isinstance(other, VariantCollection)
#         self.pipe.append( StepAdd(other) )     
#         return self
#     
#     def __sub__(self, other):
#         assert isinstance(other, VariantCollection)
#         self.pipe.append( StepSub(other) )     
#         return self   
    
    def build(self):
        
        cond = None
        q = VariantAssignment.select().join(VariantCollection)
        for step in self.pipe:
            step.join(q)
        
        for step in self.pipe:
            step.where(cond)
        
        return q

if __name__ == '__main__':
    connect_to_db(database="vardb2",  password="mito")
    
    
    qb = QueryBuilder(VariantCollection.select().where(VariantCollection.sample == "1109_S1_L001").get())
    
    qb.samples.append( VariantCollection.select().where(VariantCollection.sample == "2003_S4_L001").get() )
    for x in qb.tuples():
        print(x)

   
    
    

    
    
    
    





        