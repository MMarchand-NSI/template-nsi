from pathlib import Path
import sys

def log_info(message: str):
    """Affiche un message d'information."""
    print(f"ℹ️  {message}")

def log_success(message: str):
    """Affiche un message de succès."""
    print(f"✅ {message}")

def log_warning(message: str):
    """Affiche un avertissement."""
    print(f"⚠️  {message}")

def log_error(message: str):
    """Affiche une erreur."""
    print(f"❌ {message}", file=sys.stderr)


def lycee() -> bool:
    """
    On est au lycée si le répertoire C:/Programmes_Portables existe
    """
    return Path(r"C:\Programmes_Portables").exists()


