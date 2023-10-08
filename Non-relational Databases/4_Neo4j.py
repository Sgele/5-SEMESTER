from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
from gdsclient import Neo4jQueryRunner, GraphDataScience

gds = GraphDatabase.driver(uri="neo4j://localhost:7687", auth=("neo4j", "test"))
session = gds.session()

clearDatabase = "MATCH (n) DETACH DELETE (n)"
nodes = session.run(clearDatabase)

createDatabase = "MERGE (vilnius:City {name: 'Vilnius'})" \
                 "MERGE (kaunas:City {name: 'Kaunas'})" \
                 "MERGE (siauliai:City {name: 'Siauliai'})" \
                 "MERGE (varena:City {name: 'Varena'})" \
                 "MERGE (klaipeda:City {name: 'Klaipeda'})" \
                 "MERGE (marijampole:City {name: 'Marijampole'})" \
                 "MERGE (trainA:Train {name: 'Train VLN - KLP'})" \
                 "MERGE (trainB:Train {name: 'Train VLN - VRN'})" \
                 "MERGE (trainC:Train {name: 'Train VLN - KN'})" \
                 "MERGE (trainD:Train {name: 'Train KN - SL'})" \
                 "MERGE (trainE:Train {name: 'Train KN - MRL'})" \
                 "MERGE (trainA) -[:TRAVEL_TO]-> (vilnius)" \
                 "MERGE (trainA) -[:TRAVEL_TO]-> (klaipeda)" \
                 "MERGE (trainB) -[:TRAVEL_TO]-> (vilnius)" \
                 "MERGE (trainB) -[:TRAVEL_TO]-> (varena)" \
                 "MERGE (trainC) -[:TRAVEL_TO]-> (vilnius)" \
                 "MERGE (trainC) -[:TRAVEL_TO]-> (kaunas)" \
                 "MERGE (trainD) -[:TRAVEL_TO]-> (kaunas)"  \
                 "MERGE (trainD) -[:TRAVEL_TO]-> (siauliai)" \
                 "MERGE (trainE) -[:TRAVEL_TO]-> (kaunas)" \
                 "MERGE (trainE) -[:TRAVEL_TO]-> (marijampole)" \
                 "MERGE (vilnius) -[:ROAD {cost: 23}]-> (klaipeda)" \
                 "MERGE (klaipeda) -[:ROAD {cost: 32}]-> (vilnius)" \
                 "MERGE (klaipeda) -[:ROAD {cost: 35}]-> (vilnius)" \
                 "MERGE (vilnius) -[:ROAD {cost: 6}]-> (varena)" \
                 "MERGE (varena) -[:ROAD {cost: 4}]-> (vilnius)" \
                 "MERGE (vilnius) -[:ROAD {cost: 10}]-> (kaunas)" \
                 "MERGE (kaunas) -[:ROAD {cost: 8}]-> (vilnius)" \
                 "MERGE (kaunas) -[:ROAD {cost: 15}]-> (siauliai)" \
                 "MERGE (kaunas) -[:ROAD {cost: 20}]-> (siauliai)" \
                 "MERGE (kaunas) -[:ROAD {cost: 5}]-> (marijampole)" \
                 "MERGE (marijampole) -[:ROAD {cost: 6}]-> (kaunas)" \

nodes2 = session.run(createDatabase)

def findTrainByName(train_name):
    train_by_name = f"MATCH (train:Train{{name:'{train_name}'}}) RETURN train"
    nodes = session.run(train_by_name)
    print("Train:")
    for node in nodes:
        print(node)


def findTrainsByPartialName(part):
    train_by_partial_name = f"MATCH (train:Train) WHERE train.name CONTAINS '{part}' RETURN train"
    nodes = session.run(train_by_partial_name)
    print("")
    print(f"Trains with {part} in their name: ")
    for node in nodes:
        print(node)

def findTrainStopsForATrain(train_name):
    train_stops = f"MATCH cities = (train:Train {{name: '{train_name}'}}) -[:TRAVEL_TO]- (city) RETURN cities, city.name as cityName"
    nodes = session.run(train_stops)
    print("")
    print(f"Stops for a train {train_name}:")
    for node in nodes:
        print(node)

def findAllPaths(city1, city2):
    paths = f"MATCH p = (a:City{{name:'{city1}'}})-[:ROAD*]-(b:City{{name:'{city2}'}}) unwind nodes(p) as node with p, collect(node.name) as names RETURN Distinct names"
    nodes = session.run(paths)
    print("")
    print(f"Paths between {city1} and {city2}:")
    for node in nodes:
        print(node)

def findShortestPath(city1, city2):
    shortest_path = f"MATCH(a:City{{name: '{city1}'}}), (b:City{{name: '{city2}'}}), p = shortestPath((a)-[:ROAD*]-(b)) RETURN nodes(p)"
    nodes = session.run(shortest_path)
    print("")
    print(f"Shortest path between {city1} and {city2}:")
    for node in nodes:
        print(node)

def findCostOfTrip(city1, city2):
    cost_of_trip = f"MATCH p=(a:City{{name:'{city1}'}})-[:ROAD*]->(b:City{{name:'{city2}'}}) unwind nodes(p) as node with p, collect(node.name) as names RETURN names, reduce(sum=0, x in relationships(p) | sum + x.cost) as cost"
    nodes = session.run(cost_of_trip)
    print("")
    print(f"Paths between {city1} and {city2} with their costs:")
    for node in nodes:
        print(node)

def numberOfRoutes():
    routes = "MATCH (a:Train)-[:TRAVEL_TO]->(b:City) RETURN b.name as city, count(a) as numRoutes"
    nodes = session.run(routes)
    print("")
    print("Number of different routes:")
    for node in nodes:
        print(node)


findTrainByName('Train VLN - KLP')
findTrainsByPartialName('Train')
findTrainStopsForATrain('Train VLN - KLP')
findAllPaths('Vilnius', 'Siauliai')
findShortestPath('Vilnius', 'Siauliai')
findCostOfTrip('Vilnius', 'Marijampole')
numberOfRoutes()