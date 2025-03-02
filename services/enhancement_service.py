from models.enhancement import Enhancement
from utils.db_connection import get_db_connection

class EnhancementService:
    @staticmethod
    def get_all_enhancements():
        """
        Récupère toutes les améliorations disponibles.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM enhancement")
            enhancements_data = cursor.fetchall()

        # Passer les valeurs explicitement pour éviter les erreurs
        return [
            Enhancement(
                id_enhancement=data["id_enhancement"],
                experience_cost=data["experience_cost"],
                boost_value=data["boost_value"],
                id_type=data["id_type"]
            ).to_dict()
            for data in enhancements_data
        ]

    @staticmethod
    def get_enhancement(enhancement_id: int):
        """
        Récupère une amélioration spécifique.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM enhancement WHERE id_enhancement = %s", (enhancement_id,))
            enhancement_data = cursor.fetchone()

        if enhancement_data:
            return Enhancement(
                id_enhancement=enhancement_data["id_enhancement"],
                experience_cost=enhancement_data["experience_cost"],
                boost_value=enhancement_data["boost_value"],
                id_type=enhancement_data["id_type"]
            ).to_dict()
        return None
