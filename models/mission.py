from models.difficulty import Difficulty

class Mission:
    """
    Représente une mission de piratage.
    """
    def __init__(self, id_mission: int, name: str, reward_money: int, reward_power: int, difficulty: Difficulty):
        self.id = id_mission
        self.name = name
        self.difficulty = difficulty
        self.reward_money = reward_money
        self.reward_power = reward_power

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "reward_money": self.reward_money,
            "reward_power": self.reward_power,
            "difficulty": self.difficulty.to_dict()
        }
