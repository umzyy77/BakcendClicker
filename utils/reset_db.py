import pymysql
from utils.db_connection import get_db_connection

def reset_database():
    """
    Supprime toutes les tables de la base de données et réinitialise la structure.
    """
    connection = get_db_connection()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            connection.commit()
            print("✅ Base de données réinitialisée avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation de la base : {e}")
    finally:
        connection.close()

# Exécution directe
if __name__ == "__main__":
    reset_database()
