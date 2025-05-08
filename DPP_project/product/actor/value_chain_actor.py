"""
Class for Actor of type ValueChainActor in the DPP ontology.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from DPP_project.product.actor.actor import Actor


class ValueChainActor(Actor):
    def __init__(self, id: str, name: str, mail: str, owner_of: list[str] = None):
        super().__init__(id, name, mail, owner_of)

    def get_role(self) -> str:
        return "ValueChainActor"
    
    def set_owner_of(self, owner_of: list[str]):
        self.owner_of = owner_of
