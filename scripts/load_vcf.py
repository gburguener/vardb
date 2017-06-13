from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.Variant import Variant
from VARDB.VariantAnnotation import VariantAnnotation
from VARDB.VariantCollection import VariantCollection
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VcfSnpeffIO import VcfSnpeffIO




if __name__ == '__main__':  
    ref_organism = "H37rv" 
    vc = VariantCollection(ref_organism=ref_organism, sample="1109_S1")
    vc.save()
     
    for var, effects in VcfSnpeffIO.parse("/data/projects/PiuriTB/analysis/variant_call_h37/1109_S1_L001/variants.ann.vcf"):
        variant_query = Variant.select().where( (Variant.pos == var.POS) 
                                               & (Variant.contig == var.CHROM) 
                                               & (Variant.ref_organism == ref_organism) 
                                               & (Variant.ref == var.REF) )
        
        if not variant_query:            
            new_variant = Variant(contig=var.CHROM, pos=var.POS, ref=var.REF, ref_organism=ref_organism)
            new_variant.save()
        else:
            new_variant = variant_query.get()
        
        for alt in var.ALT:
            allele_query = Allele.select().join(Variant).where(Allele.alt==alt)
            if not allele_query:
                new_allele = Allele(variant=new_variant,alt=alt)
                new_allele.save()
                
                for effect in effects:
                    new_effect = Effect(transcript=effect.gene,variant_type="|".join( effect.annotation) )
                    if effect.aa_pos:
                        new_effect.aa_pos = effect.aa_pos
                        new_effect.aa_ref = effect.aa_ref
                        new_effect.aa_mut = effect.aa_mut
                    
                    new_effect.save()
                    if not new_variant.gene:
                        new_variant.gene = effect.gene
                        new_variant.gene_pos = effect.gene
                        
                    
                    
            else:
                new_allele= allele_query.get()
            
            assignment = VariantAssignment(variant_collection=vc, variant=new_variant, allele=new_allele)
            assignment.save()
            qual_va = VariantAnnotation(assignment=assignment,prop="qual",value=var.QUAL)
            qual_va.save()
            
            
                
            
                    
        print var, effects
        break
    
