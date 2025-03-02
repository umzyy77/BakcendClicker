import logging

# Configurer le logger
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str):
    """Enregistre un message d'information."""
    logging.info(message)
    print(f"ℹ️ {message}")

def log_error(message: str):
    """Enregistre une erreur."""
    logging.error(message)
    print(f"❌ {message}")
