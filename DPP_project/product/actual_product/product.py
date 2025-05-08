"""
Product class for instances of products in the DPP ontology.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

class Product:
    def __init__(self, id: str, name: str, parts: list):
        self.id = id
        self.name = name
        self.parts = parts

    def __repr__(self):
        return f"Product(id='{self.id}', name='{self.name} ', parts={self.parts})"