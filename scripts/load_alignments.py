'''
Created on Jun 16, 2017

@author: eze
'''

import argparse
from VARDB.Aln2Sql import Aln2Sql


if __name__ == '__main__':
    
#     parser = argparse.ArgumentParser(description='load an aligment to the database')
#     parser.add_argument('-t','--aln_type',choices=parser_choises,  help='input format of the alignment')
#     parser.add_argument('-i','--input',help='input file' )
#     
#     args = parser.parse_args()
#     
#     if not os.path.exists(args.input):
#         print "input file %s does not exists"
    pr = Aln2Sql.load_run("/data/projects/Staphylococcus/annotation/uniprot/sp_blast.xml", "blast-xml")
    print pr.id
    
    