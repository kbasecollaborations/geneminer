import os
from installed_clients.DataFileUtilClient import DataFileUtil
from geneminer.Utils.genescoreparser import genescoreparser
from geneminer.Utils.evidenceparser import evidenceparser





class geneminerutils:
    def __init__(self):
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        #self.hr = htmlreportutils()
        #self.config = config
        #self.params = params

    def download_genelist(self, genelistref):
        get_objects_params = {'object_refs': [genelistref]}
        geneset = self.dfu.get_objects(get_objects_params)['data'][0]['data']
        #geneset_query = ",".join(geneset)
        return (geneset['element_ordering'])
      #  #with open(genesetfile, 'w') as filehandle:
      #      #for item in geneset['element_ordering']:
      #       #   filehandle.write('%s\n' % item)
      #  #return (genesetfile)

    def generate_query(self, genomenetmine_dyn_url, genelistref, species, pheno):
        #pheno = ["disease"]
        #species = "potatoknet"
        #genes = ["PGSC0003DMG400006345", "PGSC0003DMG400012792", "PGSC0003DMG400033029", "PGSC0003DMG400016390",
        #         "PGSC0003DMG400039594", "PGSC0003DMG400028153"]
        #genomenetmine_dyn_url = 'http://ec2-18-236-212-118.us-west-2.compute.amazonaws.com:5000/networkquery/api'
        genes = self.download_genelist(genelistref)
        gsp = genescoreparser()
        x = gsp.summary(genomenetmine_dyn_url, genes, species, pheno)
        return (x)

    def get_evidence(self,genomenetmine_dyn_url, genelistref, species, pheno ):
        genes = self.download_genelist(genelistref)
        ep = evidenceparser()
        x = ep.summary(genomenetmine_dyn_url, genes, species, pheno)
        return (x)





