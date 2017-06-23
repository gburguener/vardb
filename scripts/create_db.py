
from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Variant import Variant
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB.VariantCollection import VariantCollection
from VARDB.VariantAssignment import VariantAssignment

from VARDB import connect_to_db
from VARDB.DbIO import DbIO
import argparse
from VARDB.Alignment import Alignment
from VARDB.AlignmentParam import AlignmentParam
from VARDB.AlnLine import AlnLine
from VARDB.ProgramRun import ProgramRun
from VARDB.ProgramParameter import ProgramParameter






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='load a vcf to the database')
    parser.add_argument('--dbuser', default='root')
    parser.add_argument('--dbpass', default='')
    parser.add_argument('--database', default='vardb')     
    args = parser.parse_args()
      
    connect_to_db(database=args.database, user=args.dbuser, password=args.dbpass)  
       
   
    DbIO().create_db()
    
    print "OK"


