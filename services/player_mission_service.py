from models.difficulty import Difficulty
from models.mission import Mission
from models.player import Player
from models.player_mission import PlayerMission
from models.status import Status
from utils.db_connection import get_db_connection
from utils.logger import log_error

class PlayerMissionService:
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
                # On commence la mission, le statut est 'en cours' (id_status = 2)
                cursor.execute("""
                     INSERT INTO player_mission (id_player, id_mission, id_status) 
                     VALUES (%s, %s, 2)
                 """, (player_id, mission_id))  # Mission en cours
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
                # Récupérer les récompenses de la mission
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
                    SET id_status = 3  # statut 'complété'
                    WHERE id_player = %s AND id_mission = %s
                """, (player_id, mission_id))
                connection.commit()

            return True

        except Exception as e:
            log_error(f"Erreur lors de la complétion de la mission {mission_id} pour le joueur {player_id}: {e}")
            return False

        finally:
            connection.close()

    @staticmethod
    def get_player_missions(player_id: int):
        """
        Récupère toutes les missions d'un joueur (en cours, échouées ou complétées).
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT player_mission.id_player, player_mission.id_mission, player_mission.id_status, mission.name, status.label AS status_label 
                    FROM player_mission
                    INNER JOIN mission ON player_mission.id_mission = mission.id_mission
                    INNER JOIN status ON player_mission.id_status = status.id_status
                    WHERE player_mission.id_player = %s
                """, (player_id,))
                player_missions = cursor.fetchall()

            missions = []
            for mission_data in player_missions:
                # Créer un objet Mission avec la difficulté liée
                mission = Mission(
                    id_mission=mission_data['id_mission'],
                    name=mission_data['name'],
                    reward_money=mission_data['reward_money'],
                    reward_power=mission_data['reward_power'],
                    difficulty=Difficulty(id_difficulty=mission_data['id_difficulty'], label=mission_data['difficulty_label'])
                )
                status = Status(id_status=mission_data['id_status'], label=mission_data['status_label'])
                player_mission = PlayerMission(
                    player=Player(id_player=mission_data['id_player'], username=''),  # Ajouter l'objet Player avec ses informations
                    mission=mission,
                    status=status
                )
                missions.append(player_mission.to_dict())

            return missions

        except Exception as e:
            log_error(f"Erreur lors de la récupération des missions du joueur {player_id}: {e}")
            return []

        finally:
            connection.close()

    @staticmethod
    def get_player_mission(player_id: int, mission_id: int):
        """
        Récupère une mission spécifique d'un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT player_mission.id_player, player_mission.id_mission, player_mission.id_status, 
                        mission.name, mission.reward_money, mission.reward_power, difficulty.label AS difficulty_label, 
                        status.label AS status_label
                    FROM player_mission
                    INNER JOIN mission ON player_mission.id_mission = mission.id_mission
                    INNER JOIN difficulty ON mission.id_difficulty = difficulty.id_difficulty
                    INNER JOIN status ON player_mission.id_status = status.id_status
                    WHERE player_mission.id_player = %s AND player_mission.id_mission = %s
                """, (player_id, mission_id))
                mission_data = cursor.fetchone()

            if not mission_data:
                return None

            # Création de l'objet Mission et Status avec la difficulté liée
            mission = Mission(
                id_mission=mission_data['id_mission'],
                name=mission_data['name'],
                reward_money=mission_data['reward_money'],
                reward_power=mission_data['reward_power'],
                difficulty=Difficulty(id_difficulty=mission_data['id_difficulty'], label=mission_data['difficulty_label'])  # Difficulté associée
            )
            status = Status(id_status=mission_data['id_status'], label=mission_data['status_label'])

            player_mission = PlayerMission(
                player=Player(id_player=mission_data['id_player'], username=''),  # Ajout du joueur
                mission=mission,
                status=status
            )

            return player_mission.to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération de la mission {mission_id} pour le joueur {player_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def assign_mission_to_player(player_id: int, mission_id: int, status_id: int = 1):
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
                    VALUES (%s, %s, %s)
                """, (player_id, mission_id, status_id))
                connection.commit()

            return {"status": "success", "message": "Mission assigned successfully"}

        except Exception as e:
            log_error(f"Erreur lors de l'assignation de la mission {mission_id} au joueur {player_id}: {e}")
            return {"status": "error", "message": "Failed to assign mission"}

        finally:
            connection.close()

    @staticmethod
    def get_player_in_progress_missions(player_id: int):
        """
        Récupère toutes les missions en cours d'un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                       SELECT mission.id_mission, mission.name, mission.id_difficulty, mission.reward_money, mission.reward_power, difficulty.label 
                       FROM mission
                       INNER JOIN player_mission ON mission.id_mission = player_mission.id_mission
                       INNER JOIN difficulty ON mission.id_difficulty = difficulty.id_difficulty
                       WHERE player_mission.id_player = %s AND player_mission.id_status = 2
                   """, (player_id,))
                missions_data = cursor.fetchall()

            missions = []
            for mission_data in missions_data:
                # Créer l'objet Difficulty avec les données récupérées
                difficulty = Difficulty(id_difficulty=mission_data['id_difficulty'], label=mission_data['label'])

                # Créer l'objet Mission en incluant l'objet Difficulty
                mission = Mission(
                    id_mission=mission_data['id_mission'],
                    name=mission_data['name'],
                    reward_money=mission_data['reward_money'],
                    reward_power=mission_data['reward_power'],
                    difficulty=difficulty  # Lier l'objet Difficulty ici
                )
                # Ajouter la mission à la liste
                missions.append(mission.to_dict())

            return missions

        except Exception as e:
            log_error(f"Erreur lors de la récupération des missions en cours du joueur {player_id}: {e}")
            return []

        finally:
            connection.close()