from models.player import Player
from models.mission import Mission
from models.status import Status

class PlayerMission:
    """
    Associe un joueur à une mission et garde son statut et sa progression.
    """
    def __init__(self, player: Player, mission: Mission, status: Status, clicks_done: int):
        self.player = player
        self.mission = mission
        self.status = status
        self.clicks_done = clicks_done

    def to_dict(self) -> dict:
        return {
            "player": self.player.to_dict(),
            "mission": self.mission.to_dict(),
            "status": self.status.to_dict(),
            "clicks_done": self.clicks_done
        }

