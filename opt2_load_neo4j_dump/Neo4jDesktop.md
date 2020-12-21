
# Load dump file in Neo4j Desktop

1. create a new 4.2 database (do not start the database)
2. click on the ... and click **Manage** in the pop up menu, click on **Open Terminal**
3. restore the database from dump file with command

`bin/neo4j-admin load --from=pathtofile/dclneodb.dump --database=neo4j`

4. exit terminal, click **Start** the database
5. click **Open**, to use built in neo4j browser to query and explore

Note: instructions tested on MacBookPro 2017 - MacOS Catalina
