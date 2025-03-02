class Enhancement:
    """
    Représente une amélioration achetable par le joueur.
    """

    def __init__(self, id_enhancement: int, experience_cost: int, boost_value: int, id_type: int):
        self.id = id_enhancement
        self.experience_cost = experience_cost
        self.boost_value = boost_value
        self.id_type = id_type  # Stocke l'ID du type d'amélioration (dps ou exp)

    def to_dict(self) -> dict:
        """
        Convertit l'amélioration en dictionnaire JSON.
        """
        return {
            "id": self.id,
            "experience_cost": self.experience_cost,
            "boost_value": self.boost_value,
            "id_type": self.id_type  # Envoi l'ID du type d'amélioration
        }
