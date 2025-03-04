from models.player import Player
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error

class PlayerService:
    @staticmethod
    def get_player(player_id: int):
        """
        Récupère un joueur par son ID.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM player WHERE id_player = %s", (player_id,))
                player_data = cursor.fetchone()

            if not player_data:
                return None

            return Player(**player_data).to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération du joueur {player_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def create_player(username: str):
        """
        Crée un nouveau joueur avec un nom d'utilisateur donné, assigne les missions et améliorations par défaut.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                # Création du joueur
                cursor.execute("INSERT INTO player (username, hacking_power, money) VALUES (%s, 1, 0)", (username,))
                connection.commit()
                new_player_id = cursor.lastrowid

                # Assignation des missions verrouillées au joueur (missions faciles)
                cursor.execute(
                    "SELECT id_mission FROM mission WHERE id_difficulty = 1")  # Missions verrouillées (Facile)
                locked_missions = cursor.fetchall()
                for mission in locked_missions:
                    cursor.execute("""
                        INSERT INTO player_mission (id_player, id_mission, id_status) 
                        VALUES (%s, %s, 1)  # 'unlocked'
                    """, (new_player_id, mission['id_mission']))
                connection.commit()

            # Retourner le joueur créé
            return PlayerService.get_player(new_player_id)

        except Exception as e:
            log_error(f"Erreur lors de la création du joueur {username}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def increment_hacking_power(player_id: int):
        """
        Augmente la puissance de hacking d'un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE player SET hacking_power = hacking_power + 1 WHERE id_player = %s", (player_id,))
                connection.commit()

            return PlayerService.get_player(player_id)

        except Exception as e:
            log_error(f"Erreur lors de l'incrémentation de la puissance de hacking du joueur {player_id}: {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def delete_player(player_id: int) -> bool:
        """
        Supprime un joueur par son ID.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM player WHERE id_player = %s", (player_id,))
                connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            log_error(f"Erreur lors de la suppression du joueur {player_id}: {e}")
            return False

        finally:
            connection.close()

    @staticmethod
    def get_player_stats(player_id: int):
        """
        Récupère les statistiques globales d'un joueur :
        - Missions complétées
        - Améliorations achetées
        - Montant d'argent
        - Puissance de hacking
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                # Récupérer le nombre de missions complétées
                cursor.execute("""
                       SELECT COUNT(*) 
                       FROM player_mission 
                       WHERE id_player = %s AND id_status = (SELECT id_status FROM status WHERE label = 'completed')
                   """, (player_id,))
                missions_completed = cursor.fetchone()[0]

                # Récupérer le nombre d'améliorations achetées
                cursor.execute("""
                       SELECT COUNT(*) 
                       FROM player_upgrade 
                       WHERE id_player = %s
                   """, (player_id,))
                upgrades_owned = cursor.fetchone()[0]

                # Récupérer l'argent total du joueur
                cursor.execute("""
                       SELECT money 
                       FROM player 
                       WHERE id_player = %s
                   """, (player_id,))
                money = cursor.fetchone()[0]

                # Récupérer la puissance de hacking du joueur
                cursor.execute("""
                       SELECT hacking_power 
                       FROM player 
                       WHERE id_player = %s
                   """, (player_id,))
                hacking_power = cursor.fetchone()[0]

            return {
                "missions_completed": missions_completed,
                "upgrades_owned": upgrades_owned,
                "money": money,
                "hacking_power": hacking_power
            }

        except Exception as e:
            log_error(f"Erreur lors de la récupération des statistiques du joueur {player_id}: {e}")
            return None

        finally:
            connection.close()