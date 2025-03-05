import pymysql

from services.upgrade_service import UpgradeService
from utils.db_connection import get_db_connection
from utils.logger import log_error


class PlayerMissionService:
    """
    Service gérant l'association des joueurs avec les missions.
    """

    @staticmethod
    def get_missions_for_player(player_id: int):
        """
        Récupère toutes les missions d’un joueur avec leur statut actuel.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT pm.id_mission, m.name, pm.id_status, pm.clicks_done, d.clicks_required
                FROM player_mission pm
                JOIN mission m ON pm.id_mission = m.id_mission
                JOIN difficulty d ON m.id_difficulty = d.id_difficulty
                WHERE pm.id_player = %s
                ORDER BY pm.id_mission
                """
                cursor.execute(sql, (player_id,))
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération des missions du joueur : {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def get_first_unlocked_mission(player_id: int):
        """
        Récupère l'ID de la première mission déverrouillée mais non commencée.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT id_mission FROM player_mission 
                WHERE id_player = %s AND id_status = 2 
                ORDER BY id_mission ASC LIMIT 1
                """
                cursor.execute(sql, (player_id,))
                mission = cursor.fetchone()
                return mission["id_mission"] if mission else None
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la récupération de la mission déverrouillée : {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def start_mission(player_id: int, mission_id: int = None):
        """
        Démarre une mission si elle est en unlocked ou reprend une mission en cours/completée.
        """
        if not mission_id:
            return False

        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE player_mission SET id_status = 3 WHERE id_player = %s AND id_mission = %s AND id_status IN (2, 3, 4)
                """
                cursor.execute(sql, (player_id, mission_id))
                connection.commit()
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors du démarrage de la mission : {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def assign_default_missions(player_id: int):
        """
        Assigne toutes les missions au joueur avec la première mission en unlocked.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                # Trouver l'ID de la première mission
                sql = "SELECT MIN(id_mission) AS first_mission FROM mission"
                cursor.execute(sql)
                first_mission = cursor.fetchone()

                if not first_mission or not first_mission["first_mission"]:
                    return False

                first_mission_id = first_mission["first_mission"]

                # Insérer les missions avec la première débloquée
                sql = """
                INSERT INTO player_mission (id_player, id_mission, id_status, clicks_done)
                SELECT %s, id_mission, 
                       CASE WHEN id_mission = %s THEN 2 ELSE 1 END, 0 
                FROM mission
                """
                cursor.execute(sql, (player_id, first_mission_id))
                connection.commit()
                return True
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de l'assignation des missions : {e}")
            return False
        finally:
            connection.close()



    @staticmethod
    def assign_next_mission(player_id: int, mission_id: int):
        """
        Déverrouille la prochaine mission après la complétion de la mission actuelle.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                # Trouver l'ID de la mission suivante
                sql = """
                SELECT id_mission FROM mission 
                WHERE id_mission > %s 
                ORDER BY id_mission ASC 
                LIMIT 1
                """
                cursor.execute(sql, (mission_id,))
                next_mission = cursor.fetchone()

                if not next_mission:
                    return False  # Aucune mission suivante

                next_mission_id = next_mission["id_mission"]

                # Débloquer la mission suivante
                sql = """
                UPDATE player_mission 
                SET id_status = 2 
                WHERE id_player = %s 
                  AND id_mission = %s 
                  AND id_status = 1
                """
                cursor.execute(sql, (player_id, next_mission_id))
                connection.commit()

                # 🚀 Enregistrer la mission débloquée dans player_progress
                sql = """
                           INSERT INTO player_progress (id_player, last_unlocked_mission) 
                           VALUES (%s, %s)
                           ON DUPLICATE KEY UPDATE last_unlocked_mission = %s
                           """
                cursor.execute(sql, (player_id, next_mission_id, next_mission_id))
                connection.commit()

                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors du déverrouillage de la prochaine mission : {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def check_newly_unlocked_mission(player_id: int):
        """
        Vérifie si une mission vient juste d'être débloquée et supprime l'info après récupération.
        """
        connection = get_db_connection()
        if not connection:
            return None

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Récupérer l'ID de la dernière mission débloquée
                sql = "SELECT last_unlocked_mission FROM player_progress WHERE id_player = %s"
                cursor.execute(sql, (player_id,))
                result = cursor.fetchone()

                if result and result["last_unlocked_mission"]:
                    mission_id = result["last_unlocked_mission"]

                    # Supprimer l'info après récupération pour éviter que l'animation se rejoue
                    sql = "UPDATE player_progress SET last_unlocked_mission = NULL WHERE id_player = %s"
                    cursor.execute(sql, (player_id,))
                    connection.commit()

                    return {"id_mission": mission_id, "just_unlocked": True}

                return {"just_unlocked": False}

        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la vérification des nouvelles missions débloquées : {e}")
            return None
        finally:
            connection.close()

    @staticmethod
    def increment_clicks(player_id: int, mission_id: int):
        """
        Incrémente les clics d'une mission en fonction des bonus et vérifie la complétion.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                # 🔒 Verrouille la mission en cours pour éviter les race conditions
                sql = """
                SELECT clicks_done, id_status FROM player_mission 
                WHERE id_player = %s AND id_mission = %s FOR UPDATE
                """
                cursor.execute(sql, (player_id, mission_id))
                mission = cursor.fetchone()

                if not mission or mission[1] != 3:  # Vérifie si la mission est bien en cours (id_status = 3)
                    return False  # Mission pas en cours

                # 🔥 Récupérer le bonus de clics grâce à UpgradeService
                click_bonus = UpgradeService.get_total_click_bonus(player_id)
                click_increment = 1 + click_bonus  # 1 clic de base + bonus d'améliorations

                new_clicks = mission[0] + click_increment

                # Mettre à jour le compteur de clics
                sql = """
                UPDATE player_mission SET clicks_done = %s 
                WHERE id_player = %s AND id_mission = %s
                """
                cursor.execute(sql, (new_clicks, player_id, mission_id))
                connection.commit()

                # Vérifier si l'objectif de la mission est atteint
                sql = """
                SELECT d.clicks_required 
                FROM mission m 
                JOIN difficulty d ON m.id_difficulty = d.id_difficulty 
                WHERE m.id_mission = %s
                """
                cursor.execute(sql, (mission_id,))
                objective = cursor.fetchone()

                if new_clicks >= objective[0]:
                    return PlayerMissionService.complete_mission(player_id, mission_id)

                return True
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de l'incrémentation des clics : {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def complete_mission(player_id: int, mission_id: int):
        """
        Marque une mission comme complétée, attribue les récompenses et débloque la suivante.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                sql = "SELECT reward_money, reward_power FROM mission WHERE id_mission = %s"
                cursor.execute(sql, (mission_id,))
                mission = cursor.fetchone()

                if not mission:
                    return False

                sql = "UPDATE player_mission SET id_status = 4 WHERE id_player = %s AND id_mission = %s"
                cursor.execute(sql, (player_id, mission_id))

                sql = "UPDATE player SET money = money + %s, hacking_power = hacking_power + %s WHERE id_player = %s"
                cursor.execute(sql, (mission["reward_money"], mission["reward_power"], player_id))

                connection.commit()

                # Débloquer la mission suivante
                PlayerMissionService.assign_next_mission(player_id, mission_id)

                return True
        except pymysql.MySQLError as e:
            log_error(f"❌ Erreur lors de la complétion de la mission : {e}")
            return False
        finally:
            connection.close()




