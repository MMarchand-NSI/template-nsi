from pathlib import Path
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


def log_info(message: str):
    """Affiche un message d'information en cyan."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")
    else:
        print(f"ℹ️  {message}")


def log_success(message: str):
    """Affiche un message de succès en vert."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ {message}{Style.RESET_ALL}")
    else:
        print(f"✅ {message}")


def log_warning(message: str):
    """Affiche un avertissement en jaune."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  {message}{Style.RESET_ALL}")
    else:
        print(f"⚠️  {message}")


def log_error(message: str):
    """Affiche une erreur en rouge."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.RED}{Style.BRIGHT}❌ {message}{Style.RESET_ALL}", file=sys.stderr)
    else:
        print(f"❌ {message}", file=sys.stderr)


def lycee() -> bool:
    """
    On est au lycée si le répertoire C:/Programmes_Portables existe
    """
    return Path(r"C:\Programmes_Portables").exists()


