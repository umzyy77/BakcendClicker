class Upgrade:
    """
    Représente une amélioration achetable dans le jeu.
    """
    def __init__(self, id_upgrade: int, name: str):
        self.id = id_upgrade
        self.name = name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

