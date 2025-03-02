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

            if not enemies_data:  # ✅ Vérifie si la liste est vide
                log_info("Aucun ennemi trouvé dans la base de données.")
                return []

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
            return None  # ✅ Empêche d'aller plus loin avec un ID invalide

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM enemy WHERE level = %s", (level,))
                enemy_data = cursor.fetchone()

            if not enemy_data:  # ✅ Vérifie si l'ennemi existe
                log_error(f"Ennemi de niveau {level} non trouvé.")
                return None  # ✅ Retourne None proprement

            log_info(f"Récupération de l'ennemi de niveau {level} réussie.")
            return Enemy(**enemy_data).to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération de l'ennemi {level} : {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def delete_enemy(level: int) -> bool:
        """
        Supprime un ennemi par son niveau.
        Retourne True si l'ennemi a été supprimé, False sinon.
        """
        if level <= 0:
            return False  # ✅ Évite les niveaux invalides

        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM enemy WHERE level = %s", (level,))
                connection.commit()
                deleted = cursor.rowcount > 0  # Vérifie si une ligne a été supprimée

            if deleted:
                log_info(f"Ennemi niveau {level} supprimé avec succès.")
            else:
                log_error(f"Échec de suppression : ennemi {level} introuvable.")

            return deleted

        except Exception as e:
            log_error(f"Erreur lors de la suppression de l'ennemi {level} : {e}")
            return False

        finally:
            connection.close()

