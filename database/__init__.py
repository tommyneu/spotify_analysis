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

def create_track_node(id, name="", duration=0, explicit=True, popularity=0):
    global Driver

    def create_track_query(tx):
        result = tx.run("""
            CREATE (t:Track{
                id:$id, 
                name:$name,
                duration:$duration,
                explicit:$explicit,
                popularity: $popularity}) RETURN t
            """, 
            id=id, 
            name=name, 
            duration=duration, 
            explicit=explicit, 
            popularity=popularity
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(create_track_query)

    return [record for record in result]

def get_track_node(id):
    global Driver

    def get_track_query(tx):
        result = tx.run("""
            MATCH (t:Track{id:$id}) RETURN t
            """, 
            id=id
        ).data()
        return result

    with Driver.session() as session:
        result = session.write_transaction(get_track_query)

    return [record for record in result]
