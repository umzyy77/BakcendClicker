class UpgradeLevel:
    """
    Représente un niveau spécifique d'une amélioration.
    """
    def __init__(self, id_level: int, id_upgrade: int, level: int, cost: int, boost_value: int):
        self.id = id_level
        self.id_upgrade = id_upgrade
        self.level = level
        self.cost = cost
        self.boost_value = boost_value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_upgrade": self.id_upgrade,
            "level": self.level,
            "cost": self.cost,
            "boost_value": self.boost_value
        }