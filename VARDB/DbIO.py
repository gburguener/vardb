'''
Created on Jun 22, 2017

@author: eze
'''
from VARDB.VariantCollection import VariantCollection
from VARDB.VcfSnpeffIO import VcfSnpeffIO
from VARDB.Variant import Variant
from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Allele import DeferredEffect
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB import sqldb


DeferredEffect.set_model(Effect)

class VariantCollectionExistsError(Exception):
    
    def __init__(self, ref_organism, sample):
        self.ref_organism = ref_organism
        self.sample = sample
    
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    
    def __str__(self):
        return "Ref: %s Sample %s already exists" % (self.ref_organism, self.sample)
    

class MultipleSamplesError(Exception):
    
    def __init__(self, vcf, samples):
        self.vcf = vcf
        self.samples = samples
        
    
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    
    def __str__(self):
        return "only vcfs with one sample are accepted, '%s' has %i: %s" % (
            self.vcf, len(self.samples), ", ".join(self.samples))


class DbIO(object):
    '''
    classdocs
    '''
    
    tables = [VariantCollection,   Variant,Allele,VariantAssignment,VariantAnnotation,  Effect] 
    
    def create_db(self):
        
        for t in reversed( DbIO.tables):
            if t.table_exists():
                t.drop_table()
        
        
        for t in DbIO.tables:            
            t.create_table()
        sqldb.create_foreign_key(Allele, Allele.main_effect)
    


    def add_variant(self, ref_organism, vc, var, effects):
        variant_query = Variant.select().where(
            (Variant.pos == var.POS) & (Variant.contig == var.CHROM) & (Variant.ref_organism == ref_organism) & (Variant.ref == var.REF))
        if not variant_query:
            new_variant = Variant(contig=var.CHROM, pos=var.POS, ref=var.REF, ref_organism=ref_organism)
            new_variant.save()
        else:
            new_variant = variant_query.get()
        for alt in var.ALT:
            allele_query = Allele.select().join(Variant).where((Allele.variant == new_variant) & (Allele.alt == alt))
            if not allele_query:
                new_allele = Allele(variant=new_variant, alt=alt)
                new_allele.save()
                first = True
                for effect in effects:
                    
                    new_effect = Effect(allele=new_allele, transcript=effect.gene, variant_type="|".join(effect.annotation))
                    if effect.aa_pos:
                        new_effect.aa_pos = effect.aa_pos
                        new_effect.aa_ref = effect.aa_ref
                        new_effect.aa_alt = effect.aa_alt
                    new_effect.save()
                    if not new_variant.gene:
                        new_variant.gene = effect.gene
                        new_variant.gene_pos = effect.gene_pos
                        new_variant.save()
                        
                    if first:
                        new_allele.main_effect = new_effect
                        new_allele.save()
                        first = False
            
            else:
                new_allele = allele_query.get()
            assignment = VariantAssignment(variant_collection=vc, variant=new_variant, allele=new_allele)
            assignment.save()
            
            for k, v in var.samples[0].data._asdict().items():
                val = "|".join(map(str, v)) if isinstance(v, (list, tuple)) else  str(v)
                VariantAnnotation(
                source_type="prediction" , source="VC",
                assignment=assignment, prop=k, value=val).save()
            
            qual_va = VariantAnnotation(
                source_type="prediction" , source="VC",
                assignment=assignment, prop="qual", value=var.QUAL)
            qual_va.save()
        
        

    def exists_sample(self, ref_organism, sample):
        return bool(VariantCollection.select().where(
            (VariantCollection.sample == sample) 
            & (VariantCollection.ref_organism == ref_organism)
            ).count())
    
    def delete_sample(self, ref_organism, sample):
        return  VariantCollection.select().where(
            (VariantCollection.sample == sample) 
            & (VariantCollection.ref_organism == ref_organism)).get().delete_instance(recursive=True)
            
    

    def load_variants(self, variants, ref_organism, sample):
        '''
        variants: array of (variant,effects ) tuple
        '''
        
        if self.exists_sample(ref_organism, sample):
            raise VariantCollectionExistsError(ref_organism, sample)
        
        vc = VariantCollection(ref_organism=ref_organism, sample=sample)
        vc.save()
         
        for var, effects in variants:
            
            self.add_variant(ref_organism, vc, var, effects)
            

    def load_vcf(self, vcf, ref_organism, sample=None):
        with open(vcf) as h:
            variant = next(vcf.VCFReader(h).iter())
            if variant.samples.length > 1:
                raise MultipleSamplesError(vcf, [s.sample for s in variant.samples])
            if not sample:
                sample = variant.samples[0].sample
        self.load_variants(VcfSnpeffIO.parse(vcf), ref_organism, sample)
        
        
        
        
