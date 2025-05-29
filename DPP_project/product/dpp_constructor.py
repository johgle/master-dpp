"""
Module for creating instances of Product, Part, Actor, and DPP.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from product.onshape_codes import onshape_api
from product.digital_product_passport.product_dpp import DPP
from product.actual_product.product import Product
from product.actor.value_chain_actor import ValueChainActor
from product.actual_product.part import Part

def make_part_instance(DID, WID, EID):
    volume_parts, total_product_volume = onshape_api.get_product_volume(DID, WID, EID)
    mass_parts, total_product_mass = onshape_api.get_product_mass(DID, WID, EID)
    material_parts, total_product_material = onshape_api.get_product_materials(DID, WID, EID)
    product_parts_json = onshape_api.get_product_parts(DID, WID, EID)
    document_name = onshape_api.get_document_name(DID)

    product_parts = []
    for part in product_parts_json:
        part_id = part["partId"]
        part_name = part["name"]
        part_mass = round(mass_parts[part_id], 4)
        part_volume = round(volume_parts[part_id], 4)
        part_material = material_parts[part_id]
        example_part_lifetime = 10.0
        specific_part_id = document_name.lower().replace(" ","_") + "_" + part_id
        product_part = Part(specific_part_id, part_name, example_part_lifetime, part_mass, part_volume, part_material)
        product_parts.append(product_part)
    return product_parts

def make_product_instance(DID, WID, EID):
    product_parts = make_part_instance(DID, WID, EID)
    product_name = onshape_api.get_document_name(DID)
    example_product_id = "ID_" + product_name.lower().replace(" ","_")
    product = Product(example_product_id, product_name, product_parts)
    return product

def make_actor_instance(DID):
    product_owner = onshape_api.get_document_owner(DID)
    example_actor_mail = product_owner.lower().replace(" ","_") + "@example.com"
    example_actor_id = "ID_" + product_owner.lower().replace(" ","_")
    value_chain_actor_chair = ValueChainActor(example_actor_id, product_owner, example_actor_mail)
    return value_chain_actor_chair

def make_instances(DID, WID, EID):
    product = make_product_instance(DID, WID, EID)
    value_chain_actor_chair = make_actor_instance(DID)
    product_name = onshape_api.get_document_name(DID)
    example_dpp_ID = "ID_DPP_" + product_name.lower().replace(" ","_")
    example_dpp_timeStampInvalid = "2030-01-01"
    product_DPP = DPP(example_dpp_ID, example_dpp_timeStampInvalid, value_chain_actor_chair, product)
    return product, value_chain_actor_chair, product_DPP
