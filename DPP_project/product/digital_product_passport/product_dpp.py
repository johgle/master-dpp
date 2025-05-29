"""
Class for Digital Product Passport (DPP) for products in the DPP ontology.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""
from product.actor.actor import Actor
from product.actual_product.product import Product



class DPP:

    RepairInformation = None  # Placeholder for repair information
    RecyclingInformation = None  # Placeholder for recycling information
    DisassemblyInformation = None  # Placeholder for disassembly information

    def __init__(self, id: str, timeStampInvalid:str, responsibleActor: Actor, describes: Product):
        self.id = id
        self.timeStampInvalid = timeStampInvalid
        self.responsibleActor = responsibleActor
        self.describes = describes

    def __repr__(self):
        return f"DPP(id='{self.id}', timeStampInvalid='{self.timeStampInvalid}', responsibleActor={self.responsibleActor}, describes={self.describes})"
