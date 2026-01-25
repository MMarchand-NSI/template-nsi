"""
install_wrapper.py - Wrapper multi-plateforme pour les installations

Ce script détecte automatiquement le système d'exploitation et appelle
le script d'installation approprié :
- Windows : installs.py
- Linux   : installs_linux.py
- macOS   : installs_macos.py
"""

import sys
import platform
import subprocess
from pathlib import Path


def detect_os():
    """Détecte le système d'exploitation"""
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        raise RuntimeError(f"Système d'exploitation non supporté: {system}")


def get_install_script(os_type):
    """Retourne le chemin du script d'installation selon l'OS"""
    script_dir = Path(__file__).parent

    scripts = {
        "windows": script_dir / "installs.py",
        "linux": script_dir / "installs_linux.py",
        "macos": script_dir / "installs_macos.py"
    }

    return scripts.get(os_type)


def get_install_module_name(os_type):
    """Retourne le nom du module d'installation selon l'OS"""
    modules = {
        "windows": "installs",
        "linux": "installs_linux",
        "macos": "installs_macos"
    }
    return modules.get(os_type)


def get_available_components(os_type):
    """Retourne la liste des composants disponibles selon l'OS en important le module"""
    import importlib

    module_name = get_install_module_name(os_type)
    if not module_name:
        return []

    try:
        # Importer dynamiquement le module
        module = importlib.import_module(module_name)
        # Récupérer la constante AVAILABLE_COMPONENTS
        return getattr(module, 'AVAILABLE_COMPONENTS', [])
    except (ImportError, AttributeError):
        return []


if __name__ == "__main__":
    try:
        # Détecter l'OS
        os_type = detect_os()
        print(f"🖥️  Système détecté: {os_type}")

        # Obtenir le script approprié
        install_script = get_install_script(os_type)

        if not install_script.exists():
            print(f"❌ Script d'installation introuvable: {install_script}")
            sys.exit(1)

        # Obtenir les composants disponibles
        available = get_available_components(os_type)

        # Passer tous les arguments au script approprié
        if len(sys.argv) < 2:
            # Afficher l'aide
            print(f"Composants disponibles sur {os_type}: {', '.join(available)}")
            print(f"\nUsage: python install_wrapper.py <composant>")
            sys.exit(1)

        # Vérifier que le composant est disponible sur cette plateforme
        component = sys.argv[1].lower()
        if component not in available:
            print(f"⚠️  Le composant '{component}' n'est pas disponible sur {os_type}")
            print(f"ℹ️  Composants disponibles: {', '.join(available)}")
            sys.exit(1)

        # Exécuter le script approprié avec les arguments
        args = [sys.executable, str(install_script)] + sys.argv[1:]
        result = subprocess.run(args)
        sys.exit(result.returncode)

    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
