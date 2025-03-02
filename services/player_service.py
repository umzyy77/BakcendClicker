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
            return None  # ✅ Empêche d'aller plus loin avec un ID invalide

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM player WHERE id_player = %s", (player_id,))
                player_data = cursor.fetchone()

            if not player_data:  # ✅ Vérifie si le joueur existe
                log_error(f"Joueur {player_id} non trouvé.")
                return None  # ✅ Retourne None proprement

            log_info(f"Joueur {player_id} trouvé.")
            return Player(
                id_player=player_data["id_player"],
                pseudo=player_data["pseudo"],
                total_experience=player_data["total_experience"],
                id_enemy=player_data["id_enemy"]
            ).to_dict()

        except Exception as e:
            log_error(f"Erreur lors de la récupération du joueur {player_id} : {e}")
            return None  # ✅ Retourne None même en cas d'erreur

        finally:
            connection.close()

    @staticmethod
    def increment_clicks(player_id: int):
        """
        Incrémente l'expérience du joueur à chaque clic.
        """
        player = PlayerService.get_player(player_id)

        if not player:  # ✅ Vérifie si le joueur existe
            log_error(f"Joueur {player_id} introuvable pour un clic.")
            return None  # ✅ Retourne None proprement au lieu de provoquer une erreur 500

        player["total_experience"] += 10  # ✅ Chaque clic donne 10 XP

        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE player SET total_experience = %s WHERE id_player = %s",
                    (player["total_experience"], player_id)
                )
                connection.commit()

            log_info(f"XP mis à jour pour le joueur {player_id}. Nouveau XP : {player['total_experience']}")
            return {"total_experience": player["total_experience"]}  # ✅ Retourne les données correctement

        except Exception as e:
            log_error(f"Erreur lors de l'incrémentation du clic pour le joueur {player_id} : {e}")
            return None

        finally:
            connection.close()

    @staticmethod
    def buy_enhancement(player_id: int, enhancement_id: int):
        """
        Permet à un joueur d'acheter une amélioration.
        """
        player = PlayerService.get_player(player_id)
        enhancement = EnhancementService.get_enhancement(enhancement_id)

        if not player:  # ✅ Vérifie si le joueur existe AVANT toute autre action
            log_error(f"Joueur {player_id} introuvable pour un achat.")
            return None  # ✅ Retourne None pour signaler une erreur 404

        if not enhancement:  # ✅ Vérifie si l'amélioration existe
            log_error(f"Amélioration {enhancement_id} introuvable.")
            return None  # ✅ Retourne None si l'amélioration n'existe pas

        if player["total_experience"] < enhancement["experience_cost"]:  # ✅ Vérifie si le joueur a assez d'XP
            log_error(f"Joueur {player_id} n'a pas assez d'expérience pour acheter l'amélioration {enhancement_id}.")
            return {"error": "Not enough experience to buy this enhancement"}  # ✅ Retourne une erreur proprement

        # ✅ Déduction du coût et mise à jour de l'XP
        player["total_experience"] -= enhancement["experience_cost"]

        connection = get_db_connection()
        if not connection:
            return {"error": "Database connection error"}

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE player SET total_experience = %s WHERE id_player = %s",
                    (player["total_experience"], player_id)
                )
                cursor.execute(
                    "INSERT INTO buy (id_player, id_enhancement) VALUES (%s, %s)",
                    (player_id, enhancement_id)
                )
                connection.commit()

            log_info(
                f"Joueur {player_id} a acheté l'amélioration {enhancement_id}. XP restant : {player['total_experience']}")

            return {"message": "Enhancement purchased successfully"}

        except Exception as e:
            log_error(f"Erreur lors de l'achat de l'amélioration {enhancement_id} par le joueur {player_id} : {e}")
            return {"error": "Internal Server Error"}

        finally:
            connection.close()

    @staticmethod
    def delete_player(player_id: int) -> bool:
        """
        Supprime un joueur par son ID.
        Retourne True si le joueur a été supprimé, False sinon.
        """
        if player_id <= 0:
            return False  # ✅ Empêche la suppression avec un ID négatif

        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM player WHERE id_player = %s", (player_id,))
                connection.commit()
                deleted = cursor.rowcount > 0  # ✅ Vérifie si une ligne a été supprimée

            if deleted:
                log_info(f"Joueur {player_id} supprimé avec succès.")
            else:
                log_error(f"Échec de suppression : joueur {player_id} introuvable.")

            return deleted

        except Exception as e:
            log_error(f"Erreur lors de la suppression du joueur {player_id} : {e}")
            return False  # ✅ Retourne False en cas d'erreur

        finally:
            connection.close()

