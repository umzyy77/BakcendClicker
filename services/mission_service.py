from models.mission import Mission
from utils.db_connection import get_db_connection
from utils.logger import log_error
from models.difficulty import Difficulty

class MissionService:
    @staticmethod
    def get_mission(mission_id: int):
        """
        Récupère une mission par son ID, avec sa difficulté associée.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT mission.id_mission, mission.name, mission.id_difficulty, mission.reward_money, mission.reward_power, difficulty.label 
                    FROM mission
                    INNER JOIN difficulty ON mission.id_difficulty = difficulty.id_difficulty
                    WHERE mission.id_mission = %s
                """, (mission_id,))
                mission_data = cursor.fetchone()

            if not mission_data:
                return None

            # Création de l'objet Difficulty
            difficulty = Difficulty(id_difficulty=mission_data['id_difficulty'], label=mission_data['label'])

            # Création de l'objet Mission avec l'objet Difficulty
            mission = Mission(
                id_mission=mission_data['id_mission'],
                name=mission_data['name'],
                reward_money=mission_data['reward_money'],
                reward_power=mission_data['reward_power'],
                difficulty=difficulty
            )
            return mission.to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération de la mission {mission_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def get_all_missions():
        """
        Récupère toutes les missions disponibles, avec leur difficulté.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT mission.id_mission, mission.name, mission.id_difficulty, mission.reward_money, mission.reward_power, difficulty.label 
                    FROM mission
                    INNER JOIN difficulty ON mission.id_difficulty = difficulty.id_difficulty
                """)
                missions_data = cursor.fetchall()

            missions = []
            for mission_data in missions_data:
                difficulty = Difficulty(id_difficulty=mission_data['id_difficulty'], label=mission_data['label'])
                mission = Mission(
                    id_mission=mission_data['id_mission'],
                    name=mission_data['name'],
                    reward_money=mission_data['reward_money'],
                    reward_power=mission_data['reward_power'],
                    difficulty=difficulty
                )
                missions.append(mission.to_dict())

            return missions

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
                cursor.execute("""
                    INSERT INTO player_mission (id_player, id_mission, id_status) 
                    VALUES (%s, %s, 2)
                """, (player_id, mission_id))
                connection.commit()

            return {"message": "Mission started"}

        except Exception as e:
            log_error(f"Erreur lors du démarrage de la mission {mission_id} pour le joueur {player_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def complete_mission(player_id: int, mission_id: int):
        """
        Marque une mission comme complétée pour un joueur et attribue les récompenses.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT reward_money, reward_power FROM mission WHERE id_mission = %s
                """, (mission_id,))
                rewards = cursor.fetchone()

                if not rewards:
                    return False

                # Mise à jour des récompenses
                cursor.execute("""
                    UPDATE player 
                    SET money = money + %s, hacking_power = hacking_power + %s 
                    WHERE id_player = %s
                """, (rewards['reward_money'], rewards['reward_power'], player_id))

                # Marque la mission comme complétée
                cursor.execute("""
                    UPDATE player_mission 
                    SET id_status = 3 
                    WHERE id_player = %s AND id_mission = %s
                """, (player_id, mission_id))
                connection.commit()

            return True

        except Exception as e:
            log_error(f"Erreur lors de la complétion de la mission {mission_id} pour le joueur {player_id}: {e}")
            return False

        finally:
            connection.close()
