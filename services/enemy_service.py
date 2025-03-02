from models.enemy import Enemy
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error

class EnemyService:
    @staticmethod
    def get_all_enemies():
        """
        Récupère tous les ennemis depuis la base de données.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM enemy")
                enemies_data = cursor.fetchall()
            log_info("Récupération de tous les ennemis réussie.")
            return [Enemy(**data).to_dict() for data in enemies_data]
        except Exception as e:
            log_error(f"Erreur lors de la récupération des ennemis : {e}")
            return []
        finally:
            connection.close()

    @staticmethod
    def get_enemy(level: int):
        """
        Récupère un ennemi spécifique par son niveau.
        """
        if level <= 0:
            return None

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM enemy WHERE level = %s", (level,))
                enemy_data = cursor.fetchone()
            if enemy_data:
                log_info(f"Récupération de l'ennemi de niveau {level} réussie.")
                return Enemy(**enemy_data).to_dict()
            else:
                log_error(f"Ennemi de niveau {level} non trouvé.")
                return None
        except Exception as e:
            log_error(f"Erreur lors de la récupération de l'ennemi {level} : {e}")
            return None
        finally:
            connection.close()
