import os
from installed_clients.DataFileUtilClient import DataFileUtil

class genelistutil:
  def __init__(self):
      self.callback_url = os.environ['SDK_CALLBACK_URL']
      self.dfu = DataFileUtil(self.callback_url)
      pass

  def download_genelist(self, genelistref, genesetfile):
      get_objects_params = {'object_refs' : [genelistref]} 
      geneset = self.dfu.get_objects(get_objects_params)['data'][0]['data']
      with open(genesetfile, 'w') as filehandle:
           for item in geneset['element_ordering']:
               filehandle.write('%s\n' % item)

  def listToString(self, s):  
    str1 = ""     
    for ele in s:  
        str1 += ele      
    return str1 

  def get_genomeid_from_featuresetid (self, genelistref):
      genome = {}
      get_objects_params = {'object_refs' : [genelistref]} 
      geneset = self.dfu.get_objects(get_objects_params)['data'][0]['data']

      for k, v in geneset['elements'].items():
        genome[self.listToString(v)] = 1
      if (len(genome) != 1):
         exit("source of genome is not unique\n")
      else:
         return (list(genome.keys())[0])







     
     
      
  
