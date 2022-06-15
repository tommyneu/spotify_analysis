from neo4j import GraphDatabase
from neo4j.debug import watch

Driver = None

def create_connection(url="localhost:7687", username="neo4j", password="neo4j"):
    global Driver
    uri = "neo4j://" + url
    Driver = GraphDatabase.driver(uri, auth=(username, password))

def close_connection():
    global Driver
    Driver.close()

def connect_nodes(node_a_type, node_a_id, node_b_type, node_b_id):
    types = [node_a_type.upper(), node_b_type.upper()]

    if "TRACK" in types and "ALBUM" in types:
        if node_a_type.upper() == "TRACK":
            return connect_track_and_album(node_a_id, node_b_id)
        return connect_track_and_album(node_b_id, node_a_id)

    if "TRACK" in types and "ARTIST" in types:
        if node_a_type.upper() == "TRACK":
            return connect_track_and_artist(node_a_id, node_b_id)
        return connect_track_and_artist(node_b_id, node_a_id)

    if "ARTIST" in types and "ALBUM" in types:
        if node_a_type.upper() == "ARTIST":
            return connect_artist_and_album(node_a_id, node_b_id)
        return connect_artist_and_album(node_b_id, node_a_id)

    if "ARTIST" in types and "GENRE" in types:
        if node_a_type.upper() == "ARTIST":
            return connect_artist_and_genre(node_a_id, node_b_id)
        return connect_artist_and_genre(node_b_id, node_a_id)

