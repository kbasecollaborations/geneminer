/*
A KBase module: geneminer
*/

module geneminer {

    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure {
        string geneset_ref;
        string terms;
    } geneminer_input;



    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_geneminer(geneminer_input params) returns (ReportResults output) authentication required;

};
