import pymysql


from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error



class PlayerService:
    """
    Service gérant les opérations sur les joueurs.
    """

    @staticmethod
    def create_player(username: str):
        """
        Crée un nouveau joueur avec un nom d'utilisateur donné.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO player (username, hacking_power, money) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, 1, 0))
                connection.commit()
                player_id = cursor.lastrowid

            # Assigner les missions par défaut
            from services.player_mission_service import PlayerMissionService
            PlayerMissionService.assign_default_missions(player_id)
            return player_id
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la création du joueur : {e}")
            return None
        finally:
            connection.close()

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
                sql = "SELECT * FROM player WHERE id_player = %s"
                cursor.execute(sql, (player_id,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération du joueur : {e}")
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
                sql = "DELETE FROM player WHERE id_player = %s"
                cursor.execute(sql, (player_id,))
                connection.commit()
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la suppression du joueur : {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def update_player_money(player_id: int, amount: int) -> bool:
        """
        Met à jour l'argent du joueur.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE player SET money = money + %s WHERE id_player = %s"
                cursor.execute(sql, (amount, player_id))
                connection.commit()
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la mise à jour de l'argent du joueur : {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def update_hacking_power(player_id: int, power: int) -> bool:
        """
        Met à jour la puissance de hacking du joueur.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE player SET hacking_power = hacking_power + %s WHERE id_player = %s"
                cursor.execute(sql, (power, player_id))
                connection.commit()
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la mise à jour de la puissance de hacking du joueur : {e}")
            return False
        finally:
            connection.close()
