from models.mission_task import MissionTask
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error
class MissionTaskService:
    @staticmethod
    def get_tasks_by_mission(mission_id: int):
        """
        Récupère toutes les tâches associées à une mission.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM mission_task WHERE id_mission = %s", (mission_id,))
                tasks = cursor.fetchall()

            return [MissionTask(**task).to_dict() for task in tasks]

        except Exception as e:
            log_error(f"Erreur lors de la récupération des tâches de la mission {mission_id}: {e}")
            return []

        finally:
            connection.close()

    @staticmethod
    def check_task_completion(player_id: int, mission_id: int, task_type: str, progress_value: int):
        """
        Vérifie si une tâche est complétée par un joueur.
        """
        tasks = MissionTaskService.get_tasks_by_mission(mission_id)
        for task in tasks:
            if task['task_type'] == task_type and progress_value >= task['task_value']:
                return True
        return False