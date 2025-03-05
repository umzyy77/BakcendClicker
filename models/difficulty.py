class Difficulty:
    """
    Représente un niveau de difficulté de mission.
    """
    def __init__(self, id_difficulty: int, label: str, clicks_required: int):
        self.id = id_difficulty
        self.label = label
        self.clicks_required = clicks_required

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "clicks_required": self.clicks_required
        }
