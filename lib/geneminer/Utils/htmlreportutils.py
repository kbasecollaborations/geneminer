import uuid
import os
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
import shutil 


class htmlreportutils:

    def __init__(self):
        self.organism_dict = {}
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        pass

    def create_html_report(self, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(self.callback_url)
        report_name = 'genenetminer' + str(uuid.uuid4())
        report = KBaseReport(self.callback_url)
  
        report_shock_id = dfu.file_to_shock({'file_path': output_dir,
                                            'pack': 'zip'})['shock_id']

        html_file = {
            'shock_id': report_shock_id,
            'name': 'index.html',
            'label': 'index.html',
            'description': 'Variation HTML report'
            }
        
        report_info = report.create_extended_report({
                        'direct_html_link_index': 0,
                        'html_links': [html_file],
                        'report_object_name': report_name,
                        'workspace_name': workspace_name
                    })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }


