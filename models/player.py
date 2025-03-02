class Player:
    """
    Représente un joueur dans le jeu.
    """

    def __init__(self, id_player: int, pseudo: str, total_experience: int, id_enemy: int):
        self.id = id_player
        self.pseudo = pseudo
        self.total_experience = total_experience
        self.id_enemy = id_enemy
        self.click_damage = 1  # Par défaut, le joueur inflige 1 dégât par clic

    def gain_experience(self, amount: int):
        """
        Ajoute de l'expérience au joueur.
        """
        self.total_experience += amount

    def increase_damage(self, bonus: int):
        """
        Augmente les dégâts infligés par le joueur.
        """
        self.click_damage += bonus

    def to_dict(self) -> dict:
        """
        Convertit le joueur en dictionnaire JSON.
        """
        return {
            "id": self.id,
            "pseudo": self.pseudo,
            "total_experience": self.total_experience,
            "id_enemy": self.id_enemy,
            "click_damage": self.click_damage
        }
