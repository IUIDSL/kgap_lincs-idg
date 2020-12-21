# `kgap_lincs-idg`

Knowledge graph analytics platform (KGAP) for LINCS and IDG Common Fund dataset integration.
The initial biomedical application is Parkinson's disease drug target discovery, in alignment
with the IDSL __PRIDE__ initiative (Parkinson's Research through Integrative Data Experiments).

See also:

* [KGAP Project Homepage](http://cheminfov.informatics.indiana.edu/projects/kgap/)

## Publication  (in preparation)

"Knowledge graph analytic platform with LINCS and IDG for Parkinson's disease target illumination",
by Jeremy J Yang, Christopher R Gessner, Joel L Duerksen, Brian Foote, Daniel Biber,
Jessica L Binder, Robin McEntire, Kyle Stirling, Ying Ding and David J Wild.

<img align="center" height="200" src="doc/images/LINCS-IDG_Integration.png">

## Graph database

### The fast path
Note: These steps should work with little or no modifications on Macintosh, Unix, and Windows. Process tested on MacBookPro 2017 Catalina

To restore this graph database from a dump file download
this [dump file](http://cheminfov.informatics.indiana.edu/projects/kgap/data/dclneodb.dump),
install the Neo4j Desktop Client [Neo4j](https://neo4j.com/) and then 
follow these [instructions](https://github.com/IUIDSL/kgap_lincs-idg/blob/master/opt2_load_neo4j_dump/Neo4jDesktop.md)
to restore the database dump.

### The long path (and more technical), to recreate the graph database from scratch
#### Step 1: create node and relationship files 
Note: Process developed on Ubuntu 20.04, and tested on MacbookPro 2017 Catalina 

- clone this repository in your home directory, the following process assumes ~/kgap_lincs-idg/ exists and is populated
- Download, restore and bring online [drugcentral_lincs](http://cheminfov.informatics.indiana.edu/projects/kgap/data/drugcentral_lincs.pgdump)
- Download the file [tcrd_targets.tsv](https://github.com/IUIDSL/kgap_lincs-idg/blob/master/opt1_step1_create_neo4j_input_files/tcrd_targets.tsv) either directly or if you cloned this repository, you will have a copy already.
- Download and install [Knime](https://www.knime.com/) Note: The workflow was created with version 4.3
- import the knime workflow [kgap_lincs-idg/opt1_step1_create_neo4j_files](opt1_step1_create_neo4j_input_files/drugcentral_lincs_etl2neo4jfiles.knwf), you will see and safely ignore this dialog message <BR>![knime workflow load message](doc/images/knime-workflow-load-message.png)
- This workflow ETLs data from three datasets, a tsv in this repo, the online ![DrugCentral 2021](doc/images/DrugCentral%202021.png) database, and the drugcentral_lincs database (loaded above). In the knime workflow find the drugcentral_lincs PostgresSQL Connector ![image of PostgresSQL connector](doc/images/drugcentral_lincs-PostgresSQLConnctor.png) and change the address/port to point to the drugcentral_lincs database where you are hosting it.

