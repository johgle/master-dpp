"""
Class to handle the communication with the Knowledge Base server.
Used to send SPARQL queries to the server and receive the results.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import requests

from product.actual_product.product import Product
from product.actor.actor import Actor
from product.digital_product_passport.product_dpp import DPP


# For å starte Fuseki server:
# kjør i Command prompt:
# cd C:\Users\Johanne\Downloads\apache-jena-fuseki-5.3.0\apache-jena-fuseki-5.3.0
# fuseki-server

URL = "http://127.0.0.1:3030/dpp"

# Method to get data from the knowledge base
# --------------------------------------------------
def ask_query(query):
    PARAMS = {"query": query}
    resp = requests.get(url = URL, params = PARAMS) 
    if resp.status_code == 400 or resp.status_code == 404:
        return "Data was not found."
    return resp.json()["results"]["bindings"]

# Method to update the knowledge base
# --------------------------------------------------
def update_kb(query):
    """ Used to INSERT or DELETE data to/from the knowledge base. """
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
    timestamp = dpp.timeStampInvalid
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
            dpp:hasTimeStampInvalid "{timestamp}"^^xsd:dateTime ;
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


def get_dpp_data(dpp_id):
    try:
        results = ask_query(make_get_dpp_product_actor_query(dpp_id))
        if not results:
            return None

        # Extract data from the query results
        dpp_data = results[0]  # Assuming one result per DPP_ID
        new_dpp_data = {
            "dpp_id": dpp_id,
            
            "describes": {
                "productID": dpp_data["productID"]["value"],
                "productName": dpp_data["productName"]["value"],
            },
            
            "timeStampInvalid": dpp_data["timeStampInvalid"]["value"],
            
            "responsibleActor": {
                "actorID": dpp_data["actorID"]["value"],
                "actorName": dpp_data["actorName"]["value"],
                "actorMail": dpp_data["actorMail"]["value"],
            },

            "allParts": [part.split("/")[-1] for part in dpp_data["allParts"]["value"].split(",")]  # Combined logic

        }

        # Fetch parts data
        parts_query = make_get_parts_data_query(new_dpp_data["allParts"])
        parts_results = ask_query(parts_query)
        if not parts_results:
            return None

        # Create a dictionary for parts data
        parts_data = []
        for part in parts_results:
            part_data = {
                "partID": part["partID"]["value"],
                "partName": part["partName"]["value"],
                "partMass": float(part["partMass"]["value"]),
                "partVolume": float(part["partVolume"]["value"]),
                "partMaterial": part["partMaterial"]["value"],
            }
            parts_data.append(part_data)

        # Add parts data to new_dpp_data
        new_dpp_data["parts"] = parts_data
        
        return new_dpp_data
    
    except Exception as e:
        print(f"Error fetching DPP data for ID {dpp_id}: {e}")
        return None


def make_get_dpp_product_actor_query(dpp_id):
    """
    Fetch data for a Digital Product Passport (DPP) from the knowledge base using its ID,
    including details about the product and its parts, with aggregation to avoid long results.
    """
    query = f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?dppID ?timeStampInvalid ?productID ?productName 
        (GROUP_CONCAT(?product_parts; separator=", ") AS ?allParts)
        ?actorID ?actorName ?actorMail
    WHERE {{
    dpp:{dpp_id} a dpp:Product_DPP ;
        dpp:hasID ?dppID ;
        dpp:hasTimeStampInvalid ?timeStampInvalid ;
        dpp:describes ?product ;
        dpp:responsibleActor ?actor .

    ?product a dpp:Product ;
        dpp:hasID ?productID ;
        dpp:hasName ?productName ;
        dpp:consistsOf ?product_parts .

    ?actor a dpp:Actor ;
        dpp:hasID ?actorID ;
        dpp:hasName ?actorName ;
        dpp:hasMail ?actorMail .
    }}
    GROUP BY ?dppID ?timeStampInvalid ?productID ?productName ?actorID ?actorName ?actorMail
        '''
    return query

def make_get_parts_data_query(part_ids):
    """part_ids: List of part IDs to fetch data for"""
    PREFIXES = '''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    '''
    # Construct the FILTER clause
    filter_clause = "FILTER (?part IN (" + ", ".join(f"dpp:{part_id}" for part_id in part_ids) + "))"
    # Construct the full query
    query = f"""{PREFIXES} 
    SELECT ?partID ?partName ?partMass ?partVolume ?partMaterial
    WHERE {{
        ?part a dpp:Part ;
              dpp:hasID ?partID ;
              dpp:hasName ?partName ;
              dpp:hasMass ?partMass ;
              dpp:hasVolume ?partVolume ;
              dpp:hasMaterial ?partMaterial .
        {filter_clause}
    }}"""
    return query


def make_remove_dpp_query(dpp_id):
    """Create a SPARQL query to remove a Digital Product Passport (DPP), its associated product, and parts from the knowledge base."""
    return f'''
    PREFIX dpp: <http://www.semanticweb.org/johanne/ontologies/2025/2/dpp_ontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    # Delete the DPP and its properties
    DELETE {{
        dpp:{dpp_id} ?p ?o .
    }}
    WHERE {{
        dpp:{dpp_id} ?p ?o .
    }} ;

    # Delete any references to the DPP
    DELETE {{
        ?s ?p dpp:{dpp_id} .
    }}
    WHERE {{
        ?s ?p dpp:{dpp_id} .
    }} ;

    # Delete the product described by the DPP and its properties
    DELETE {{
        ?product ?p ?o .
    }}
    WHERE {{
        dpp:{dpp_id} dpp:describes ?product .
        ?product ?p ?o .
    }} ;

    # Delete all parts associated with the product and their properties
    DELETE {{
        ?part ?p ?o .
    }}
    WHERE {{
        dpp:{dpp_id} dpp:describes ?product .
        ?product dpp:consistsOf ?part .
        ?part ?p ?o .
    }} ;

    # Delete any references to the product
    DELETE {{
        ?s ?p ?product .
    }}
    WHERE {{
        dpp:{dpp_id} dpp:describes ?product .
        ?s ?p ?product .
    }} ;

    # Delete any references to the parts
    DELETE {{
        ?s ?p ?part .
    }}
    WHERE {{
        dpp:{dpp_id} dpp:describes ?product .
        ?product dpp:consistsOf ?part .
        ?s ?p ?part .
    }} ;

    # Delete any nested references to parts or products
    DELETE {{
        ?nested_subject ?nested_predicate ?nested_object .
    }}
    WHERE {{
        {{
            dpp:{dpp_id} dpp:describes ?product .
            ?product dpp:consistsOf ?part .
            ?nested_subject ?nested_predicate ?part .
        }}
        UNION
        {{
            dpp:{dpp_id} dpp:describes ?product .
            ?nested_subject ?nested_predicate ?product .
        }}
    }} ;

    # Delete any remaining references to the product or parts by their ID
    DELETE {{
        ?s ?p ?o .
    }}
    WHERE {{
        ?s ?p ?o .
        FILTER(CONTAINS(STR(?s), "{dpp_id}") || CONTAINS(STR(?o), "{dpp_id}"))
    }} ;
    '''
    
def make_remove_product_query(product_id, part_ids):
    """Create a SPARQL query to remove a product and its parts from the knowledge base."""
    
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

def make_remove_actor_query(actor_id):
    """Create a SPARQL query to remove an actor from the knowledge base."""
    
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
