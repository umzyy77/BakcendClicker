import pymysql
from utils.db_connection import get_db_connection
from utils.logger import log_error, log_info

class UpgradeService:
    """
    Service gérant les améliorations disponibles pour les joueurs.
    """

    @staticmethod
    def get_total_click_bonus(player_id: int) -> int:
        """
        Récupère le bonus total de clics en fonction des améliorations achetées par le joueur.
        Utilisé dans la gameloop du player_mission_service.py.
        """
        connection = get_db_connection()
        if not connection:
            return 0  # Aucun bonus en cas d'erreur

        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT COALESCE(SUM(ul.boost_value), 0) AS total_bonus
                FROM player_upgrade pu
                JOIN upgrade_level ul ON pu.id_level = ul.id_level
                WHERE pu.id_player = %s
                """
                cursor.execute(sql, (player_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération du bonus total de clics : {e}")
            return 0
        finally:
            connection.close()

    @staticmethod
    def get_all_upgrades(player_id: int):
        """
        Récupère toutes les améliorations disponibles et leur niveau pour un joueur.
        Sert à afficher dans le front-end pour voir les upgrades achetables ou déjà possédées.
        """
        connection = get_db_connection()
        if not connection:
            return []

        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT u.id_upgrade, u.name, ul.id_level, ul.level, ul.cost, ul.boost_value,
                       (pu.id_player IS NOT NULL) AS purchased
                FROM upgrade u
                JOIN upgrade_level ul ON u.id_upgrade = ul.id_upgrade
                LEFT JOIN player_upgrade pu ON ul.id_level = pu.id_level AND pu.id_player = %s
                ORDER BY u.id_upgrade, ul.level ASC
                """
                cursor.execute(sql, (player_id,))
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération des améliorations : {e}")
            return []
        finally:
            connection.close()

    @staticmethod
    def buy_upgrade(player_id: int, upgrade_id: int) -> bool:
        """
        Permet d'acheter une amélioration pour le joueur.
        Vérifie :
        - Si le joueur a assez d'argent.
        - Si l'amélioration n'est pas déjà au niveau max.
        - Si l'amélioration peut être achetée (prend le niveau suivant).
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                # Récupérer le niveau actuel de l'amélioration pour le joueur
                sql = """
                SELECT ul.id_level, ul.level, ul.cost, ul.boost_value, u.id_upgrade
                FROM upgrade_level ul
                JOIN upgrade u ON ul.id_upgrade = u.id_upgrade
                LEFT JOIN player_upgrade pu ON ul.id_level = pu.id_level AND pu.id_player = %s
                WHERE u.id_upgrade = %s
                ORDER BY ul.level ASC
                """
                cursor.execute(sql, (player_id, upgrade_id))
                levels = cursor.fetchall()

                if not levels:
                    log_error(f"❌ Aucune amélioration trouvée avec l'ID {upgrade_id}")
                    return False

                # Déterminer le niveau suivant disponible
                current_level = None
                for level in levels:
                    if level[-1]:  # Vérifie si l'upgrade est déjà achetée
                        current_level = level[1]  # Niveau actuel

                next_level = next((lvl for lvl in levels if lvl[1] == (current_level or 0) + 1), None)

                if not next_level:
                    log_info(f"🚫 Le joueur {player_id} a déjà le niveau max de l'upgrade {upgrade_id}.")
                    return False

                # Vérifier si le joueur a assez d'argent
                sql = "SELECT money FROM player WHERE id_player = %s"
                cursor.execute(sql, (player_id,))
                player = cursor.fetchone()

                if not player or player[0] < next_level[2]:
                    log_info(f"🚫 Le joueur {player_id} n'a pas assez d'argent pour acheter l'upgrade {upgrade_id}.")
                    return False

                # Déduire l'argent et ajouter l'amélioration
                sql = "UPDATE player SET money = money - %s WHERE id_player = %s"
                cursor.execute(sql, (next_level[2], player_id))

                sql = "INSERT INTO player_upgrade (id_player, id_level) VALUES (%s, %s)"
                cursor.execute(sql, (player_id, next_level[0]))

                connection.commit()
                log_info(f"✅ Le joueur {player_id} a acheté l'upgrade {upgrade_id} (Niveau {next_level[1]}).")
                return True
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de l'achat de l'amélioration : {e}")
            return False
        finally:
            connection.close()
