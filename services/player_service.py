from models.player import Player
from services.enhancement_service import EnhancementService
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error

class PlayerService:
    @staticmethod
    def get_player(player_id: int):
        """
        Récupère un joueur par son ID.
        """
        if player_id <= 0:
            return None

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM player WHERE id_player = %s", (player_id,))
                player_data = cursor.fetchone()

            if player_data:
                log_info(f"Joueur {player_id} trouvé.")
                return Player(**player_data).to_dict()
            else:
                log_error(f"Joueur {player_id} non trouvé.")
                return None
        except Exception as e:
            log_error(f"Erreur lors de la récupération du joueur {player_id} : {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def delete_player(player_id: int) -> bool:
        """
        Supprime un joueur par son ID.
        """
        if player_id <= 0:
            return False

        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM player WHERE id_player = %s", (player_id,))
                connection.commit()
                deleted = cursor.rowcount > 0
            if deleted:
                log_info(f"Joueur {player_id} supprimé avec succès.")
            else:
                log_error(f"Échec de suppression : joueur {player_id} introuvable.")
            return deleted
        except Exception as e:
            log_error(f"Erreur lors de la suppression du joueur {player_id} : {e}")
            return False
        finally:
            connection.close()
