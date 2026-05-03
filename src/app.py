from db import Neo4jConnection

conn = Neo4jConnection("neo4j://127.0.0.1:7687", "neo4j", "password")

current_user = None

# UC1
def register():
    username = input("Username: ")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")

    conn.run_query("""
    CREATE (:User {
        id: rand(),
        username: $username,
        name: $name,
        email: $email,
        password: $password,
        bio: ""
    })
    """, {
        "username": username,
        "name": name,
        "email": email,
        "password": password
    })

    print("User registered!")

# UC2
def login():
    global current_user
    username = input("Username: ")
    password = input("Password: ")

    result = conn.run_query("""
    MATCH (u:User {username:$u, password:$p})
    RETURN u
    """, {"u": username, "p": password})

    if result:
        current_user = username
        print("Logged in!")
    else:
        print("Invalid credentials")

# UC3
def view_profile():
    if not current_user:
        print("Please log in first.")
        return
    
    result = conn.run_query("""
    MATCH (u:User {username:$u})
    RETURN u.username, u.name, u.email, u.bio
    """, {"u": current_user})

    for r in result:
        print("Username:", r["u.username"])
        print("Name:", r["u.name"])
        print("Email:", r["u.email"])
        print("Bio:", r["u.bio"])

# UC4
def edit_profile():
    if not current_user:
        print("Please log in first.")
        return
    
    name = input("New name: ")
    bio = input("New bio: ")

    conn.run_query("""
    MATCH (u:User {username:$u})
    SET u.name = $name,
        u.bio = $bio
    """, {"u": current_user, "name": name, "bio": bio})

    print("Profile updated!")

# UC5
def follow():
    if not current_user:
        print("Please log in first.")
        return
    
    u2 = input("Follow who: ")

    conn.run_query("""
    MATCH (a:User {username:$u1}), (b:User {username:$u2})
    CREATE (a)-[:FOLLOWS]->(b)
    """, {"u1": current_user, "u2": u2})

    print("Followed!")

# UC6
def unfollow():
    if not current_user:
        print("Please log in first.")
        return
    
    u2 = input("Unfollow who: ")

    conn.run_query("""
    MATCH (a:User {username:$u1})-[r:FOLLOWS]->(b:User {username:$u2})
    DELETE r
    """, {"u1": current_user, "u2": u2})

    print("Unfollowed!")

# UC7
def view_connections():
    if not current_user:
        print("Please log in first.")
        return
    
    print("\nFollowers:")

    followers = conn.run_query("""
    MATCH (u:User {username:$u})<-[:FOLLOWS]-(f:User)
    RETURN DISTINCT f.username AS username
    """, {"u": current_user})

    if not followers:
        print("None")
    else:
        for f in followers:
            print(f["username"])

    print("\nFollowing:")

    following = conn.run_query("""
    MATCH (u:User {username:$u})-[:FOLLOWS]->(f:User)
    RETURN DISTINCT f.username AS username
    """, {"u": current_user})

    if not following:
        print("None")
    else:
        for f in following:
            print(f["username"])

# UC8
def mutual():
    if not current_user:
        print("Please log in first.")
        return
    
    u2 = input("Check mutual with: ")

    result = conn.run_query("""
    MATCH (a:User {username:$u1})-[:FOLLOWS]->(x)<-[:FOLLOWS]-(b:User {username:$u2})
    RETURN DISTINCT x.username
    """, {"u1": current_user, "u2": u2})

    for r in result:
        print("Mutual:", r["x.username"])
    if not result:
        print("No mutual connections")

# UC9
def recommend():
    if not current_user:
        print("Please log in first.")
        return

    result = conn.run_query("""
    MATCH (u:User {username:$u})-[:FOLLOWS]->(a:User)-[:FOLLOWS]->(b:User)
    WHERE NOT (u)-[:FOLLOWS]->(b) AND u <> b
    RETURN DISTINCT b.username AS rec, a.username AS via
    """, {"u": current_user})

    if not result:
        print("No recommendations found.")
        return

    print("\nRecommended Users:")
    for r in result:
        print(f"Recommended: {r['rec']} - friends with {r['via']}")

# UC10
def search():
    if not current_user:
        print("Please log in first.")
        return

    name = input("Search username: ")

    result = conn.run_query("""
    MATCH (u:User)
    WHERE toLower(u.username) CONTAINS toLower($name)
    RETURN DISTINCT u.username AS username
    """, {"name": name})

    print(f"\nSearch Results for '{name}':")

    if not result:
        print("No users found.")
        return

    for r in result:
        print(f"- {r['username']}")

# UC11
def popular():
    if not current_user:
        print("Please log in first.")
        return

    result = conn.run_query("""
    MATCH (u:User)<-[:FOLLOWS]-(f:User)
    RETURN u.username AS username, COUNT(f) AS followers
    ORDER BY followers DESC
    LIMIT 5
    """)

    print("\nMost Popular Users\n-------------------")

    if not result:
        print("No users found.")
        return

    for r in result:
        print(f"{r['username']} - {r['followers']} followers")

def menu():
    while True:
        print("\nMENU")
        print("1 Register")
        print("2 Login")
        print("3 View Profile")
        print("4 Edit Profile")
        print("5 Follow")
        print("6 Unfollow")
        print("7 View Connections")
        print("8 Mutual")
        print("9 Recommend")
        print("10 Search")
        print("11 Popular")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1": register()
        elif choice == "2": login()
        elif choice == "3": view_profile()
        elif choice == "4": edit_profile()
        elif choice == "5": follow()
        elif choice == "6": unfollow()
        elif choice == "7": view_connections()
        elif choice == "8": mutual()
        elif choice == "9": recommend()
        elif choice == "10": search()
        elif choice == "11": popular()
        elif choice == "0": break

menu()