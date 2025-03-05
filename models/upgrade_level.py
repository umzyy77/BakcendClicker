from models.upgrade import Upgrade  # Importation de la classe Upgrade

class UpgradeLevel:
    """
    Représente un niveau spécifique d'une amélioration.
    """
    def __init__(self, id_level: int, level: int, cost: int, boost_value: int, upgrade: Upgrade):
        self.id = id_level
        self.upgrade = upgrade
        self.level = level
        self.cost = cost
        self.boost_value = boost_value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "upgrade": self.upgrade.to_dict(),
            "level": self.level,
            "cost": self.cost,
            "boost_value": self.boost_value
        }
