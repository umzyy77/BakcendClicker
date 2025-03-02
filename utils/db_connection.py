import pymysql
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

def get_db_connection():
    """
    Établit une connexion sécurisée à la base de données.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ Connexion réussie à MySQL !")
        return connection
    except pymysql.MySQLError as e:
        print(f"❌ Erreur de connexion : {e}")
        return None
