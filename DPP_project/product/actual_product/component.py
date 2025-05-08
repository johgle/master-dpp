"""
Abstract Component class in the DPP ontology.
This class serves as a base for all components in the DPP ontology, including parts, features assemblies.


Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""


from abc import ABC

class Component(ABC):
    def __init__(self, id: str, name: str, lifetime: float, mass: float, volume: float):
        self.id = id
        self.name = name
        self.lifetime = lifetime
        self.mass = mass
        self.volume = volume

    def __repr__(self):
        return (f"Component(id='{self.id}', name='{self.name}', "
                f"lifetime={self.lifetime}, mass={self.mass}, volume={self.volume})")
