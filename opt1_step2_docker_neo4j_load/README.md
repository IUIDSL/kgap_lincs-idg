## Example script to load the relationships and nodes into Neo4j server running in docker

Carefully READ through the entire ```ld_neo4j_in_docker``` script before running it.  It is designed to be run, and rerun, therefore it contains an **rm -Rf path** cleanup command, so you really do need to make sure your paths are correct! Scripts assume this repository is cloned to your home directory ~ and the neo4j database will be placed under ~/neo4j/ as well.  Process tested with Neo4j community version 4.2.0, and relies on the Neo4j Plugins apoc and graph data science library.  This script directs the docker image to retrieve the correct plugin versions for the specified release of Neo4j. (automatic)

```ld_neo4j_in_docker``` script requires environment variables set in shell
(for security reasons, these are not set in the script) 

    NEO4J_AUTH
    NEO4J_USERNAME
    NEO4J_PASSWORD


- ```ld_neo4j_in_docker``` to load the neo4j community server in docker
- ```wait4bolt_outside``` used by ld_neo4j_in_docker to wait for neo4j db to come online (e.g. must be online to run cypher scripts to create indexes)
- indexes.cypher contains the cypher to create indexes, used by ld_neo4j_in_docker script
- ```clean_ev``` utility script to empty the ./e and ./v folders, which are populated by the knime script in step1

