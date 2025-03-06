import pymysql
import os
from dotenv import load_dotenv
from utils.logger import log_info, log_error

# Charger les variables d'environnement
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
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
        log_info("✅ Connexion réussie à MySQL !")
        return connection
    except pymysql.MySQLError as e:
        log_error(f"❌ Erreur de connexion MySQL : {e}")
        return None