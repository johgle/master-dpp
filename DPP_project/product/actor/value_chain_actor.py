"""
Class for Actor of type ValueChainActor in the DPP ontology.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

from DPP_project.product.actor.actor import Actor
from DPP_project.product.digital_product_passport.product_dpp import DPP


class ValueChainActor(Actor):
    def __init__(self, id: str, name: str, mail: str):
        super().__init__(id, name, mail)
        self.owner_of = []  # VCA har ingen DPP den eier fra oppretting,
                            # dette blir lagt til senere (for å unngå sirkulær avhengighet)

    def get_role(self) -> str:
        return "ValueChainActor"
    
    def set_owner_of(self, owner_of: list[DPP]):
        self.owner_of = owner_of

    def add_owner_of(self, dpp: DPP):
        self.owner_of.append(dpp)