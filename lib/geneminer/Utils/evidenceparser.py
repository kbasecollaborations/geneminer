import requests
from collections import defaultdict
import json
import networkx as nx
import re



import requests

class evidenceparser:
    def __init__(self):
        pass
        #self.callback_url = os.environ['SDK_CALLBACK_URL']
        #self.dfu = DataFileUtil(self.callback_url)

    def decode(self,r):
        """ If the request fails, then exit. Else, return the KnetMiner genetable.
            REQUIRES: The request.
            RETURNS: JSON object containing the gene-table information.
        """
        if not r.ok:
                r.raise_for_status()
                sys.exit()
        #else:
            #print("request successful")

        decoded = r.json()[u'graph']

        # remove space or newline at the end
        decoded = decoded.replace("var graphJSON=", "[")
        decoded = decoded.replace(';', '')
        decoded = decoded.replace("var allGraphData=", ",")
        decoded = decoded + "]"

        return (decoded)

        #decoded=r.json()[u'geneTable'].split("\t")
        #remove space or newline at the end
        #return (decoded)[:-1]

    def knetScorer(self,genomenetmine_dyn_url, genes, species, pheno):
        """ Returns the KnetMiner JSON table containing the KnetScore with successful requests (containing the gene ID and keyword combination given)
            REQUIRES: genes, species ID, and keyword list
            RETURNS: decoded KnetMiner JSON table """

        genelist=(",").join(genes)
        keyw="%20OR%20".join("{}".format(i) for i in pheno)
        data={
            "knet":species + "/network?",
            "keywords":keyw,
            "genelist":genelist
        }
        r = requests.post(genomenetmine_dyn_url, data=data)
        decoded = self.decode(r)
        return decoded

    def parse_graph(self, G, d, query_id, publist, gene ):
        # with open('xm.json') as f:
        #    data = json.load(f)

        res = gene + "\n"
        nr_dict = dict()
        final_results=list()

        for p in publist:
            result = ""
            s = nx.shortest_path(G, query_id, p)
            start = None
            end = None
            i = 0
            val = None
            v=0
            for n in s:
                if v==3:
                    break
                if (v==2):
                    if result not in nr_dict:
                        nr_dict[result]=1
                        final_results.append(result)
                        #print (result)
                    break
                i = i + 1
                if i != 1:
                    end = n
                node = d[n]['value']

                type = d[n]['type']
                # if pid not in d[n]:
                #    print d[n]
                if end is not None:
                    key1 = str(start) + "-" + str(end)
                    key2 = str(end) + "-" + str(start)

                    # print (key1)
                    # print (key2)


                    if key1 in d:
                        val = d[key1]['label']
                        v=1
                    else:
                        val = d[key2]['label']
                        if val=="orthologue":
                            v=1
                        elif val=="encodes":
                            v=1
                        elif val=="located_in":
                            result=""
                            v=3
                        else:
                            v=2

                if v==1:
                    r = "--" + val + "--" + node + "[" + type + "]"
                    if type=="Publication":
                        r=r.replace("PMID: ","")
                        r=r.replace("[Publication]", "")
                        r=r.replace("--published_in--","")
                        r="<a href='https://pubmed.ncbi.nlm.nih.gov/" +str(r) + "'>pubmed:" + str(r) + "</a>"
                    result += r

                if start is None:
                    start = n
                else:
                    start = end
            #result = result.replace("--encodes--", "--encoded by-")
            if result not in nr_dict:
                final_results.append(result)
                nr_dict[result]=1

        for result in final_results:
             result = re.sub('.*orthologue--', '      ortholog--', result)
             result=result.replace('has_physical_relation_with', 'interacts_with')
             result=result.rstrip()
             if result.endswith('Gene]'):
                 continue
             if result is not None:
                 res += result + "\n"
        #print (res)
        return (res)


    def summary(self, genomenetmine_dyn_url, genes, species, pheno):
        """ Searches KnetMiner for the provided keywords & genes, truncating down to only the most relevant information.
            REQUIRES: User-provided arguments.
            RETURNS: Outputs a dataframe containing the matching genes, chromosome score(s), position, & their KnetMiner API URLs.

       """
        x=1
        if x ==1:
            #pheno=[]
            #for line in fk:
            #    pheno.append(line.rstrip())
            #summary=pd.read_csv(args.genes, sep="\t", header=None)
            #summary.rename (columns={
            #                         0:"GENE"
            #                         }, inplace=True )
            #genes = list(summary["GENE"])

        #keyw="%20OR%20".join("{}".format(i) for i in pheno)


            startingLen = len(genes)
            #creating knetminer genepage urls.
            network_view=[]
            for i, keyword in enumerate(pheno):
                if ' ' in keyword:
                    pheno[i] = "\"" + keyword + "\"" # Fixing git issue #424

            keyw="%20OR%20".join("{}".format(i) for i in pheno)


            #obtaining knetscores for genes
           # print("\nYour provided traits are as follows:\n\n")
           # print(*pheno, sep=", ") # Collect all positional arguments into tuple and seperate by commasa
            decoded = self.knetScorer(genomenetmine_dyn_url, genes, species, pheno)
            #print (decoded)

            data=json.loads(decoded)

            G = nx.Graph()
            # G.add_node("1")
            # G.add_node("2")
            # G.add_edge("1","2")

            d = defaultdict(lambda: defaultdict())
            publist = list()
            idlist = list()

            nodes = data[0]['nodes']
            id_dictionary = dict()
            for j in nodes:
                id = j['data']['id']
                value = j['data']['value']
                type = j['data']['conceptType']
                pid = j['data']['pid']
                G.add_node(j['data']['id'])
                d[id]['value'] = value
                d[id]['type'] = type
                d[id]['pid'] = pid
                id_dictionary[value] = id
                idlist.append(id)
                if type == 'Publication':
                    publist.append(id)

            edges = data[0]['edges']

            for k in edges:
                G.add_edge(k['data']['source'], k['data']['target'])
                idx = str(k['data']['source']) + "-" + str(k['data']['target'])
                d[idx]['label'] = k['data']['label']

            result = "<table><tr><td>Evidence for genes</td></tr>"
            for gene in genes:
                query_id = id_dictionary[gene]
                result +="<tr><td><pre>"
                result += self.parse_graph(G, d, query_id, publist, gene)
                result += "</pre></td></tr>"
            result += "</table>"
            #print (result)
            return (result)



            # print POTRI.008G077700
            #exit()
            #query=(",").join(genes)
            #print (query)




if __name__=="__main__":
    pheno=["disease"]
    species = "potatoknet"
    #genes = ["PGSC0003DMG400006345"]
    genes = ["PGSC0003DMG400006345", "PGSC0003DMG400012792", "PGSC0003DMG400033029", "PGSC0003DMG400016390", "PGSC0003DMG400039594", "PGSC0003DMG400028153"]
    genomenetmine_dyn_url='http://ec2-18-236-212-118.us-west-2.compute.amazonaws.com:5000/networkquery/api'
    gsp = evidenceparser()
    x = gsp.summary(genomenetmine_dyn_url, genes, species, pheno)
    print (x)
