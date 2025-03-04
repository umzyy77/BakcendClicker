class PlayerMission:
    """
    Associe un joueur à une mission et garde son statut.
    """
    def __init__(self, id_player: int, id_mission: int, id_status: int):
        self.id_player = id_player
        self.id_mission = id_mission
        self.id_status = id_status

    def to_dict(self) -> dict:
        return {
            "id_player": self.id_player,
            "id_mission": self.id_mission,
            "id_status": self.id_status
        }