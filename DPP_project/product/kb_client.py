"""
Class to handle the communication with the Knowledge Base server.
Used to send SPARQL queries to the server and receive the results.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import requests
import re

from DPP_project.product.actual_product.product import Product
from DPP_project.product.actor.actor import Actor
from DPP_project.product.digital_product_passport.product_dpp import DPP


# For å starte Fuseki server:
# kjør i Command prompt:
# cd C:\Users\Johanne\Downloads\apache-jena-fuseki-5.3.0\apache-jena-fuseki-5.3.0
# fuseki-server

URL = "http://127.0.0.1:3030/dpp"

# Method to get data from the knowledge base
# --------------------------------------------------
def ask_query(query):
    PARAMS = {"query": query}
    # print("PARAMS:", PARAMS)
    resp = requests.get(url = URL, params = PARAMS) 
    print("response: ", resp)
    if resp.status_code == 400 or resp.status_code == 404:
        return "Data was not found."
    return resp.json()["results"]["bindings"]

# Method to update the knowledge base
# --------------------------------------------------
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

# Methods that makes queries to add data to the knowledge base
# --------------------------------------------------
def make_insert_product_query(product: Product):
    """Create a SPARQL query to insert a product and its parts into the knowledge base."""
    
    # Extract product properties
    id = product.id
    name = product.name
    parts = product.parts # a list with Part instances [Part1, Part2, etc.]
    
    PREFIXES = '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    '''
    
    # Build the product properties
    product_part_ids = ", ".join(f'dpp:{p.id}' for p in parts)
    # print("product_part_ids:",product_part_ids)
    product = f'''
    dpp:{id} a dpp:Product ;
        dpp:hasID      "{id}" ;
        dpp:hasName    "{name}" ;
        dpp:consistsOf {product_part_ids} .
    '''

    # Each part
    parts_block = ""
    for part in parts:
        parts_block += f'''
    dpp:{part.id} a dpp:Part ;
        dpp:hasID       "{part.id}" ;
        dpp:hasName     "{part.name}" ;
        dpp:hasMass     "{part.mass}"^^xsd:float ;
        dpp:hasVolume   "{part.volume}"^^xsd:float ;
        dpp:hasMaterial "{part.material}" .
    '''

    # Construct the full query
    query = f"""{PREFIXES}
    INSERT DATA {{
    {product}
    {parts_block}
    }}
    """
    return query

def make_insert_actor_query(actor: Actor):
    """Create a SPARQL query to insert an actor into the knowledge base."""
    
    # Extract actor properties
    id = actor.id
    name = actor.name
    mail = actor.mail
    owns = actor.owner_of or []  # Handle None as empty list
    
    # Build the properties list
    properties = [
        f"a            dpp:Actor",
        f'dpp:hasName  "{name}"',
        f'dpp:hasMail  "{mail}"',
        f'dpp:hasID    "{id}"'
    ]
    
    if owns:
        owned_items = ", ".join(f"dpp:{item.id}" for item in owns)
        properties.append(f"dpp:ownerOf  {owned_items}")
    
    properties_str = " ;\n            ".join(properties) + " ."
    
    # Construct the full query
    query = f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT DATA {{
        dpp:{id} {properties_str}
    }}
    '''
    
    return query

def make_insert_dpp_query(dpp: DPP): 
    """Create a SPARQL query to insert a Digital Product Passport (DPP) into the knowledge base."""
    
    # Extract dpp properties
    dpp_id = dpp.id
    product_id = dpp.describes.id
    timestamp = dpp.timeStamp
    actor_id = dpp.responsibleActor.id
    
    # Construct query
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

        dpp:{actor_id}
            a                     dpp:Actor ;
            dpp:ownerOf           dpp:{dpp_id} .
    }}
    '''
    return query

# Methods that make queries to remove data from the knowledge base
# --------------------------------------------------
def make_remove_product_query(product: Product):
    """Create a SPARQL query to remove a product and its parts from the knowledge base."""
    
    product_id = product.id
    part_ids = [part.id for part in product.parts]

    PREFIXES = '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    '''

    delete_blocks = f'''
    DELETE {{
        dpp:{product_id} ?p ?o .
    }}
    WHERE {{
        dpp:{product_id} ?p ?o .
    }} ;

    DELETE {{
        ?s ?p dpp:{product_id} .
    }}
    WHERE {{
        ?s ?p dpp:{product_id} .
    }} ;
    '''

    for part_id in part_ids:
        delete_blocks += f'''
    DELETE {{
        dpp:{part_id} ?p ?o .
    }}
    WHERE {{
        dpp:{part_id} ?p ?o .
    }} ;
    '''

    return f"{PREFIXES}\n{delete_blocks}"

def make_remove_actor_query(actor: Actor):
    """Create a SPARQL query to remove an actor from the knowledge base."""

    actor_id = actor.id

    return f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    DELETE {{
        dpp:{actor_id} ?p ?o .
    }}
    WHERE {{
        dpp:{actor_id} ?p ?o .
    }} ;

    DELETE {{
        ?s ?p dpp:{actor_id} .
    }}
    WHERE {{
        ?s ?p dpp:{actor_id} .
    }} ;
    '''

def make_remove_dpp_query(dpp: DPP):
    """Create a SPARQL query to remove a Digital Product Passport (DPP) from the knowledge base."""

    dpp_id = dpp.id

    return f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    DELETE {{
        dpp:{dpp_id} ?p ?o .
    }}
    WHERE {{
        dpp:{dpp_id} ?p ?o .
    }} ;

    DELETE {{
        ?s ?p dpp:{dpp_id} .
    }}
    WHERE {{
        ?s ?p dpp:{dpp_id} .
    }} ;

    '''














# ----------------- TEST QUERIES ------------------ #
# Test queries to add data to the knowledge base
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