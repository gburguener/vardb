'''
Created on May 26, 2017

@author: esosa

hgvs.parser is used to parse http://varnomen.hgvs.org/

'''

import vcf
import hgvs.parser



class SnpeffEffect():
    hgvsparser = hgvs.parser.Parser()
    
    def __init__(self,alt, effects, impact, gene, geneid, feature_type, feature_id, 
                 transcript_biotype, rank_div_total, hgvs_c, hgvs_p, c_dna_pos, 
                 cds_pos, aa_pos, dist_to_feature, errors,
                 aa_len):
        self.alt =  alt
        self.effects = effects
        self.impact = impact
        self.gene = gene
        self.geneid = geneid
        self.feature_type = feature_type
        self.feature_id = feature_id
        self.transcript_biotype = transcript_biotype
        self.rank_div_total = rank_div_total
        self.hgvs_c = hgvs_c
        self.hgvs_p = hgvs_p
        self.c_dna_pos = c_dna_pos
        self.cds_pos = cds_pos
        self.aa_pos = aa_pos
        self.dist_to_feature = dist_to_feature
        self.errors = errors
        self.aa_len = aa_len
        if self.hgvs_p:
            self.aa_ref = self.hgvs_p.pos.start.aa
            self.aa_mut = self.hgvs_p.edit.alt

    @classmethod
    def read(cls,ann_str):
        
        aa_pos,aa_len = (None,None)
        (alt, effects, impact, gene, geneid, feature_type, feature_id, transcript_biotype, 
            rank_div_total, hgvs_c, hgvs_p, c_dna_pos, cds_pos, (aa_pos_aa_len), dist_to_feature, errors) = ann_str.split("|")       
        effects = effects.split("&")
        if aa_pos_aa_len: 
            aa_pos,aa_len = aa_pos_aa_len.split("/")
            aa_pos = int(aa_pos)
        hgvs_c =  cls.hgvsparser.parse_hgvs_variant("xx:" + hgvs_c ).posedit    
        if hgvs_p:
            hgvs_p =  cls.hgvsparser.parse_hgvs_variant("xx:" + hgvs_p ).posedit
        else: 
            hgvs_p = None
        
        return SnpeffEffect(alt, effects, impact, gene, geneid, feature_type, feature_id, transcript_biotype, 
            rank_div_total, hgvs_c, hgvs_p, c_dna_pos, cds_pos, aa_pos, dist_to_feature, errors,aa_len)

class VcfSnpeffIO():

    
    @classmethod
    def parse(cls,vcf_path):
        if hasattr(vcf_path, "read"):
            h = vcf_path
        else:
            h =  open(vcf_path)
        
        try:
            variantes = vcf.VCFReader(h)
            for v in variantes:                
                yield (v, [SnpeffEffect.read(x) for x in v.INFO["ANN"]] 
                            if "ANN" in v.INFO else []) 
        finally:
            h.close()
    