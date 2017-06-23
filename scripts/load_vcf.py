from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Variant import Variant
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB.VariantCollection import VariantCollection
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VcfSnpeffIO import VcfSnpeffIO
import argparse
import os
import vcf
from VARDB.DbIO import DbIO
from VARDB import connect_to_db




if __name__ == '__main__':  
    
    parser = argparse.ArgumentParser(description='load a vcf to the database')
    parser.add_argument('-vcf', help='vcf path. The file must contain only one sample',required=True)
    parser.add_argument('-ref', '--reference',help='reference used for the alignment',required=True)
    parser.add_argument('-s', '--sample', help='sample name, it is extracted from the vcf by default', default=None)
    
    
    parser.add_argument('--dbuser', default='root')
    parser.add_argument('--dbpass', default='')
    parser.add_argument('--database', default='vardb')
     
    args = parser.parse_args()
     
    if not os.path.exists(args.vcf):
        print "input file %s does not exists" % args.vcf
    
    connect_to_db(database=args.database, user=args.dbuser, password=args.dbpass)
    
    ref_organism = args.reference
    
    db = DbIO()
    
    db.load_vcf(args.vcf, args.reference, args.sample)
   
