import pymysql
import pandas as pd
from utils.db_connection import get_db_connection

def fetch_database_tables():
    """
    Récupère et affiche le contenu de toutes les tables de la base de données.
    """
    connection = get_db_connection()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            for table in tables:
                table_name = list(table.values())[0]
                cursor.execute(f"SELECT * FROM {table_name};")
                data = cursor.fetchall()

                df = pd.DataFrame(data)
                print(f"\n🔹 Table: {table_name}")
                print(df if not df.empty else "⚠️ Aucune donnée dans cette table.")
    finally:
        connection.close()

# Exécution directe
if __name__ == "__main__":
    fetch_database_tables()
