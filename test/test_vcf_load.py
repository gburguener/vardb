'''
Created on May 26, 2017

@author: eze
'''
import unittest

from VARDB.VcfSnpeffIO import VcfSnpeffIO
import StringIO
from VARDB.DbIO import DbIO, VariantCollectionExistsError
from VARDB import connect_to_db, sqldb
from VARDB.VariantCollection import VariantCollection
from VARDB.Variant import Variant
from VARDB.Allele import Allele
from VARDB.Effect import Effect
from VARDB.VariantAssignment import VariantAssignment



class TestVcfLoad(unittest.TestCase):
    
    missense = """
    NC_000962.3     14785   .       T       C       2020.0  .       AC=1;AF=1.00;AN=1;DP=77;FS=0.000;MLEAC=1;MLEAF=1.00;MQ=60.00;QD=26.23;SOR=0.772;ANN=C|missense_variant|MODERATE|Rv0012|Rv0012|transcript|Rv0012|protein_coding|1/1|c.697T>C|p.Cys233Arg|697/789|697/789|233/262||,C|upstream_gene_variant|MODIFIER|Rv0008c|Rv0008c|transcript|Rv0008c|protein_coding||c.-2474A>G|||||2474|,C|upstream_gene_variant|MODIFIER|Rv0010c|Rv0010c|transcript|Rv0010c|protein_coding||c.-1227A>G|||||1227|,C|upstream_gene_variant|MODIFIER|Rv0011c|Rv0011c|transcript|Rv0011c|protein_coding||c.-790A>G|||||790|,C|upstream_gene_variant|MODIFIER|trpG|Rv0013|transcript|Rv0013|protein_coding||c.-129T>C|||||129|,C|downstream_gene_variant|MODIFIER|gyrA|Rv0006|transcript|Rv0006|protein_coding||c.*4967T>C|||||4967|,C|downstream_gene_variant|MODIFIER|Rv0007|Rv0007|transcript|Rv0007|protein_coding||c.*3957T>C|||||3957|WARNING_TRANSCRIPT_NO_START_CODON,C|downstream_gene_variant|MODIFIER|ppiA|Rv0009|transcript|Rv0009|protein_coding||c.*1769T>C|||||1769|,C|downstream_gene_variant|MODIFIER|pknB|Rv0014c|transcript|Rv0014c|protein_coding||c.*805A>G|||||805|,C|downstream_gene_variant|MODIFIER|pknA|Rv0015c|transcript|Rv0015c|protein_coding||c.*2682A>G|||||2682|,C|downstream_gene_variant|MODIFIER|pbpA|Rv0016c|transcript|Rv0016c|protein_coding||c.*3974A>G|||||3974| GT:AD:DP:GQ:PL  1:0,77:77:99:2050,0
    """
    missense2 = """
    NC_000962.3     14785   .       T       G       2020.0  .       AC=1;AF=1.00;AN=1;DP=77;FS=0.000;MLEAC=1;MLEAF=1.00;MQ=60.00;QD=26.23;SOR=0.772;ANN=C|missense_variant|MODERATE|Rv0012|Rv0012|transcript|Rv0012|protein_coding|1/1|c.697T>C|p.Cys233Arg|697/789|697/789|233/262||,C|upstream_gene_variant|MODIFIER|Rv0008c|Rv0008c|transcript|Rv0008c|protein_coding||c.-2474A>G|||||2474|,C|upstream_gene_variant|MODIFIER|Rv0010c|Rv0010c|transcript|Rv0010c|protein_coding||c.-1227A>G|||||1227|,C|upstream_gene_variant|MODIFIER|Rv0011c|Rv0011c|transcript|Rv0011c|protein_coding||c.-790A>G|||||790|,C|upstream_gene_variant|MODIFIER|trpG|Rv0013|transcript|Rv0013|protein_coding||c.-129T>C|||||129|,C|downstream_gene_variant|MODIFIER|gyrA|Rv0006|transcript|Rv0006|protein_coding||c.*4967T>C|||||4967|,C|downstream_gene_variant|MODIFIER|Rv0007|Rv0007|transcript|Rv0007|protein_coding||c.*3957T>C|||||3957|WARNING_TRANSCRIPT_NO_START_CODON,C|downstream_gene_variant|MODIFIER|ppiA|Rv0009|transcript|Rv0009|protein_coding||c.*1769T>C|||||1769|,C|downstream_gene_variant|MODIFIER|pknB|Rv0014c|transcript|Rv0014c|protein_coding||c.*805A>G|||||805|,C|downstream_gene_variant|MODIFIER|pknA|Rv0015c|transcript|Rv0015c|protein_coding||c.*2682A>G|||||2682|,C|downstream_gene_variant|MODIFIER|pbpA|Rv0016c|transcript|Rv0016c|protein_coding||c.*3974A>G|||||3974| GT:AD:DP:GQ:PL  1:0,77:77:99:2050,0
    """
    
    deletion = """
    NC_000962.3    4189134    .    TGCGCCTACA    T    1086.97    .    AC=1;AF=1.00;AN=1;DP=25;FS=0.000;MLEAC=1;MLEAF=1.00;MQ=60.00;QD=29.02;SOR=1.609;ANN=T|disruptive_inframe_deletion|MODERATE|Rv3737|Rv3737|transcript|Rv3737|protein_coding|1/1|c.1439_1447delGCCTACAGC|p.Arg480_Gln482del|1439/1590|1439/1590|480/529||INFO_REALIGN_3_PRIME,T|upstream_gene_variant|MODIFIER|Rv3733c|Rv3733c|transcript|Rv3733c|protein_coding||c.-4631_-4623delTGTAGGCGC|||||4623|,T|upstream_gene_variant|MODIFIER|tgs2|Rv3734c|transcript|Rv3734c|protein_coding||c.-3253_-3245delTGTAGGCGC|||||3245|,T|downstream_gene_variant|MODIFIER|Rv3735|Rv3735|transcript|Rv3735|protein_coding||c.*2558_*2566delGCGCCTACA|||||2558|,T|downstream_gene_variant|MODIFIER|Rv3736|Rv3736|transcript|Rv3736|protein_coding||c.*1440_*1448delGCGCCTACA|||||1440|,T|downstream_gene_variant|MODIFIER|PPE66|Rv3738c|transcript|Rv3738c|protein_coding||c.*142_*150delTGTAGGCGC|||||150|,T|downstream_gene_variant|MODIFIER|PPE67|Rv3739c|transcript|Rv3739c|protein_coding||c.*1141_*1149delTGTAGGCGC|||||1149|,T|downstream_gene_variant|MODIFIER|Rv3740c|Rv3740c|transcript|Rv3740c|protein_coding||c.*1690_*1698delTGTAGGCGC|||||1698|,T|downstream_gene_variant|MODIFIER|Rv3741c|Rv3741c|transcript|Rv3741c|protein_coding||c.*3036_*3044delTGTAGGCGC|||||3044|,T|downstream_gene_variant|MODIFIER|Rv3742c|Rv3742c|transcript|Rv3742c|protein_coding||c.*3707_*3715delTGTAGGCGC|||||3715|WARNING_TRANSCRIPT_NO_START_CODON,T|downstream_gene_variant|MODIFIER|ctpJ|Rv3743c|transcript|Rv3743c|protein_coding||c.*4248_*4256delTGTAGGCGC|||||4256|WARNING_TRANSCRIPT_NO_START_CODON    GT:AD:DP:GQ:PL    1:0,25:25:99:1126,0
    """
    
    not_annotated = """
    NC_000962.3     4198611 .       CG      C       2689.97 .       AC=1;AF=1.00;AN=1;DP=84;FS=0.000;MLEAC=1;MLEAF=1.00;MQ=60.13;QD=32.02;SOR=0.843 GT:AD:DP:GQ:PL  1:0,84:84:99:2729,0
    """
    
    VCF_HEADER = """
            #CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  1109_S1_L00
            """
    
    @classmethod
    def setUpClass(cls):
        connect_to_db(database="test",password='mito')
        db = DbIO()        
        db.create_db()  

    def setUp(self):
        
        self.db = DbIO() 
        self.ref_organism, self.sample = ("otest", "stest")
    
        if self.db.exists_sample(self.ref_organism, self.sample):
            self.db.delete_sample(self.ref_organism, self.sample)
        if self.db.exists_sample(self.ref_organism, self.sample + "2"):
            self.db.delete_sample(self.ref_organism, self.sample + "2")
        
        Allele.update(main_effect=None).execute()
        for t in reversed(DbIO.tables):
            t.delete().execute()
        

   
    def test_repeated(self):       
        data = StringIO.StringIO(TestVcfLoad.VCF_HEADER +TestVcfLoad.missense +  TestVcfLoad.deletion) 
        
        
        VariantCollection(ref_organism=self.ref_organism, sample=self.sample).save()        
        with self.assertRaises(VariantCollectionExistsError):
            self.db.load_variants(VcfSnpeffIO.parse(data), self.ref_organism, self.sample)

    
    def test_load(self):
        data = StringIO.StringIO(TestVcfLoad.VCF_HEADER +TestVcfLoad.missense +  TestVcfLoad.not_annotated)
        self.db.load_variants(VcfSnpeffIO.parse(data), self.ref_organism, self.sample)
        
        
        self.assertEqual(1, VariantCollection.select().count())
        self.assertEqual(2, Variant.select().count())
        self.assertEqual(2, Allele.select().count())
        self.assertEqual(11, Effect.select().count())
        vc = VariantCollection.select().get()
        assignments = list(vc.assignments)
        self.assertEqual(2, len(assignments))
        self.assertGreater( len(assignments[0].annotations),0)
        self.assertEqual( 0,len(assignments[1].allele.effects))
    
    def test_2_load(self):
        data = StringIO.StringIO(TestVcfLoad.VCF_HEADER +TestVcfLoad.missense+  TestVcfLoad.not_annotated)
        self.db.load_variants(VcfSnpeffIO.parse(data), self.ref_organism, self.sample)
        data = StringIO.StringIO(TestVcfLoad.VCF_HEADER +TestVcfLoad.missense2)
        self.db.load_variants(VcfSnpeffIO.parse(data), self.ref_organism, self.sample+"2")
        self.assertEqual(2, VariantCollection.select().count())
        self.assertEqual(2, Variant.select().count())
    
    
    
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestVcfSnpeffIO.testName']
    unittest.main()