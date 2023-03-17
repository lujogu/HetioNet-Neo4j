from py2neo import Graph

# Create a Graph object using the default Neo4j credentials
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Example query to retrieve all nodes and relationships in the graph
produce_graph = """
LOAD CSV FROM "file:///nodes.tsv" AS row FIELDTERMINATOR ' ';
CREATE(:Node{{id: row[0], name: row[1], kind:row[2]}}}});

CREATE TEXT INDEX FOR (n:Node) ON (n.id);

MATCH (n:Node)
WHERE n.id CONTAINS 'Anatomy'
SET n:Anatomy;

MATCH (n:Node)
WHERE n.id CONTAINS 'Gene'
SET n:Gene;

MATCH (n:Node)
WHERE n.id CONTAINS 'Disease'
SET n:Disease;

MATCH (n:Node)
WHERE n.id CONTAINS 'Compound'
SET n:Compound;

LOAD CSV FROM 'file:///AdG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'AdG'
CREATE (a)-[:DOWNREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///AeG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'AeG'
CREATE (a)-[:EXPRESSES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///AuG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'AuG'
CREATE (a)-[:UPREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CbG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CbG'
CREATE (a)-[:BINDS{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CdG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CdG'
CREATE (a)-[:DOWNREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CpD.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CpD'
CREATE (a)-[:PALLIATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CrC.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CrC'
CREATE (a)-[:RESEMBLES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CtD.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CtD'
CREATE (a)-[:TREATS{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///CuG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'CuG'
CREATE (a)-[:UPREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///DaG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'DaG'
CREATE (a)-[:ASSOCIATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///DdG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'DdG'
CREATE (a)-[:DOWNREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///DlA.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'DlA'
CREATE (a)-[:LOCALIZES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///DrD.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'DrD'
CREATE (a)-[:RESEMBLES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///DuG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'DuG'
CREATE (a)-[:UPREGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///GcG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'GcG'
CREATE (a)-[:COVARIES{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///GiG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'GiG'
CREATE (a)-[:INTERACTS{{metaedge: edge[1]}}]->(b) RETURN a,b;

LOAD CSV FROM 'file:///GrG.tsv' AS edge FIELDTERMINATOR '   '
MATCH (a:Node{{id:edge[0]}}), (b:Node{{id:edge[2]}}) WHERE edge[1] = 'GrG'
CREATE (a)-[:REGULATES{{metaedge: edge[1]}}]->(b) RETURN a,b;

CREATE TEXT INDEX FOR (n:Disease) ON (n.name)
"""

def query_one(param):
    query = """
    MATCH (d:Disease{{name:{}}})
    OPTIONAL MATCH (d)<-[:TREATS]-(c:Compound)
    OPTIONAL MATCH (d)<-[:PALLIATES]-(c:Compound)
    OPTIONAL MATCH (d)<-[:DOWNREGULATES]-(g:Gene)
    OPTIONAL MATCH (d)<-[:UPREGULATES]-(g:Gene)
    OPTIONAL MATCH (d)<-[:LOCALIZES]-(a:Anatomy)
    RETURN d.name AS disease_name, 
        COLLECT(DISTINCT c.name) AS compound_names, 
        COLLECT(DISTINCT g.name) AS gene_names, 
        COLLECT(DISTINCT a.name) AS anatomy_names
    """.format(param)
    results = graph.run(query)
    for record in results:
        print(record)

results = graph.run(produce_graph)
print("graph produced!")
