class Enemy:
    """
    Représente un ennemi dans le jeu.
    """

    def __init__(self, level: int, name: str, total_life: int):
        self.level = level
        self.name = name
        self.total_life = total_life
        self.current_life = total_life  # La vie actuelle de l'ennemi

    def take_damage(self, damage: int):
        """
        Réduit la vie de l'ennemi lorsqu'il prend des dégâts.
        """
        self.current_life = max(0, self.current_life - damage)

    def is_defeated(self) -> bool:
        """
        Vérifie si l'ennemi est vaincu (0 HP).
        """
        return self.current_life == 0

    def to_dict(self) -> dict:
        """
        Convertit l'ennemi en dictionnaire JSON.
        """
        return {
            "level": self.level,
            "name": self.name,
            "total_life": self.total_life,
            "current_life": self.current_life
        }
