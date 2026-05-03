import pandas as pd
from db import Neo4jConnection

conn = Neo4jConnection("neo4j://127.0.0.1:7687", "neo4j", "password")

# Load nodes
users = pd.read_csv("data/nodes.csv")
# ONLY keep rows where type == "User"
users = users[users["type"] == "User"]

for _, row in users.iterrows():
    conn.run_query("""
    MERGE (u:User {id: $id})
    SET u.username = $username,
        u.name = $username,
        u.email = $username + "@example.com",
        u.password = "password123",
        u.bio = ""
    """, {
        "id": int(row["node_id"]),
        "username": str(row["name"])
})

print("Users loaded!")

# Load edges
edges = pd.read_csv("data/edges.csv")

for _, row in edges.iterrows():
    conn.run_query("""
    MATCH (a:User {id: $src}), (b:User {id: $dst})
    WHERE a IS NOT NULL AND b IS NOT NULL
    CREATE (a)-[:FOLLOWS]->(b)
    """, {
        "src": int(row["source_id"]),
        "dst": int(row["target_id"])
    })

print("Edges loaded!")

conn.close()