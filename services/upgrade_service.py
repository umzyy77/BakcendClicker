from models.upgrade import Upgrade
from utils.db_connection import get_db_connection
from utils.logger import log_info, log_error


class UpgradeService:
    @staticmethod
    def get_all_upgrades():
        """
        Récupère toutes les améliorations disponibles.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM upgrade")
                upgrades_data = cursor.fetchall()

            return [Upgrade(**upgrade).to_dict() for upgrade in upgrades_data]

        except Exception as e:
            log_error(f"Erreur lors de la récupération des améliorations: {e}")
            return []

        finally:
            connection.close()

    @staticmethod
    def purchase_upgrade(player_id: int, upgrade_level_id: int):
        """
        Permet à un joueur d'acheter une amélioration spécifique.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT cost, boost_value FROM upgrade_level WHERE id_level = %s", (upgrade_level_id,))
                upgrade_data = cursor.fetchone()

                if not upgrade_data:
                    return None

                cursor.execute("SELECT money, hacking_power FROM player WHERE id_player = %s", (player_id,))
                player_data = cursor.fetchone()

                if not player_data or player_data["money"] < upgrade_data["cost"]:
                    return {"error": "Not enough money"}

                new_money = player_data["money"] - upgrade_data["cost"]
                new_power = player_data["hacking_power"] + upgrade_data["boost_value"]

                cursor.execute("UPDATE player SET money = %s, hacking_power = %s WHERE id_player = %s",
                               (new_money, new_power, player_id))
                cursor.execute("INSERT INTO player_upgrade (id_player, id_level) VALUES (%s, %s)",
                               (player_id, upgrade_level_id))
                connection.commit()

            return {"message": "Upgrade purchased successfully", "new_money": new_money, "new_power": new_power}

        except Exception as e:
            log_error(f"Erreur lors de l'achat de l'amélioration {upgrade_level_id} par le joueur {player_id}: {e}")
            return None

        finally:
            connection.close()
