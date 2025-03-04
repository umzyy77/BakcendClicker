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
        Crée un nouveau joueur avec un username donné.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO player (username, hacking_power, money) VALUES (%s, %s, %s)",
                               (username, 1, 0))
                connection.commit()
                new_player_id = cursor.lastrowid

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