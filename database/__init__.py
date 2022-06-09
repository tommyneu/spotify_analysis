from lib2to3.pgen2 import driver
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


#   _______             _
#  |__   __|           | |
#     | |_ __ __ _  ___| | __
#     | | '__/ _` |/ __| |/ /
#     | | | | (_| | (__|   <
#     |_|_|  \__,_|\___|_|\_\
def create_track_node(id):
    global Driver

    def create_track_query(tx):
        result = tx.run("CREATE (t:Track{id:$id}) RETURN t", 
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
        result = tx.run("CREATE (b:Album{id:$id}) RETURN b",
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
        result = tx.run("CREATE (a:Artist{id:$id}) RETURN a",
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

def delete_artist_node(id):
    global Driver

    def delete_artist_query(tx):
        tx.run("MATCH (a:Artist{id:$id}) DELETE a", 
            id=id
        ).data()

    with Driver.session() as session:
        session.write_transaction(delete_artist_query)