def connect_track_and_album(track_id, album_id):
    global Driver

    def connect_track_and_album_query(tx):
        result = tx.run("""
            MATCH
                (t:Track),
                (b:Album)
            WHERE t.id = $track_id AND b.id = $album_id
            MERGE (t)-[i:In]->(b)
            RETURN i
        """, 
            track_id=track_id,
            album_id=album_id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(connect_track_and_album_query)

    return [record for record in result]

def connect_track_and_artist(track_id, artist_id):
    global Driver

    def connect_track_and_artist_query(tx):
        result = tx.run("""
            MATCH
                (t:Track),
                (a:Artist)
            WHERE t.id = $track_id AND a.id = $artist_id
            MERGE (a)-[w:Preformed]->(t)
            RETURN w
        """, 
            track_id=track_id,
            artist_id=artist_id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(connect_track_and_artist_query)

    return [record for record in result]

def connect_artist_and_album(artist_id, album_id):
    global Driver

    def connect_artist_and_album_query(tx):
        result = tx.run("""
            MATCH
                (a:Artist),
                (b:Album)
            WHERE a.id = $artist_id AND b.id = $album_id
            MERGE (a)-[p:Produced]->(b)
            RETURN p
        """, 
            artist_id=artist_id,
            album_id=album_id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(connect_artist_and_album_query)

    return [record for record in result]

def connect_artist_and_genre(artist_id, genre_name):
    global Driver

    def connect_artist_and_genre_query(tx):
        result = tx.run("""
            MATCH
                (a:Artist),
                (g:Genre)
            WHERE a.id = $artist_id AND g.name = $genre_name
            MERGE (a)-[u:Uses]->(g)
            RETURN u
        """, 
            artist_id=artist_id,
            genre_name=genre_name
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(connect_artist_and_genre_query)

    return [record for record in result]

#   _______             _
#  |__   __|           | |
#     | |_ __ __ _  ___| | __
#     | | '__/ _` |/ __| |/ /
#     | | | | (_| | (__|   <
#     |_|_|  \__,_|\___|_|\_\
def create_track_node(id):
    global Driver

    def create_track_query(tx):
        result = tx.run("MERGE (t:Track{id:$id}) RETURN t", 
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(create_track_query)

    return [record for record in result]

def set_track_property(id, propertyName, propertyValue):
    global Driver

    def set_track_property_query(tx):
        result = tx.run("""
            MATCH (t:Track{id:$id}) 
            SET t.""" + propertyName + """ = $value
            RETURN t
            """, 
            id=id,
            value=propertyValue
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(set_track_property_query)

    return [record for record in result]

def get_track_node(id):
    global Driver

    def get_track_query(tx):
        result = tx.run("MATCH (t:Track{id:$id}) RETURN t", 
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_track_query)

    return [record for record in result]

def get_all_track_nodes():
    global Driver

    def get_all_track_query(tx):
        result = tx.run("MATCH (t:Track) RETURN t"
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_all_track_query)

    return [record for record in result]

def delete_track_node(id):
    global Driver

    def delete_track_query(tx):
        tx.run("MATCH (t:Track{id:$id}) DELETE t", 
            id=id
        ).data()

    with Driver.session() as session:
        session.write_transaction(delete_track_query)


#            _ _
#      /\   | | |
#     /  \  | | |__  _   _ _ __ ___
#    / /\ \ | | '_ \| | | | '_ ` _ \
#   / ____ \| | |_) | |_| | | | | | |
#  /_/    \_\_|_.__/ \__,_|_| |_| |_|
def create_album_node(id):
    global Driver

    def create_album_query(tx):
        result = tx.run("MERGE (b:Album{id:$id}) RETURN b",
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(create_album_query)

    return [record for record in result]

def set_album_property(id, propertyName, propertyValue):
    global Driver

    def set_album_property_query(tx):
        result = tx.run("""
            MATCH (b:Album{id:$id}) 
            SET b.""" + propertyName + """ = $value
            RETURN b
            """, 
            id=id,
            value=propertyValue
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(set_album_property_query)

    return [record for record in result]

def get_album_node(id):
    global Driver

    def get_album_query(tx):
        result = tx.run("MATCH (b:Album{id:$id}) RETURN b",
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_album_query)

    return [record for record in result]

def get_all_album_nodes():
    global Driver

    def get_all_album_query(tx):
        result = tx.run("MATCH (b:Album) RETURN b"
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_all_album_query)

    return [record for record in result]

def delete_album_node(id):
    global Driver

    def delete_album_query(tx):
        tx.run("MATCH (b:Album{id:$id}) DELETE b", 
            id=id
        ).data()

    with Driver.session() as session:
        session.write_transaction(delete_album_query)

#                 _   _     _
#      /\        | | (_)   | |
#     /  \   _ __| |_ _ ___| |_
#    / /\ \ | '__| __| / __| __|
#   / ____ \| |  | |_| \__ \ |_
#  /_/    \_\_|   \__|_|___/\__|
def create_artist_node(id):
    global Driver

    def create_artist_query(tx):
        result = tx.run("MERGE (a:Artist{id:$id}) RETURN a",
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(create_artist_query)

    return [record for record in result]

def set_artist_property(id, propertyName, propertyValue):
    global Driver

    def set_artist_property_query(tx):
        result = tx.run("""
            MATCH (a:Artist{id:$id}) 
            SET a.""" + propertyName + """ = $value
            RETURN a
            """, 
            id=id,
            value=propertyValue
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(set_artist_property_query)

    return [record for record in result]

def get_artist_node(id):
    global Driver

    def get_artist_query(tx):
        result = tx.run("MATCH (a:Artist{id:$id}) RETURN a", 
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_artist_query)

    return [record for record in result]

def get_all_artist_nodes():
    global Driver

    def get_all_artist_query(tx):
        result = tx.run("MATCH (a:Artist) RETURN a"
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_all_artist_query)

    return [record for record in result]

def delete_artist_node(id):
    global Driver

    def delete_artist_query(tx):
        tx.run("MATCH (a:Artist{id:$id}) DELETE a", 
            id=id
        ).data()

    with Driver.session() as session:
        session.write_transaction(delete_artist_query)



def create_genre_node(name):
    global Driver

    def create_genre_query(tx):
        result = tx.run("MERGE (g:Genre{name:$name}) RETURN g",
            name=name
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(create_genre_query)

    return [record for record in result]

def set_genre_property(name, propertyName, propertyValue):
    global Driver

    def set_genre_property_query(tx):
        result = tx.run("""
            MATCH (g:Genre{name:$name}) 
            SET g.""" + propertyName + """ = $value
            RETURN g
            """, 
            name=name,
            value=propertyValue
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(set_genre_property_query)

    return [record for record in result]

def get_genre_node(name):
    global Driver

    def get_genre_query(tx):
        result = tx.run("MATCH (g:Genre{name:$name}) RETURN g", 
            name=name
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_genre_query)

    return [record for record in result]

def get_all_genre_nodes():
    global Driver

    def get_all_genre_query(tx):
        result = tx.run("MATCH (g:Genre) RETURN g"
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_all_genre_query)

    return [record for record in result]

def delete_genre_node(name):
    global Driver

    def delete_genre_query(tx):
        tx.run("MATCH (g:Genre{name:$name}) DELETE g", 
            name=name
        ).data()

    with Driver.session() as session:
        session.write_transaction(delete_genre_query)