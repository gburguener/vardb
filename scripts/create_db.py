
from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Variant import Variant
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB.VariantCollection import VariantCollection
from VARDB.VariantAssignment import VariantAssignment
from VARDB.Alignment import Alignment
from VARDB.AlignmentParam import AlignmentParam
from VARDB.AlnLine import AlnLine
from VARDB.ProgramRun import ProgramRun
from VARDB.ProgramParameter import ProgramParameter




if __name__ == '__main__': 
       
    tables = [VariantCollection,   Variant,Allele,VariantAssignment,VariantAnnotation,  Effect,
              ProgramRun,ProgramParameter,Alignment,AlnLine,AlignmentParam
              
              ]
    for t in reversed( tables):
        if t.table_exists():
            t.drop_table()
    
    
    for t in tables:
        print t
        t.create_table()
        print "--"
    
    print "OK"


