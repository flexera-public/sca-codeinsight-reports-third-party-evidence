'''
Copyright 2021 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Mar 24 2021
File : report_data.py
'''

import logging

import CodeInsight_RESTAPIs.project.get_project_information
import CodeInsight_RESTAPIs.project.get_project_evidence

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------#
def gather_data_for_report(baseURL, projectID, authToken, reportName, reportOptions):
 
    projectInformation = CodeInsight_RESTAPIs.project.get_project_information.get_project_information_summary(baseURL, projectID, authToken)
    projectName = projectInformation["name"]
    totalFiles = projectInformation["totalFiles"]

    fileEvidence = {} # Dict to hold evidience information for each file (claimable or not)
    filesWithCopyrights = 0
    filesWithLicenses =  0
    filesWithEmailURL = 0
    filesWithSearchTerms = 0
    filesWithExactMatches = 0
    filesWithSourceMatches = 0

    # Get the evidence gathered
    projectEvidence = CodeInsight_RESTAPIs.project.get_project_evidence.get_project_evidence(baseURL, projectID, authToken)
    for evidence in projectEvidence["data"]:

        fileName = evidence["fileName"]
        filePath = evidence["filePath"]
        remote = evidence["remote"]
        scannedFileId = evidence["scannedFileId"]
        copyrightEvidienceFound = evidence["copyRightMatches"]
        emailUrlEvidenceFound = evidence["emailUrlMatches"]
        licenseEvidenceFound =  evidence["licenseMatches"]
        searchTermMatchEvidenceFound =  evidence["searchTextMatches"]
        exactFileMatchEvidenceFound =  evidence["exactFileMatches"]
        sourceMatchEvidenceFound =  evidence["sourceMatches"]

        fileEvidence[filePath] = {} # Dict to hold the data for each file
        fileEvidence[filePath]["filelink"] =  baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + str(projectID) + "&tab=workbench&view=file&fileid=" + str(scannedFileId) + "&remote=" + str(remote)

        fileEvidence[filePath]["evidence"] = {}

        if len(copyrightEvidienceFound):
            fileEvidence[filePath]["evidence"]["copyright"] = True
            filesWithCopyrights +=1
        if len(licenseEvidenceFound):
            fileEvidence[filePath]["evidence"]["license"] = True
            filesWithLicenses +=1
        if len(emailUrlEvidenceFound):
            fileEvidence[filePath]["evidence"]["emailURL"] = True
            filesWithEmailURL +=1
        if searchTermMatchEvidenceFound:
            fileEvidence[filePath]["evidence"]["searchTerm"] = True
            filesWithSearchTerms +=1
        if exactFileMatchEvidenceFound:
            fileEvidence[filePath]["evidence"]["exactMatch"] = True
            filesWithExactMatches +=1
        if sourceMatchEvidenceFound:
            fileEvidence[filePath]["evidence"]["sourceMatch"] = True
            filesWithSourceMatches +=1

        # Is there any evidence at all?
        if not len(fileEvidence[filePath]["evidence"]):
            # Remove the file since it has no evidence
            del fileEvidence[filePath]

    # Dictionary to contain the roll up summary for files/evidence
    evidenceSummary = {}
    evidenceSummary["totalScannedFiles"] = totalFiles
    evidenceSummary["copyright"] = filesWithCopyrights
    evidenceSummary["license"] = filesWithLicenses
    evidenceSummary["emailURL"] = filesWithEmailURL
    evidenceSummary["searchTerm"] = filesWithSearchTerms
    evidenceSummary["exactMatch"] = filesWithExactMatches
    evidenceSummary["sourceMatch"] = filesWithSourceMatches

    # Build up the data to return for the report generation
    reportData = {}
    reportData["reportName"] = reportName
    reportData["projectName"] = projectName
    reportData["fileEvidence"] = fileEvidence
    reportData["evidenceSummary"] = evidenceSummary
    
    
    return reportData