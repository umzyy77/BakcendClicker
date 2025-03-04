class PlayerUpgrade:
    """
    Associe un joueur à une amélioration achetée.
    """
    def __init__(self, id_player: int, id_level: int):
        self.id_player = id_player
        self.id_level = id_level

    def to_dict(self) -> dict:
        return {
            "id_player": self.id_player,
            "id_level": self.id_level
        }