class Player:
    """
    Représente un joueur dans le jeu.
    """
    def __init__(self, id_player: int, username: str, hacking_power: int, money: int):
        self.id = id_player
        self.username = username
        self.hacking_power = hacking_power
        self.money = money

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "hacking_power": self.hacking_power,
            "money": self.money
        }
