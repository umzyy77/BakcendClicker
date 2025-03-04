class MissionTask:
    """
    Représente une tâche à accomplir pour valider une mission.
    """
    def __init__(self, id_task: int, id_mission: int, task_type: str, task_value: int):
        self.id = id_task
        self.id_mission = id_mission
        self.task_type = task_type
        self.task_value = task_value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_mission": self.id_mission,
            "task_type": self.task_type,
            "task_value": self.task_value
        }