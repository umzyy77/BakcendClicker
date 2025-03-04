class Mission:
    """
    Représente une mission de piratage.
    """
    def __init__(self, id_mission: int, name: str, id_difficulty: int, reward_money: int, reward_power: int):
        self.id = id_mission
        self.name = name
        self.id_difficulty = id_difficulty
        self.reward_money = reward_money
        self.reward_power = reward_power

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "id_difficulty": self.id_difficulty,
            "reward_money": self.reward_money,
            "reward_power": self.reward_power
        }