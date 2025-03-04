from utils.db_connection import get_db_connection
from utils.logger import log_error


class PlayerMissionService:
    @staticmethod
    def update_mission_status(player_id: int, mission_id: int, new_status: int):
        """
        Met à jour le statut d'une mission pour un joueur.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE player_mission SET id_status = %s WHERE id_player = %s AND id_mission = %s",
                               (new_status, player_id, mission_id))
                connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            log_error(f"Erreur lors de la mise à jour du statut de la mission {mission_id} pour le joueur {player_id}: {e}")
            return False

        finally:
            connection.close()

    @staticmethod
    def complete_mission(player_id: int, mission_id: int):
        """
        Marque une mission comme complétée et attribue les récompenses au joueur.
        """
        connection = get_db_connection()
        if not connection:
            return False

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT reward_money, reward_power FROM mission WHERE id_mission = %s", (mission_id,))
                rewards = cursor.fetchone()

                if not rewards:
                    return False

                cursor.execute("UPDATE player SET money = money + %s, hacking_power = hacking_power + %s WHERE id_player = %s",
                               (rewards['reward_money'], rewards['reward_power'], player_id))
                cursor.execute("UPDATE player_mission SET id_status = 3 WHERE id_player = %s AND id_mission = %s",
                               (player_id, mission_id))
                connection.commit()
                return True

        except Exception as e:
            log_error(f"Erreur lors de la complétion de la mission {mission_id} pour le joueur {player_id}: {e}")
            return False

        finally:
            connection.close()
