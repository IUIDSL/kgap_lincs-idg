WARNING:  Preparation is required before running these on a different machine
- First arrange the directories and files referenced in the Knime workflow (including the entire postgres dump file)
- then edit the Java Edit Variable named "PATH source score", it designed for directories (or symlinks) to be under $HOME

Knime workflows developed to create nodes and edges for each of the three prototype neo4j graphs
- lymphoma
- landmark
- all

Notes: Knime was developed on ubuntu, it might require minor changes to run on other OSs (e.g. $HOME variable?)
