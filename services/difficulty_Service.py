from models.difficulty import Difficulty
from utils.db_connection import get_db_connection
from utils.logger import log_error

class DifficultyService:
    @staticmethod
    def get_all_difficulties():
        """
        Récupère tous les niveaux de difficulté.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM difficulty")
                difficulties_data = cursor.fetchall()

            # Créer des objets Difficulty et les convertir en dictionnaires
            return [Difficulty(**difficulty).to_dict() for difficulty in difficulties_data]

        except Exception as e:
            log_error(f"Erreur lors de la récupération des niveaux de difficulté: {e}")
            return []

        finally:
            connection.close()
