class Difficulty:
    """
    Représente un niveau de difficulté de mission.
    """
    def __init__(self, id_difficulty: int, label: str):
        self.id = id_difficulty
        self.label = label

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label
        }
