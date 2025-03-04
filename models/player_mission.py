from models.player import Player
from models.mission import Mission
from models.status import Status

class PlayerMission:
    """
    Associe un joueur à une mission et garde son statut.
    """
    def __init__(self, player : Player, mission: Mission, status: Status):
        self.player = player
        self.mission = mission
        self.status = status

    def to_dict(self) -> dict:
        return {
            "player": self.player.to_dict(),
            "mission": self.mission.to_dict(),
            "status": self.status.to_dict()  # Sérialisation de l'objet Status
        }

