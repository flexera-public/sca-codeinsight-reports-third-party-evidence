# sca-codeinsight-reports-third-party-evidence

The sca-codeinsight-reports-third-party-evidence repository is a example report for Revenera's Code Insight product. This report allows a user to report on the current evidence found within the project such as
 
- Copyright
- License
- Emails and URLs
- Search Terms
- Exact File Matchs
- Source Matches


This repository utilizes the following via CDN for the creation of the report artifacts.
- [Bootstrap](https://getbootstrap.com/)
- [DataTables](https://datatables.net/)
- [chart.js](https://www.chartjs.org/)



## Prerequisites


 **Code Insight Release Requirements**
  
|Repository Tag | Minimum Code Insight Release  |
|--|--|
|1.0.x |2021R2  |



**Submodule Repositories**

This repository contains two submodules pointing to other git repos for code that can be in common to multiple projects. After the initial clone of sca-codeinsight-reports-project-inventory you will need to enter the cloned directory, link and pull down the necessary code via

    git submodule init
    git submodule update

**Python Requirements**

This repository requires the python requests module to interact with the Code Insight REST APIs.  To install this as well as the the modules it depends on the [requirements.txt](requirements.txt) file has been supplied and can be used as follows.

    pip install -r requirements.txt

## Required Configuration

There are two locations that require updates to provide the report scripts details about the host system.

The [create_report.sh](create_report.sh) or [create_report.bat](create_report.bat) file contains a **baseURL** value that should be updated to allow for project and inventory links to point to the correct system. 

For registration purposes update the **baseURL** and **adminAuthToken** values within [registration.py](registration.py) to reflect the correct values to allow the report itself to be registered on the Code Insight server.

### Registering the Report


Prior to being able to call the script directly from within Code Insight it must be registered. The registration.py file can be used to directly register the report once the contents of this repository have been copied into the custom_report_script folder at the base Code Insight installation directory.

To register this report:

    python registration.py -reg


To unregister this report:

    python registration.py -unreg


## Usage

This report is executed directly from within Revenera's Code Insight product. From the project reports tab each Code Insight project it is possible to *generate* the **Third Party Evidence Report** via the Custom Report Framework.

The Code Insight Custom Report Framework will provide the following to the custom report when initiated:

- Project ID
- Report ID
- Authorization Token
 

For this example report these three items are passed on to a batch or sh file which will in turn execute a python script. This script will then:

- Collect data for the report via REST API using the Project ID and Authorization Token
- Take this collected data and generated an html document with details about the project inventory
	- The *"viewable"* file   
 - Create a zip file of this html document
	  - The *"downloadable"* file
  - Create a zip file with the viewable file and the downloadable file
- Upload this combined zip file to Code Insight via REST API
- Delete the report artifacts that were created as the script ran


## License

[MIT](LICENSE.TXT)


