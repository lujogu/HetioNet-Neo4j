from py2neo import Graph

# Create a Graph object using the default Neo4j credentials
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Example query to retrieve all nodes and relationships in the graph
query = """
MATCH (n)
RETURN n
"""

results = graph.run(query)
for record in results:
    print(record)
