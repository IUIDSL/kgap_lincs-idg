## Example script to load the relationships and nodes into Neo4j server running in docker

# ```ld_neo4j_in_docker``` script requires environment variables set in shell
# (for security reasons, these are not set in the script) 
#
# NEO4J_AUTH
# NEO4J_USERNAME
# NEO4J_PASSWORD

Note: read scripts before running them (script contains *rm -Rf path* so you'll want to make sure your paths are correct!), scripts assume this repo is cloned to your home directory ~ and the neo4j database will be placed under ~/neo4j/ as well
- ```ld_neo4j_in_docker``` to load the neo4j community server in docker
- ```wait4bolt_outside``` used by ld_neo4j_in_docker to wait for neo4j db to come online (e.g. must be online to run cypher scripts to create indexes)
- indexes.cypher contains the cypher to create indexes, used by ld_neo4j_in_docker script
- ```clean_ev``` utility script to empty the ./e and ./v folders

