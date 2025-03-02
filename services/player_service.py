from models.player import Player
from services.enhancement_service import EnhancementService
from utils.db_connection import get_db_connection

class PlayerService:

    @staticmethod
    def create_player(pseudo: str, id_enemy: int):
        """
        Insère un nouveau joueur dans la base de données et retourne ses infos.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO player (pseudo, total_experience, id_enemy) VALUES (%s, %s, %s)",
                (pseudo, 0, id_enemy)  # 0 XP au départ
            )
            connection.commit()
            new_id = cursor.lastrowid  # Récupère l'ID du joueur inséré

            # Récupérer le joueur ajouté pour le retourner
            cursor.execute("SELECT * FROM player WHERE id_player = %s", (new_id,))
            player_data = cursor.fetchone()

        return Player(
            id_player=player_data["id_player"],
            pseudo=player_data["pseudo"],
            total_experience=player_data["total_experience"],
            id_enemy=player_data["id_enemy"]
        ).to_dict()


    @staticmethod
    def get_player(player_id: int):
        """
        Récupère un joueur par son ID.
        """
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM player WHERE id_player = %s", (player_id,))
            player_data = cursor.fetchone()

        if player_data:
            return Player(
                id_player=player_data["id_player"],
                pseudo=player_data["pseudo"],
                total_experience=player_data["total_experience"],
                id_enemy=player_data["id_enemy"]
            ).to_dict()
        return None

    @staticmethod
    def increment_clicks(player_id: int):
        """
        Incrémente l'expérience du joueur à chaque clic.
        """
        player = PlayerService.get_player(player_id)
        if not player:
            return None

        player["total_experience"] += 10  # Chaque clic donne 10 XP

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE player SET total_experience = %s WHERE id_player = %s",
                (player["total_experience"], player_id)
            )
            connection.commit()

        return player

    @staticmethod
    def buy_enhancement(player_id: int, enhancement_id: int):
        """
        Permet à un joueur d'acheter une amélioration.
        """
        player = PlayerService.get_player(player_id)
        enhancement = EnhancementService.get_enhancement(enhancement_id)

        if not player or not enhancement:
            return None

        if player["total_experience"] < enhancement["experience_cost"]:
            return {"error": "Not enough experience to buy this enhancement"}

        # Déduire le coût et ajouter l'amélioration
        player["total_experience"] -= enhancement["experience_cost"]

        connection = get_db_connection()
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

        return {"message": "Enhancement purchased successfully"}
