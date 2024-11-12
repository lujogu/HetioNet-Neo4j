Hello! Below I have some preliminary 
steps for our Neo4j db to work:

When creating the Neo4j server, be sure to assign the password as 'password'

Inside the attached folder is two python scripts:
edgepartition.py
mainfile.py

Edgepartition should be run first. It will partition the edges.tsv file such that the 
creation of no single relationship exceeds the heap capacity of Neo4J. The generated files, 
including nodes.tsv and edges.tsv, should then be copied into the 'imports' folder of the Neo4j server. 

Next, in the server's config file (neo4j.conf), change the property dbms.memory.heap.max_size from 1G to 2G. 
This is necessary because the server will crash otherwise. 

Finally start the Neo4j server, either through the Desktop app or another distribution. 
The mainfile.py script will use the port accessed by the server to transmit queries. 

Thanks again,
Lucas and Nabeel
