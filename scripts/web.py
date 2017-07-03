'''
Created on Jun 29, 2017

@author: eze
'''

import re

from bottle import route, run, template, get, request
from VARDB import connect_to_db
from VARDB.Variant import Variant
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VariantCollection import VariantCollection
from VARDB.Query.QueryBuilder import QueryBuilder, SameFilter, SubtractFilter,\
    EffectFilter, VariantFilter



connect_to_db("test",  password="mito")
regepx = r"[_ \-]"

mappings = {
}


@get('/variants/<ref>/<sample>')
def variants(ref,sample):
    try:
        vc = VariantCollection.get(VariantCollection.sample == sample)
        variants = Variant.select().join(VariantAssignment).where((Variant.ref_organism ==ref) & 
                                  (VariantAssignment.variant_collection == vc) )
        res = []
        for v in variants:
            x = v._data
            x["modified_date"] = str(x["modified_date"])
            res.append(x)
        #print variants[0]._data
        return { "jojo": res, "count": len(variants)}
    except:
        return "NO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

@get('/query/<ref>')
def query(ref):
    
        
        
    
    if 'samples' in request.query:
        qb = QueryBuilder()
        operators = re.findall(regepx,request.query['samples'])
        samplesStr = re.split(regepx, request.query['samples'])
        samples = []
        for sample in  samplesStr:
            vc = VariantCollection.get(
                (VariantCollection.ref_organism==ref) &
                (VariantCollection.sample==sample) 
                )   
            samples.append(vc)          
            qb.samples.append(vc) # ver de no agregar repetidos
        for i,op in enumerate(operators):
            if op == "_":
                qb.filters.append( SameFilter(samples[i],samples[i+1]) )
            elif op == "-":
                qb.filters.append( SubtractFilter(samples[i+1]) )
        
        if 'filters' in request.query:
            operators = request.query['filters'].split("-")
            for op in operators:
                if op.startswith("effect"):
                    qb.filters.append( EffectFilter(op.split("=")[1]) )  
                if op.startswith("genes"):
                    qb.filters.append( VariantFilter(op.split("=")[1].split(",")) )  
        
        
        return {"res": list(qb.tuples()) }  
        
    else:
        return "NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

@get('/<ref>')
def index(ref):
    return template('index',name=query(ref)["res"])

@get('/')
def index2():
    return template('index2')

run(host='localhost', port=8080)



