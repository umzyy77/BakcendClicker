from models.enemy import Enemy
from utils.db_connection import get_db_connection

class EnemyService:
    @staticmethod
    def get_all_enemies():
        """
        Récupère tous les ennemis depuis la base de données.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM enemy")
            enemies_data = cursor.fetchall()
        return [Enemy(**data).to_dict() for data in enemies_data]


    @staticmethod
    def get_enemy(level: int):
        """
        Récupère un ennemi spécifique par son niveau.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM enemy WHERE level = %s", (level,))
            enemy_data = cursor.fetchone()
        return Enemy(**enemy_data).to_dict() if enemy_data else None
