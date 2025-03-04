from models.mission import Mission
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error

class MissionService:
    @staticmethod
    def get_mission(mission_id: int):
        """
        Récupère une mission par son ID.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM mission WHERE id_mission = %s", (mission_id,))
                mission_data = cursor.fetchone()

            if not mission_data:
                return None

            return Mission(**mission_data).to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération de la mission {mission_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def get_all_missions():
        """
        Récupère toutes les missions disponibles.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM mission")
                missions_data = cursor.fetchall()

            return [Mission(**mission).to_dict() for mission in missions_data]

        except Exception as e:
            log_error(f"Erreur lors de la récupération des missions: {e}")
            return []

        finally:
            connection.close()

    @staticmethod
    def start_mission(player_id: int, mission_id: int):
        """
        Assigne une mission à un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO player_mission (id_player, id_mission, id_status) VALUES (%s, %s, 2)", (player_id, mission_id))
                connection.commit()

            return {"message": "Mission started"}

        except Exception as e:
            log_error(f"Erreur lors du démarrage de la mission {mission_id} pour le joueur {player_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def get_player_missions(player_id: int):
        """
        Récupère les missions en cours et terminées d'un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM player_mission WHERE id_player = %s", (player_id,))
                player_missions = cursor.fetchall()

            return player_missions

        except Exception as e:
            log_error(f"Erreur lors de la récupération des missions du joueur {player_id}: {e}")
            return []

        finally:
            connection.close()
