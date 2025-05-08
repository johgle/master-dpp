"""
Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from DPP_project.product import kb_client as KBClient
from DPP_project.product.onshape_codes import onshape_api
from DPP_project.product.digital_product_passport.product_dpp import DPP
from DPP_project.product.actual_product.product import Product
from DPP_project.product.actor.value_chain_actor import ValueChainActor
from DPP_project.product.actual_product.part import Part


# bruke klassen til:
# å hente data fra onshapeAPI
# lagre data i instanser av product, parts osv
# lagre det i instans av DPP
# lagre DPP i knowledge base.

DID_chair = "ddd738631676985828abef74"  # Document ID
WID_chair = "76466b78737892550146d811"  # Workspace ID
EID_chair = "789de4812fe20a46c3f3962b"  # Element ID

DID = DID_chair # Document ID
WID = WID_chair # Workspace ID
EID = EID_chair # Element ID

# ---------------- INSTANCES ------------------ #

# Parts
# --------

#DATA:
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

#Update actor with owned product
value_chain_actor_chair.owner_of.append(product_DPP)
# print(value_chain_actor_chair.__repr__())