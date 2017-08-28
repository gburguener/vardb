'''
Created on Jun 27, 2017

@author: eze
'''
import unittest

from VARDB import  connect_to_test_db,  disconnect
from VARDB.Allele import Allele
from VARDB.DbIO import DbIO
from VARDB.Effect import Effect
from VARDB.Query.QueryBuilder import QueryBuilder, SameFilter, SubtractFilter, \
    EffectFilter, VariantFilter
from VARDB.Variant import Variant
from VARDB.VariantAssignment import VariantAssignment
from VARDB.VariantCollection import VariantCollection


class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect_to_test_db()
        
        for t in DbIO.tables:            
            t.create_table()
        cls.create_data()
        
    @classmethod
    def tearDownClass(cls):
        disconnect()
        
        
    @classmethod
    def create_data(cls):
        ref_org = "X"  
        v1 = Variant(pos=10, gene="pkng", contig="C1", ref_organism=ref_org, ref="A") 
        v1.save()
        v2 = Variant(pos=20, gene="pkng", contig="C1", ref_organism=ref_org, ref="C") 
        v2.save()       
        v3 = Variant(pos=30, gene="pepe", contig="C1", ref_organism=ref_org, ref="G") 
        v3.save()
        v4 = Variant(pos=40, gene="juan", contig="C1", ref_organism=ref_org, ref="T") 
        v4.save()
        v5 = Variant(pos=50, gene="tito", contig="C1", ref_organism=ref_org, ref="A") 
        v5.save()
        v6 = Variant(pos=60, gene="tito", contig="C1", ref_organism=ref_org, ref="C") 
        v6.save()
         
        # main_effect
        a1_1 = Allele(variant=v1, alt="C")
        a1_1.save()
         
        a1_2 = Allele(variant=v2, alt="G")
        a1_2.save()
        a2_2 = Allele(variant=v2, alt="T")
        a2_2.save()
         
        a1_3 = Allele(variant=v3, alt="C")
        a1_3.save()
        a2_3 = Allele(variant=v3, alt="T")
        a2_3.save()
        a3_3 = Allele(variant=v3, alt="A")
        a3_3.save()
         
        a1_4 = Allele(variant=v4, alt="C")
        a1_4.save()
         
        a1_5 = Allele(variant=v5, alt="G")
        a1_5.save()
        a2_5 = Allele(variant=v5, alt="T")
        a2_5.save()
         
        a1_6 = Allele(variant=v6, alt="G")
        a1_6.save()
        a2_6 = Allele(variant=v6, alt="T")
        a2_6.save()
        a3_6 = Allele(variant=v6, alt="A")
        a3_6.save()
         
        #-------------
        e1_1 = Effect(allele=a1_1, variant_type="missense_variant", predicted_impact="HIGH",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e1_1.save()
         
        e1_2 = Effect(allele=a1_2, variant_type="missense_variant", predicted_impact="MODERATE",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G") 
        e1_2.save()
        e2_2 = Effect(allele=a2_2, variant_type="synonymous_variant", predicted_impact="LOW",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e2_2.save()
         
        e1_3 = Effect(allele=a1_3, variant_type="missense_variant", predicted_impact="MODERATE",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e1_3.save()
        e2_3 = Effect(allele=a2_3, variant_type="synonymous_variant", predicted_impact="LOW",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e2_3.save()
        e3_3 = Effect(allele=a3_3, variant_type="missense_variant", predicted_impact="MODERATE",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e3_3.save()
         
        e1_4 = Effect(allele=a1_4, variant_type="frameshift_variant", predicted_impact="MODERATE")
        e1_4.save()
         
        e1_5 = Effect(allele=a1_5, variant_type="missense_variant", predicted_impact="MODERATE",
                      aa_ref="L", aa_pos="10",
                      aa_alt="G")
        e1_5.save()
        e2_5 = Effect(allele=a2_5, variant_type="stop_gained", predicted_impact="HIGH",
                      aa_ref="L", aa_pos="10",
                      aa_alt="*")
        e2_5.save()
         
        e1_6 = Effect(allele=a1_6, variant_type="upstream_gene_variant", predicted_impact="LOW")
        e1_6.save()
        e2_6 = Effect(allele=a2_6, variant_type="upstream_gene_variant", predicted_impact="LOW")
        e2_6.save()
        e3_6 = Effect(allele=a3_6, variant_type="upstream_gene_variant", predicted_impact="LOW")
        e3_6.save()
        
        a1_1.main_effect = e1_1
        a1_1.save()
        a1_2.main_effect = e1_2
        a1_2.save()
        a2_2.main_effect = e2_2
        a2_2.save()        
        a1_3.main_effect = e1_3
        a1_3.save()
        a2_3.main_effect = e2_3
        a2_3.save()        
        a3_3.main_effect = e3_3
        a3_3.save()
        
        a1_4.main_effect = e1_4
        a1_4.save()
        a1_5.main_effect = e1_5
        a1_5.save()
        a2_5.main_effect = e2_5
        a2_5.save()
        a1_6.main_effect = e1_6
        a1_6.save()
        a2_6.main_effect = e2_6
        a2_6.save()
        a3_6.main_effect = e3_6
        a3_6.save()
        
         
         
        vc1 = VariantCollection(ref_organism=ref_org, sample="A")        
        vc1.save()
        vc2 = VariantCollection(ref_organism=ref_org, sample="B")
        vc2.save()        
        vc3 = VariantCollection(ref_organism=ref_org, sample="C")
        vc3.save()
        tbdream = VariantCollection(ref_organism=ref_org, sample="tbdream")
        tbdream.save()
        
         
        va = VariantAssignment(variant_collection=vc1 , variant=v1 , allele=a1_1)
        va.save()
        va = VariantAssignment(variant_collection=vc2 , variant=v1 , allele=a1_1)
        va.save()        
        va = VariantAssignment(variant_collection=tbdream , variant=v1 , allele=a1_1)
        va.save()
         
        va = VariantAssignment(variant_collection=vc1 , variant=v2 , allele=a1_2)
        va.save()
        va = VariantAssignment(variant_collection=vc2 , variant=v2 , allele=a2_2)
        va.save()
        va = VariantAssignment(variant_collection=vc3 , variant=v2 , allele=a2_2)
        va.save()
         
        va = VariantAssignment(variant_collection=vc1 , variant=v3 , allele=a1_3)
        va.save()
        va = VariantAssignment(variant_collection=vc2 , variant=v3 , allele=a2_3)
        va.save()
        va = VariantAssignment(variant_collection=vc3 , variant=v3 , allele=a3_3)
        va.save()
        va = VariantAssignment(variant_collection=tbdream , variant=v3 , allele=a3_3)
        va.save()
         
         
        va = VariantAssignment(variant_collection=vc2 , variant=v4 , allele=a1_4)
        va.save()
         
         
        va = VariantAssignment(variant_collection=vc1 , variant=v5 , allele=a2_5)
        va.save()
        va = VariantAssignment(variant_collection=vc2 , variant=v5 , allele=a1_5)
        va.save()
        
         
        va = VariantAssignment(variant_collection=vc1 , variant=v6 , allele=a1_6)
        va.save()
        va = VariantAssignment(variant_collection=vc2 , variant=v6 , allele=a1_6)
        va.save()
        va = VariantAssignment(variant_collection=vc3 , variant=v6 , allele=a1_6)
        va.save()
        va = VariantAssignment(variant_collection=tbdream , variant=v6 , allele=a2_6)
        va.save()
        
    def setUp(self):
        self.db = DbIO()
        ref_org = "X"          
        
        self.vc1 = VariantCollection.get((VariantCollection.ref_organism==ref_org) & (VariantCollection.sample=="A"))        
        self.vc2 = VariantCollection.get((VariantCollection.ref_organism==ref_org) & (VariantCollection.sample=="B"))
        self.vc3 = VariantCollection.get((VariantCollection.ref_organism==ref_org) & (VariantCollection.sample=="C"))
      
    def tearDown(self):
        pass

    def test_instersect_list(self):
#         vars = self.vc1 & self.vc2
        qb = QueryBuilder(self.vc1)
        qb.samples.append(self.vc2)
        qb.filters.append( SameFilter(self.vc1,self.vc2) )
        # a1_1 / a1_6        
        
        self.assertEqual(2,len(qb.tuples()))
            # contig, pos, ref, gene, gene_pos,           
                
        
#         vars = self.vc1 & self.vc2 & self.vc3
        qb = QueryBuilder(self.vc1)
        qb.samples.append(self.vc2)
        qb.samples.append(self.vc3)
        qb.filters.append( SameFilter(self.vc1,self.vc2,self.vc3) )
        
        self.assertEqual(1,len(qb.tuples()))        
        # a1_6
        
    def test_has_hasnt_list(self):
#         vars = (self.vc1 & self.vc2) - self.vc3
        qb = QueryBuilder(self.vc1)
        qb.samples.append(self.vc2)
        qb.samples.append(self.vc3)
        qb.filters.append( SameFilter(self.vc1,self.vc2) )
        qb.filters.append( SubtractFilter(self.vc3) )
        
        self.assertEqual(1,len(qb.tuples()))
        self.assertEqual(10,qb.tuples()[0][1])
        # a1_1
        
     
    def test_missense_list(self):
#         vars = (self.vc1 + self.vc2 + self.vc3) | QueryBuilder.missense
        qb = QueryBuilder(self.vc1)
        qb.samples.append(self.vc2)
        qb.samples.append(self.vc3)
        
        qb.filters.append( EffectFilter("missense_variant") )
   
        self.assertEqual(4,len(qb.tuples()))
        #a1_5 a3_3 a1_3 a1_2 a1_1
     
 
#     def test_high_quality_snps(self):
#         pass
#     
    def test_gene_list(self):
#         vars = (self.vc1 + self.vc2 + self.vc3) | QueryBuilder.genes("pkng","pepe")
        qb = QueryBuilder(self.vc1)
        qb.samples.append(self.vc2)
        qb.samples.append(self.vc3)
        
        qb.filters.append( VariantFilter({"pkng":1,"pepe":1}) )
   
        self.assertEqual(3,len(qb.tuples()))
        self.assertEqual(60,sum([int(x[1]) for x in qb.tuples()] ) )
        # a1_1 a1_2 a2_2 a1_3 a2_3 a3_3
     
     
#     def test_gene_in_variant_collection(self):
#         vars = (self.vc1 + self.vc2 + self.vc3) | QueryBuilder.genes_from(self.tbdream)
          

        # tito pepe pkng ->   a1_1 a1_2 a2_2 a1_3 a2_3 a3_3 a1_5 a2_5 a1_6 
        
#         vars = (self.vc1 + self.vc2 + self.vc3 + self.tbdream) | QueryBuilder.genes_from(self.tbdream)
        # tito pepe pkng ->   a1_1 a1_2 a2_2 a1_3 a2_3 a3_3 a1_5 a2_5 a1_6 (a2_6)  
     
#     def test_all_filters(self):
#         vars = ((self.vc1 + self.vc2 + self.vc3) | QueryBuilder.missense | QueryBuilder.genes_from(self.tbdream)) - self.vc3
    
    

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
