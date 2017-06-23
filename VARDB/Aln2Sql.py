'''
Created on Jun 16, 2017

@author: eze
'''

import Bio.SearchIO as bpsio
import Bio.AlignIO as bpaio
import os
from VARDB.ProgramRun import ProgramRun
from VARDB.Alignment import Alignment
from VARDB.AlnLine import AlnLine
from VARDB.AlignmentParam import AlignmentParam
from VARDB.ProgramParameter import ProgramParameter
from VARDB import mysql_db

parser_choises = bpsio._ITERATOR_MAP.keys() + bpaio._FormatToIterator.keys()

class Aln2Sql(object):
    '''
    classdocs
    '''

    @staticmethod
    def load_run(file_name,file_format,name="",description=""):
        pr = ProgramRun(description=description,format=file_format,name=name)
        pr.save()
        first = True
        if file_format in bpsio._ITERATOR_MAP:
            for query_result in bpsio.parse(file_name, file_format) :
                with mysql_db.atomic():
                    if first:
                        first = False
                        if hasattr(query_result, "program"):
                            pr.program = query_result.program
                            pr.save()
                        for x in  ["version","target","reference","param_filter","param_matrix","param_evalue_threshold"]:
                            if hasattr(query_result, x):
                                ProgramParameter(run=pr,name=x,value=str(  getattr(query_result, x) )).save()
                    hits = list(query_result)
                    if hits:
                        seqs_count = 2
                        for hit in hits:
                            for hsp in hit:                                
                                aln = Alignment(aln_run=pr)
                                aln.seqs_count = seqs_count
                                aln.save()
                                AlnLine(alignment=aln,name=hsp.query_id,
                                        seq=str(hsp.aln[0].seq),
                                        start=hsp.query_start,
                                        end=hsp.query_end).save()
                                AlnLine(alignment=aln,name=hsp.hit_id,
                                        seq=str(hsp.aln[1].seq),
                                        start=hsp.hit_start,
                                        end=hsp.hit_end).save()
                                
                                AlignmentParam(aln=aln,name="evalue",value=hsp.evalue).save()
                                
                                
                                
                                if all([ hasattr(hsp, x) for x in ["ident_num","aln_span"]]):
                                    AlignmentParam(aln=aln,name="identity",value=1.0 * hsp.ident_num / hsp.aln_span ).save()
                                
                                if hasattr(query_result, "seq_len"):
                                    AlignmentParam(aln=aln,name="qlen",value=query_result.seq_len).save()
                                    if hasattr(hsp, "query_span"):
                                        AlignmentParam(aln=aln,name="query_coverage",value=1.0 * hsp.query_span / query_result.seq_len).save()
                                
                                if hasattr(hit, "seq_len"):
                                    AlignmentParam(aln=aln,name="hlen",value=hit.seq_len).save()
                                    if hasattr(hsp, "hit_span"):
                                        AlignmentParam(aln=aln,name="hit_coverage",value= 1.0 * hsp.hit_span / hit.seq_len).save()
                                        
                                if hasattr(hsp, "query_strand"):
                                    AlignmentParam(aln=aln,name="query_strand",value=hsp.query_strand).save()
                                if hasattr(hsp, "hit_strand"):
                                    AlignmentParam(aln=aln,name="hit_strand",value=hsp.hit_strand).save()
                                
                                
                    else:
                        aln = Alignment(aln_run=pr)
                        aln.save()
                        AlnLine(alignment=aln,name=query_result.id).save()
                    
        else:
            pass
        return pr

    
    @staticmethod
    def exists( program_run_name):
        return ProgramRun.select().where(ProgramRun.name == program_run_name ).count()
    
    
        