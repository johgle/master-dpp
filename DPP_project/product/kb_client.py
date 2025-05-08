"""
Class to handle the communication with the Knowledge Base server.
Used to send SPARQL queries to the server and receive the results.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import requests
import re


URL = "http://127.0.0.1:3030/dpp"

# For å starte Fuseki server:
# kjør i Command prompt:
# cd C:\Users\Johanne\Downloads\apache-jena-fuseki-5.3.0\apache-jena-fuseki-5.3.0>
# fuseki-server


def ask_query(query):
    PARAMS = {"query": query}
    # print("PARAMS:", PARAMS)
    resp = requests.get(url = URL, params = PARAMS) 
    print("response: ", resp)
    if resp.status_code == 400 or resp.status_code == 404:
        return "Data was not found."
    return resp.json()["results"]["bindings"]

def update_kb(query):
    PARAMS = {"update": query}
    try:
        resp = requests.post(url=URL + "/update", data=PARAMS, timeout=5)
        if resp.status_code == 400:
            return "Bad request (400)"
        elif resp.status_code == 404:
            return "Data not found (404)"
        elif not resp.ok:
            return f"Unhandled error: {resp.status_code}"
        return resp
    except requests.exceptions.RequestException as e:
        return f"Network or connection error: {e}"

# Skal vi legge til annet enn DPP i databasen?
def make_insert_product_query(id: str, name: str, type: str, mass: float, volume: float, parts: list[dict]):
    """Create a SPARQL query to insert a product and its parts into the knowledge base."""
    PREFIXES = '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    '''

    # The product
    product_part_ids = ", ".join(f'dpp:{p["id"]}' for p in parts)
    product = f'''
    dpp:{id} a dpp:{type} ;
        dpp:hasName    "{name}" ;
        dpp:hasMass    "{mass}"^^xsd:float ;
        dpp:hasVolume  "{volume}"^^xsd:float ;
        dpp:consistsOf {product_part_ids} .
    '''

    # Each part
    parts_block = ""
    for part in parts:
        parts_block += f'''
    dpp:{part["id"]} a dpp:Part ;
        dpp:hasName     "{part["name"]}" ;
        dpp:hasMass     "{part["mass"]}"^^xsd:float ;
        dpp:hasVolume   "{part["volume"]}"^^xsd:float ;
        dpp:hasMaterial "{part["material"]}" .
    '''

    # Put the query together
    query = f"""{PREFIXES}
    INSERT DATA {{
    {product}
    {parts_block}
    }}
    """
    return query

def make_insert_actor_query(id: str, name: str, mail: str, owns: list[str] = None):
    """Create a SPARQL query to insert an actor into the knowledge base."""
    
    owns = owns or []  # Håndterer None som tom liste
    owns = [item.strip() for item in owns if item.strip()]  # Fjerner tomme strenger

    owner_line = ""
    if owns:
        owned_items = ", ".join(f"dpp:{item}" for item in owns)
        owner_line = f"\n            dpp:ownerOf  {owned_items} ;"

    query = f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        dpp:{id}
            a            dpp:Actor ;
            dpp:hasName  "{name}" ;
            dpp:hasMail  "{mail}" ;
            dpp:hasID    "{id}" ;{owner_line}
    }}
    '''

    # Fjerner semikolon før siste } hvis owner_line er tom (for korrekt syntaks)
    query = re.sub(r';\s*}', ' }', query)

    return query

def make_insert_DPP_query(dpp_id: str, product_id: str, timestamp: str, actor_id: str):
    """Create a SPARQL query to insert a Digital Product Passport (DPP) into the knowledge base."""
    query = f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        dpp:{dpp_id}
            a                     dpp:Product_DPP ;
            dpp:hasID             "{dpp_id}" ;
            dpp:describes         dpp:{product_id} ;
            dpp:hasTimeStampCreation "{timestamp}"^^xsd:dateTime ;
            dpp:responsibleActor  dpp:{actor_id} .
    }}
    '''
    return query



actor_id = "Actor_ErikEriksen"
actor_name = "Erik Eriksen"
actor_mail = "ee@mail.com"
owns_list = [""]

# print(make_insert_actor_query(
#     id=actor_id,
#     name=actor_name,
#     mail=actor_mail,
#     owns=owns_list
# ))

# print(update_kb(make_insert_actor_query(
#     id=actor_id,
#     name=actor_name,
#     mail=actor_mail,
#     owns=owns_list
# )))

request_actor_query = '''
PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>

SELECT ?id ?name ?mail ?ownerOf WHERE {
  ?actor dpp:hasID ?id ;
        dpp:hasName ?name ;
        dpp:hasMail ?mail .
  OPTIONAL {
    ?actor dpp:ownerOf ?ownerOf .
  }
}

 '''
# print(ask_query(request_actor_query))

















QUERY_add_chair = (
    # A new chair product
    '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {
    dpp:ChairExample a dpp:Product ;
        dpp:hasName    "Example Chair" ;
        dpp:hasMass    "10.0"^^xsd:float ;
        dpp:hasVolume  "0.014"^^xsd:float ;
        dpp:consistsOf dpp:Leg1,
                        dpp:Leg2,
                        dpp:Leg3,
                        dpp:Leg4,
                        dpp:SeatPlate,
                        dpp:BackPlate .

    # The four legs
    dpp:Leg1 a dpp:Part ;
        dpp:hasName     "Chair Leg" ;
        dpp:hasMass     "1.5"^^xsd:float ;
        dpp:hasVolume   "0.002"^^xsd:float ;
        dpp:hasMaterial "Birch" .

    dpp:Leg2 a dpp:Part ;
        dpp:hasName     "Chair Leg" ;
        dpp:hasMass     "1.5"^^xsd:float ;
        dpp:hasVolume   "0.002"^^xsd:float ;
        dpp:hasMaterial "Birch" .

    dpp:Leg3 a dpp:Part ;
        dpp:hasName     "Chair Leg" ;
        dpp:hasMass     "1.5"^^xsd:float ;
        dpp:hasVolume   "0.002"^^xsd:float ;
        dpp:hasMaterial "Birch" .

    dpp:Leg4 a dpp:Part ;
        dpp:hasName     "Chair Leg" ;
        dpp:hasMass     "1.5"^^xsd:float ;
        dpp:hasVolume   "0.002"^^xsd:float ;
        dpp:hasMaterial "Birch" .

    # The seating plate
    dpp:SeatPlate a dpp:Part ;
        dpp:hasName     "Seat Plate" ;
        dpp:hasMass     "2.0"^^xsd:float ;
        dpp:hasVolume   "0.003"^^xsd:float ;
        dpp:hasMaterial "Birch" .

    # The back plate
    dpp:BackPlate a dpp:Part ;
        dpp:hasName     "Back Plate" ;
        dpp:hasMass     "2.0"^^xsd:float ;
        dpp:hasVolume   "0.003"^^xsd:float ;
        dpp:hasMaterial "Birch" .
    }
''')

QUERY_add_chair_DPP = (
    # A new Digital Product Passport (DPP) for the example chair
    '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {
    dpp:ChairExample_DPP
            a               dpp:Product_DPP ;
            dpp:hasID       "ChairExample_DPP" ;
            dpp:describes   dpp:ChairExample ;
            dpp:hasTimeStampCreation "2025-05-07T12:00:00Z"^^xsd:dateTime ;
            dpp:responsibleActor dpp:Johanne_Glende .  
    }


    
''')

QUERY_add_actor = (
    # Define the actor Johanne Glende
    '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {
    dpp:Actor_JohanneGlende
            a            dpp:Actor ;
            dpp:hasName  "Johanne Glende" ;
            dpp:hasMail  "jg@mail.com" ;
            dpp:hasID    "JohanneGlende" ;
            dpp:ownerOf  dpp:ChairExample_DPP .
    }
''')

QUERY_update_chair_DPP = ('''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    DELETE {
    dpp:ChairExample_DPP dpp:hasID ?oldID .
    }
    INSERT {
    dpp:ChairExample_DPP dpp:hasID "ChairExample_DPP"^^xsd:string .
    }
    WHERE {
    OPTIONAL { dpp:ChairExample_DPP dpp:hasID ?oldID . }
    }

''')

QUERY_remove_chair_DPP = ('''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>

    DELETE WHERE {
    # ?p and ?o are variables matching any predicate and any object for the given subject, that is, ?p and ?o can be anything.
    dpp:ChairExample_DPP ?p ?o .
    }
''')

QUERY_remove_actor = ('''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>

    DELETE WHERE {
    dpp:Actor_JohanneGlende ?p ?o .
    }

''')

QUERY_remove_chair = ('''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>

    DELETE WHERE {
    dpp:ChairExample ?p ?o .
    }
''')

QUERY_request_Product_DPP_data = ('''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>

    SELECT ?id ?describes ?timeStamp ?responsibleActor
    WHERE {
        ?Product_DPP dpp:hasID ?id;
            dpp:describes ?describes;
            dpp:hasTimeStampCreation ?timeStamp;
            dpp:responsibleActor ?responsibleActor. }''')