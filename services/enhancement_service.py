from models.enhancement import Enhancement
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error


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
        if enhancement_id <= 0:  # ✅ Vérification pour éviter un ID incorrect
            return None

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM enhancement WHERE id_enhancement = %s", (enhancement_id,))
                enhancement_data = cursor.fetchone()

            if enhancement_data:
                log_info(f"Récupération de l'amélioration {enhancement_id} réussie.")
                return Enhancement(
                    id_enhancement=enhancement_data["id_enhancement"],
                    experience_cost=enhancement_data["experience_cost"],
                    boost_value=enhancement_data["boost_value"],
                    id_type=enhancement_data["id_type"]
                ).to_dict()
            else:
                log_error(f"Amélioration {enhancement_id} non trouvée.")
                return None  # ✅ Retourne None proprement si l'amélioration n'existe pas

        except Exception as e:
            log_error(f"Erreur lors de la récupération de l'amélioration {enhancement_id} : {e}")
            return None
        finally:
            connection.close()

