'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Nov 19 2021
File : report_artifacts_html.py
'''

import logging
import os
import base64

import _version

logger = logging.getLogger(__name__)


#------------------------------------------------------------------#
def generate_html_report(reportData):
    logger.info("    Entering generate_html_report")

    reportName = reportData["reportName"]
    projectName = reportData["projectName"]
    reportFileNameBase = reportData["reportFileNameBase"]
    reportTimeStamp =  reportData["reportTimeStamp"] 
    fileEvidence = reportData["fileEvidence"]
    evidenceSummary = reportData["evidenceSummary"]
   
    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    cssFile =  os.path.join(scriptDirectory, "report_branding/css/revenera_common.css")
    logoImageFile =  os.path.join(scriptDirectory, "report_branding/images/logo_reversed.svg")
    iconFile =  os.path.join(scriptDirectory, "report_branding/images/favicon-revenera.ico")

    logger.debug("cssFile: %s" %cssFile)
    logger.debug("imageFile: %s" %logoImageFile)
    logger.debug("iconFile: %s" %iconFile)

    #########################################################
    #  Encode the image files
    encodedLogoImage = encodeImage(logoImageFile)
    encodedfaviconImage = encodeImage(iconFile)

    htmlFile = reportFileNameBase + ".html"
    logger.debug("htmlFile: %s" %htmlFile)
    
    #---------------------------------------------------------------------------------------------------
    # Create a simple HTML file to display
    #---------------------------------------------------------------------------------------------------
    try:
        html_ptr = open(htmlFile,"w")
    except:
        logger.error("Failed to open htmlfile %s:" %htmlFile)
        raise

    html_ptr.write("<html>\n") 
    html_ptr.write("    <head>\n")

    html_ptr.write("        <!-- Required meta tags --> \n")
    html_ptr.write("        <meta charset='utf-8'>  \n")
    html_ptr.write("        <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'> \n")

    html_ptr.write(''' 
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css" integrity="sha384-VCmXjywReHh4PwowAiWNagnWcLhlEJLA5buUprzK8rxFgeH0kww/aWY76TfkUoSX" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.css">
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/dataTables.bootstrap4.min.css">
    ''')


    html_ptr.write("        <style>\n")

    # Add the contents of the css file to the head block
    try:
        f_ptr = open(cssFile)
        logger.debug("Adding css file details")
        for line in f_ptr:
            html_ptr.write("            %s" %line)
        f_ptr.close()
    except:
        logger.error("Unable to open %s" %cssFile)
        print("Unable to open %s" %cssFile)


    html_ptr.write("        </style>\n")  

    html_ptr.write("    	<link rel='icon' type='image/png' href='data:image/png;base64, {}'>\n".format(encodedfaviconImage.decode('utf-8')))
    html_ptr.write("        <title>%s</title>\n" %(reportName))
    html_ptr.write("    </head>\n") 

    html_ptr.write("<body>\n")
    html_ptr.write("<div class=\"container-fluid\">\n")

    #---------------------------------------------------------------------------------------------------
    # Report Header
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN HEADER -->\n")
    html_ptr.write("<div class='header'>\n")
    html_ptr.write("  <div class='logo'>\n")
    html_ptr.write("    <img src='data:image/svg+xml;base64,{}' style='width: 400px;'>\n".format(encodedLogoImage.decode('utf-8')))
    html_ptr.write("  </div>\n")
    html_ptr.write("<div class='report-title'>%s</div>\n" %(reportName))
    html_ptr.write("</div>\n")
    html_ptr.write("<!-- END HEADER -->\n")

    #---------------------------------------------------------------------------------------------------
    # Body of Report
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN BODY -->\n") 
 
    html_ptr.write("<table id='evidenceSummary' class='table' style='width:90%'>\n")
    html_ptr.write("    <thead>\n")
    html_ptr.write("        <tr>\n") 
    html_ptr.write("            <th class='text-center'><h4>%s - Third Party Evidence Summary</h4></th>\n"%projectName) 
    html_ptr.write("        </tr>\n") 
    html_ptr.write("    </thead>\n")
    html_ptr.write("    <tbody>\n")
    html_ptr.write("        <tr><td>\n") 
    html_ptr.write("            <div style=\"height: 300px\" class='container'>\n")
    html_ptr.write("                <canvas id='projectEvidence'></canvas>\n")
    html_ptr.write("            </div>\n")
    html_ptr.write("        </td></tr>\n") 
    html_ptr.write("    </body>\n")
    html_ptr.write("</table>\n")

    html_ptr.write("<hr class='small'>")

    html_ptr.write("<table id='fileEvidence' class='table table-hover table-sm row-border' style='width:90%'>\n")

    html_ptr.write("    <thead>\n")
    html_ptr.write("        <tr>\n")
    html_ptr.write("            <th colspan='10' class='text-center'><h4>%s - Third Party Evidence File Details</h4></th>\n" %projectName) 
    html_ptr.write("        </tr>\n") 
    html_ptr.write("        <tr>\n")
    html_ptr.write("            <th style='vertical-align: middle; width: 50%' class='text-left text-nowrap'>File Path</th>\n") 
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>Copyright</th>\n") 
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>License</th>\n")
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>Email/URL</th>\n")
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>Search Terms</th>\n")
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>Exact File Match</th>\n")
    html_ptr.write("            <th style='vertical-align: middle; width: 5%' class='text-center'>Source Code Match</th>\n")
    html_ptr.write("        </tr>\n")
    html_ptr.write("    </thead>\n")  
    html_ptr.write("    <tbody>\n")  

    for filePath in sorted(fileEvidence):

        filelink = fileEvidence[filePath]["filelink"]

        html_ptr.write("        <tr> \n")
        html_ptr.write("            <td class='text-left'><a href='%s' target='_blank'>%s</a></td>\n" %(filelink, filePath))

        for evidence in ["copyright", "license", "emailURL", "searchTerm", "exactMatch", "sourceMatch"]:
            # See if the evidence exists.  If the key is not there that type was not found
            if evidence in fileEvidence[filePath]["evidence"]:
                html_ptr.write("            <td class='text-center text-nowrap' style='vertical-align: middle;'><span class='dot dot-%s'></span></td>\n" %evidence)
            else:
                html_ptr.write("            <td>&nbsp</td>\n")

        html_ptr.write("        </tr>\n") 

    html_ptr.write("    </tbody>\n")


    html_ptr.write("</table>\n")  

    html_ptr.write("<!-- END BODY -->\n")  
    #---------------------------------------------------------------------------------------------------
    # Report Footer
    #---------------------------------------------------------------------------------------------------
    html_ptr.write("<!-- BEGIN FOOTER -->\n")
    html_ptr.write("<div class='report-footer'>\n")
    html_ptr.write("  <div style='float:right'>Generated on %s</div>\n" %reportTimeStamp)
    html_ptr.write("<br>\n")
    html_ptr.write("  <div style='float:right'>Report Version: %s</div>\n" %_version.__version__)
    html_ptr.write("</div>\n")
    html_ptr.write("<!-- END FOOTER -->\n")  

    html_ptr.write("</div>\n")    

    #---------------------------------------------------------------------------------------------------
    # Add javascript 
    #---------------------------------------------------------------------------------------------------

    html_ptr.write('''

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>  
    <script src="https://cdn.datatables.net/1.10.21/js/dataTables.bootstrap4.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.8.0"></script> 
    ''')

    html_ptr.write("<script>\n")

     # Add the common chartjs config
    add_default_chart_options(html_ptr)
    # Add the js for the evidence summary stacked bar charts
    generate_evidence_summary_chart(html_ptr, evidenceSummary)

    # Add the js for inventory datatable
    html_ptr.write('''
        
            var table = $('#fileEvidence').DataTable();

            $(document).ready(function() {
                table;
            } );
    ''')

    html_ptr.write("</script>\n")

    html_ptr.write("</body>\n") 
    html_ptr.write("</html>\n") 
    html_ptr.close() 

    logger.info("    Exiting generate_html_report")
    return htmlFile

####################################################################
def encodeImage(imageFile):

    #############################################
    # Create base64 variable for branding image
    try:
        with open(imageFile,"rb") as image:
            logger.debug("Encoding image: %s" %imageFile)
            encodedImage = base64.b64encode(image.read())
            return encodedImage
    except:
        logger.error("Unable to open %s" %imageFile)
        raise

#----------------------------------------------------#
def add_default_chart_options(html_ptr):
    # Add commont defaults for display charts
    html_ptr.write('''  
        var defaultBarChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                bottom: 25  //set that fits the best
            }
        },
        tooltips: {
            enabled: false,
            yAlign: 'center'
        },
        title: {
            display: false,
            fontColor: "#323E48"
        },

        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero:true,
                    fontSize:12,
                    fontColor: "#323E48",
                    precision:0

                },
                scaleLabel:{
                    display:false
                },
                gridLines: {
                }, 
                stacked: false
            }],
            yAxes: [{
                gridLines: {
                    display:false,
                    color: "#fff",
                    zeroLineColor: "#fff",
                    zeroLineWidth: 0,
                    fontColor: "#323E48"
                },
                ticks: {
                    fontSize:15,
                    fontColor: "#323E48"
                },

                stacked: false
            }]
        },
        legend:{
            display:false
        },
        
    };  ''')

#----------------------------------------------------#
def generate_evidence_summary_chart(html_ptr, evidenceSummary):
    logger.info("Entering generate_evidence_summary_chart")
    html_ptr.write('''  
        var projectEvidence = document.getElementById("projectEvidence");
        var projectEvidenceChart = new Chart(projectEvidence, {
            type: 'horizontalBar',
            data: {
                labels: ['Total Files Scanned (%s files)', 'Copyleft (%s files - %s%%)', 'License (%s files - %s%%)','Email/URL (%s files - %s%%)','Search Terms (%s files - %s%%)','Exact Match (%s files - %s%%)','Source Match (%s files - %s%%)'],
                datasets: [{
                    data: [%s, %s, %s, %s, %s, %s, %s],
                    backgroundColor: ["#7F7F7F", "#0099FF", "#33CC33", "#FF02F9", "#02FFFF", "#FF0000", "#FFFF00"]
                }]
            },

            options: defaultBarChartOptions,
        });


        ''' %(evidenceSummary["totalScannedFiles"],
            evidenceSummary["copyright"], evidenceSummary["filesWithCopyrightPercentage"],
            evidenceSummary["license"], evidenceSummary["filesWithLicensePercentage"],
            evidenceSummary["emailURL"], evidenceSummary["filesWithemailURLPercentage"],
            evidenceSummary["searchTerm"], evidenceSummary["filesWithSearchTermPercentage"],
            evidenceSummary["exactMatch"], evidenceSummary["filesWithExactMatchPercentage"],
            evidenceSummary["sourceMatch"], evidenceSummary["filesWithSourceMatchPercentage"],
            evidenceSummary["totalScannedFiles"],
            evidenceSummary["copyright"], 
            evidenceSummary["license"], 
            evidenceSummary["emailURL"],
            evidenceSummary["searchTerm"],
            evidenceSummary["exactMatch"],
            evidenceSummary["sourceMatch"]         
            
            )  )
