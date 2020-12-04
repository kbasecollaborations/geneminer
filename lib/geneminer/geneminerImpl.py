# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid

from installed_clients.KBaseReportClient import KBaseReport
from geneminer.Utils.geneminerutils import geneminerutils
from geneminer.Utils.htmlreportutils import htmlreportutils
from installed_clients.WorkspaceClient import Workspace

#END_HEADER


class geneminer:
    '''
    Module Name:
    geneminer

    Module Description:
    A KBase module: geneminer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.ws_url = config['workspace-url']
        self.gu = geneminerutils()
        self.hr = htmlreportutils()
        #self.config = config
        #self.hr = htmlreportutils()

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_geneminer(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_geneminer
        print (params)
        filename="/kb/module/work/genelist.txt"
       # self.ws = Workspace(self.ws_url, token=ctx['token'])
        #self.gu.download_genelist(params['genelistref'], filename)
        #pheno = ["disease"]
        #species = "potatoknet"
        #genes = ["PGSC0003DMG400006345", "PGSC0003DMG400012792", "PGSC0003DMG400033029", "PGSC0003DMG400016390",
        #         "PGSC0003DMG400039594", "PGSC0003DMG400028153"]
        pheno = params['pheno']
        # Need to create a dictionary based on supported species
        species = params['species']
        #genomenetmine_dyn_url = 'http://ec2-18-236-212-118.us-west-2.compute.amazonaws.com:5000/networkquery/api'
        genomenetmine_dyn_url='https://appdev.kbase.us/dynserv/a5fee7b790d9538ec21276d0e0ca88dcf0cb3687.genomenetmine/networkquery/api'
        #genomenetmine_dyn_url = 'https://ci.kbase.us/dynserv/10a877126719dc376e6df55a83a97c58e094d3a0.genomenetmine/networkquery/api'
        #gsp = genescoreparser()
        #genomenetmine_dyn_url='https://ci.kbase.us/dynserv/0a0fc46b9d2e4fea40429d4551c31ad7462a3180.genomenetmine/networkquery/api'
        tabledata1 = self.gu.generate_query(genomenetmine_dyn_url, params['genelistref'], species, pheno)
        #print (data)
        tabledata2 = self.gu.get_evidence(genomenetmine_dyn_url, params['genelistref'], species, pheno)
        #print(data)
        directory = str(uuid.uuid4())
        path = os.path.join("/kb/module/work/tmp", directory)
        os.mkdir(path)
        html_path=os.path.join(path,"index.html")

        with open (html_path, "w") as f:
            f.write("<html><body>")
            f.write(tabledata1)
            f.write("</br")
            f.write("</br")
            f.write("</br")
            f.write(tabledata2)
            f.write("</body></html>")

        output = self.hr.create_html_report(path, params['workspace_name'])
        #report = KBaseReport(self.callback_url)
        #report_info = report.create({'report': {'objects_created':[],
        #                                        'text_message': params['genelistref']},
        #                                        'workspace_name': params['workspace_name']})
        #output = {
        #    'report_name': report_info['name'],
        #    'report_ref': report_info['ref'],
        #}

        #END run_geneminer

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_geneminer return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
