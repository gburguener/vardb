
from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Variant import Variant
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB.VariantCollection import VariantCollection
from VARDB.VariantAssignment import VariantAssignment




if __name__ == '__main__':    
    tables = [VariantCollection,   Variant,Allele,VariantAssignment,VariantAnnotation,  Effect]
    for t in reversed( tables):
        if t.table_exists():
            t.drop_table()
    
    
    for t in tables:
        print t
        t.create_table()
        print "--"
    
    print "OK"


