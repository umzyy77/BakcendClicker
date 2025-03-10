import pymysql
from utils.db_connection import get_db_connection
from utils.logger import log_error


class MissionService:
    """
    Service gérant les opérations sur les missions.
    """

    @staticmethod
    def get_all_difficulties():
        """
        Récupère toutes les difficultés disponibles.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM difficulty"
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération des difficultés : {e}")
            return []
        finally:
            connection.close()

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
                sql = "SELECT * FROM mission WHERE id_mission = %s"
                cursor.execute(sql, (mission_id,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération de la mission : {e}")
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
                sql = "SELECT * FROM mission"
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération des missions : {e}")
            return []
        finally:
            connection.close()

    @staticmethod
    def get_mission_objective(mission_id: int):
        """
        Récupère l'objectif d'une mission spécifique.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                sql = "SELECT d.clicks_required FROM mission m JOIN difficulty d ON m.id_difficulty = d.id_difficulty WHERE m.id_mission = %s"
                cursor.execute(sql, (mission_id,))
                result = cursor.fetchone()
                return result["clicks_required"] if result else None
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération de l'objectif de la mission : {e}")
            return None
        finally:
            connection.close()

