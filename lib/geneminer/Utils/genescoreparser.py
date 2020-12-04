import requests
import numpy as np
import pandas as pd
import json
import pprint
from itertools import islice

class genescoreparser:
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


        decoded=r.json()[u'geneTable'].split("\t")
        #remove space or newline at the end
        return (decoded)[:-1]

    def knetScorer(self,genomenetmine_dyn_url, genes, species, pheno):
        """ Returns the KnetMiner JSON table containing the KnetScore with successful requests (containing the gene ID and keyword combination given)
            REQUIRES: genes, species ID, and keyword list
            RETURNS: decoded KnetMiner JSON table """

        genelist=(",").join(genes)
        keyw="%20OR%20".join("{}".format(i) for i in pheno)
        data={
            "knet":species + "/genome?",
            "keywords":keyw,
            "genelist":genelist
        }
        r = requests.post(genomenetmine_dyn_url, data=data)
        decoded = self.decode(r)
        return decoded

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

    #        print (decoded)
    #        exit

            #print("Filtering results, please wait...")
            genetable = np.array(decoded).reshape(len(decoded)//9, 9) #tabulate genetable into 9 columns.
            genetable = pd.DataFrame(genetable[1:, :], columns = genetable[0, :])
            genesUpperList = list(map(str.upper, genes)) # Make the genes uppercase
            genetable = genetable.loc[genetable[u'ACCESSION'].isin(genesUpperList)] # Update the table so we only have matching genes

            knetgenes, knetscores = list(genetable[u'ACCESSION']), list(genetable[u'SCORE'])
            knetchro, knetstart = list(genetable[u'CHRO']), list(genetable[u'START'])
            genes_ordered = set(genesUpperList).intersection(knetgenes) # Only keep matching genes
            genes_ordered = list(genes_ordered)

            #updatedNetworkView = splitNetworkViewUrls(genes_ordered, network_view)

            filtered_summary = pd.DataFrame(columns=[u'ACCESSION'])
            filtered_summary[u'ACCESSION'] = genes_ordered
            filtered_summary = filtered_summary.merge(genetable, how = 'inner', on= [u'ACCESSION'])
            filtered_summary[u'ACCESSION'] = filtered_summary[u'ACCESSION'].astype(str)

            knetdict=dict(zip(knetgenes, knetscores)) # Map the genes to SNPs via a dictionary.
            #print("\n\nDisplaying knetscores for 5 genes.\n")
            #pprint.pprint(list(islice(knetdict.items(), len(knetdict.items()))))


            filtered_summary = filtered_summary.drop(filtered_summary.columns[[1, 7, 8]], axis=1)
            filtered_summary.columns = ['Accession ID', 'Gene Name', 'Chromosome', 'Start position', 'TaxID', 'KnetScore']

            #print("\n\nOrdering genes based on KnetScore, one moment...\n")
            filtered_summary[u'KnetScore'] = filtered_summary[u'KnetScore'].astype(float)
            filtered_summary.sort_values('KnetScore', ascending=False, inplace=True)
            #print("Writing results out now...\n")
            #if args.output is None:
            #    filtered_summary.to_csv("results.txt", sep="\t", index=False)
            #    print("We're Finished! Your results are in: {}/{}_output/results.txt".format(os.getcwd(), str(args.genes)[:-4]))
            #else:
            #    filtered_summary.to_csv(args.output, sep="\t", index=False, header=False)
            #    print("We're Finished! Your results are in: {}".format(args.output))
            #    headerfile= open(args.out_header, "w")
            #    headerfile.write("Accession ID,Gene Name,Chromosome,Start Position,Tax ID,KnetScore,KnetMiner genepage")
            #    headerfile.close()
            #    print("output header file in: {}".format(args.out_header))
            #print("\n\nIn total, {}/{} genes were returned by KnetMiner.\n".format(len(genes_ordered), startingLen))
            #return (filtered_summary)
            htmlstr = "<table>"
            csv_str = filtered_summary.to_csv(sep="\t")
            csv_rows = csv_str.split("\n")
            for row in csv_rows:
                htmlstr += "<tr>"
                r = row.split("\t")
                for cell in r:
                    htmlstr += "<td>" + cell + "</td>"
                htmlstr += "</tr>"
            htmlstr += "</table>"
            return(htmlstr)


if __name__=="__main__":
    pheno=["disease"]
    species = "potatoknet"
    genes = ["PGSC0003DMG400006345", "PGSC0003DMG400012792", "PGSC0003DMG400033029", "PGSC0003DMG400016390", "PGSC0003DMG400039594", "PGSC0003DMG400028153"]
    genomenetmine_dyn_url='http://ec2-18-236-212-118.us-west-2.compute.amazonaws.com:5000/networkquery/api'
    gsp = genescoreparser()
    x = gsp.summary(genomenetmine_dyn_url, genes, species, pheno)
    print (x)
