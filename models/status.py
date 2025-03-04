class Status:
    """
    Représente le statut d'une mission pour un joueur.
    """
    def __init__(self, id_status: int, label: str):
        self.id = id_status
        self.label = label

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label
        }