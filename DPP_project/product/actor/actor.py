from abc import ABC, abstractmethod

class Actor(ABC):
    def __init__(self, id: str, name: str, mail: str):
        self.id = id
        self.name = name
        self.mail = mail

    def __repr__(self):
        return f"Actor(id='{self.id}', name='{self.name}', mail='{self.mail}', owner_of={self.owner_of})"

    @abstractmethod
    def get_role(self) -> str:
        """Subklasser må implementere hvilken type rolle aktøren har."""
        pass

