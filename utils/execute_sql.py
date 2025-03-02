import pymysql
from utils.db_connection import get_db_connection

def execute_sql_file(sql_file: str):
    """
    Exécute un script SQL depuis un fichier.
    """
    connection = get_db_connection()
    if not connection:
        return

    try:
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_script = file.read()

        with connection.cursor() as cursor:
            for statement in sql_script.split(";"):
                if statement.strip():
                    cursor.execute(statement)
        connection.commit()
        print(f"✅ Script SQL '{sql_file}' exécuté avec succès !")
    except Exception as e:
        print(f"❌ Erreur SQL : {e}")
    finally:
        connection.close()

# Lancer l’exécution
if __name__ == "__main__":
    execute_sql_file("clicker.sql")
