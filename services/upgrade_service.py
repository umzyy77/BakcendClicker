from models.upgrade import Upgrade
from models.upgrade_level import UpgradeLevel
from models.player import Player
from utils.db_connection import get_db_connection
from utils.logger import log_error

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

            # Créer des objets Upgrade et les convertir en dictionnaires
            return [Upgrade(**upgrade).to_dict() for upgrade in upgrades_data]

        except Exception as e:
            log_error(f"Erreur lors de la récupération des améliorations: {e}")
            return []

        finally:
            connection.close()

    @staticmethod
    def get_player_upgrades(player_id: int):
        """
        Récupère toutes les améliorations achetées par un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                # Récupérer les améliorations achetées par le joueur
                cursor.execute("""
                    SELECT upgrade.id_upgrade, upgrade.name, upgrade_level.level, upgrade_level.cost, upgrade_level.boost_value 
                    FROM player_upgrade
                    INNER JOIN upgrade_level ON player_upgrade.id_level = upgrade_level.id_level
                    INNER JOIN upgrade ON upgrade_level.id_upgrade = upgrade.id_upgrade
                    WHERE player_upgrade.id_player = %s
                """, (player_id,))
                upgrades_data = cursor.fetchall()

            # Créer des objets UpgradeLevel et les convertir en dictionnaires
            upgrades = []
            for upgrade_data in upgrades_data:
                # Créer un objet Upgrade
                upgrade = Upgrade(id_upgrade=upgrade_data['id_upgrade'], name=upgrade_data['name'])

                # Créer un objet UpgradeLevel en incluant l'objet Upgrade
                upgrade_level = UpgradeLevel(
                    id_level=upgrade_data['id_level'],
                    level=upgrade_data['level'],
                    cost=upgrade_data['cost'],
                    boost_value=upgrade_data['boost_value'],
                    upgrade=upgrade  # Lien avec l'objet Upgrade
                )

                # Ajouter l'UpgradeLevel à la liste
                upgrades.append(upgrade_level.to_dict())

            return upgrades

        except Exception as e:
            log_error(f"Erreur lors de la récupération des améliorations du joueur {player_id}: {e}")
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
                # Récupérer les informations de l'amélioration
                cursor.execute("SELECT cost, boost_value FROM upgrade_level WHERE id_level = %s", (upgrade_level_id,))
                upgrade_data = cursor.fetchone()

                if not upgrade_data:
                    return None

                # Récupérer les informations du joueur
                cursor.execute("SELECT money, hacking_power FROM player WHERE id_player = %s", (player_id,))
                player_data = cursor.fetchone()

                # Vérifier si le joueur a assez d'argent
                if player_data["money"] < upgrade_data["cost"]:
                    return {"error": "Not enough money"}

                new_money = player_data["money"] - upgrade_data["cost"]
                new_power = player_data["hacking_power"] + upgrade_data["boost_value"]

                # Mise à jour du joueur (argent et puissance de hacking)
                cursor.execute("""
                    UPDATE player SET money = %s, hacking_power = %s WHERE id_player = %s
                """, (new_money, new_power, player_id))

                # Ajouter l'amélioration à la liste des améliorations du joueur
                cursor.execute("""
                    INSERT INTO player_upgrade (id_player, id_level) VALUES (%s, %s)
                """, (player_id, upgrade_level_id))
                connection.commit()

            return {"message": "Upgrade purchased successfully", "new_money": new_money, "new_power": new_power}

        except Exception as e:
            log_error(f"Erreur lors de l'achat de l'amélioration {upgrade_level_id} par le joueur {player_id}: {e}")
            return None

        finally:
            connection.close()
