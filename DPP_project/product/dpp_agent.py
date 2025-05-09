"""
Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from DPP_project.product import kb_client
from DPP_project.product.onshape_codes import onshape_api
from DPP_project.product.digital_product_passport.product_dpp import DPP
from DPP_project.product.actual_product.product import Product
from DPP_project.product.actor.value_chain_actor import ValueChainActor
from DPP_project.product.actual_product.part import Part

DID_chair = "ddd738631676985828abef74"  # Document ID
WID_chair = "76466b78737892550146d811"  # Workspace ID
EID_chair = "789de4812fe20a46c3f3962b"  # Element ID

DID = DID_chair # Document ID
WID = WID_chair # Workspace ID
EID = EID_chair # Element ID

# ---------------- INSTANCES ------------------ #

# Parts
# --------
volume_parts, total_product_volume = onshape_api.get_product_volume(DID, WID, EID)
mass_parts, total_product_mass = onshape_api.get_product_mass(DID, WID, EID)
material_parts, total_product_material = onshape_api.get_product_materials(DID, WID, EID)
product_parts_json = onshape_api.get_product_parts(DID, WID, EID)

product_parts = []
for part in product_parts_json:
    part_id = part["partId"]
    part_name = part["name"]
    part_mass = mass_parts[part_id]
    part_volume = volume_parts[part_id]
    part_material = material_parts[part_id]
    example_part_lifetime = 10.0  # Example lifetime in years

    # Create a Part instance for each part
    product_part = Part(part_id, part_name, example_part_lifetime, part_mass, part_volume, part_material)
    product_parts.append(product_part)

    # print(product_part.__repr__())

# Product
# --------
product_name = onshape_api.get_document_name(DID)    # antar document = product for nå
product_owner = onshape_api.get_document_owner(DID)  # antar document = product for nå, dvs dokument og producteier er det samme

example_product_id = "ID_" + product_name.lower().replace(" ","_")  # Example ID format product
product_chair = Product(example_product_id, product_name, product_parts)
# print(product_chair.__repr__())

# Actor
# -------
example_actor_mail = product_owner.lower().replace(" ","_") + "@example.com"  # Example email format
example_actor_id = "ID_" + product_owner.lower().replace(" ","_")  # Example ID format actor

value_chain_actor_chair = ValueChainActor(example_actor_id, product_owner, example_actor_mail)
# print(value_chain_actor_chair.__repr__()+"\n")

# DPP
# -------
example_dpp_ID = "ID_DPP_" + product_name.lower().replace(" ","_")  # Example ID format DPP
example_dpp_timeStamp = "2030-01-01T00:00:00Z"  # Example timestamp format
product_DPP = DPP(example_dpp_ID, example_dpp_timeStamp, value_chain_actor_chair, product_chair)
# print(product_DPP.__repr__()+"\n")

# Update actor with owned product - must be done after DPP is added to the KB
# value_chain_actor_chair.add_owner_of(product_DPP)
# print(value_chain_actor_chair.__repr__())



# ---------------- INSERT DATA TO KB ------------------ #

# INSERT PRODUCT:
kb_client.update_kb(kb_client.make_insert_product_query(product_chair))  # Insert product into the knowledge base

# INSERT ACTOR (actor is without owner_of):
kb_client.update_kb(kb_client.make_insert_actor_query(value_chain_actor_chair))  # Insert actor into the knowledge base

# INSERT PRODUCT_DPP (and additionally update the actor with owner_of):
kb_client.update_kb(kb_client.make_insert_dpp_query(product_DPP))  # Insert DPP into the knowledge base

# Update actor with owned product. Cant do this before the DPP is inserted in the KB, because it needs to be in the KB to be able to be added to the actor.
value_chain_actor_chair.add_owner_of(product_DPP) #So that the datacase and instances are consistent. 


# ---------------- REMOVE DATA FROM KB ------------------ #
# REMOVE PRODUCT:
kb_client.update_kb(kb_client.make_remove_product_query(product_chair))  # Remove product from the knowledge base

# REMOVE ACTOR:
kb_client.update_kb(kb_client.make_remove_actor_query(value_chain_actor_chair))  # Remove actor from the knowledge base

# REMOVE PRODUCT_DPP:
# kb_client.update_kb(kb_client.make_remove_dpp_query(product_DPP))  # Remove DPP from the knowledge base
