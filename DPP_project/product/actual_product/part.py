"""
Part class for instances of parts in the DPP ontology.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from product.actual_product.component import Component

class Part(Component):
    def __init__(self, id: str, name: str, lifetime: float, mass: float, volume: float, material: str):
        super().__init__(id, name, lifetime, mass, volume)
        self.material = material
        # print("sucsess, part created")

    def __repr__(self):
        return (f"Part(id='{self.id}', name='{self.name}', lifetime={self.lifetime}, "
                f"mass={self.mass}, volume={self.volume}, material='{self.material}')")
