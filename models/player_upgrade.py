from models.upgrade_level import UpgradeLevel
from models.player import Player

class PlayerUpgrade:
    """
    Associe un joueur à une amélioration achetée.
    """
    def __init__(self,player: Player, upgrade_level: UpgradeLevel):
        self.upgrade_level = upgrade_level
        self.player= player

    def to_dict(self) -> dict:
        return {
            "upgrade_level": self.upgrade_level.to_dict(),
            "player": self.player.to_dict()
        }
