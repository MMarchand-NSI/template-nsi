"""
installs_macos.py - Gestionnaire d'installation de composants pour macOS

Ce script facilite l'installation et la configuration de différents outils de développement
sous macOS. Il utilise Homebrew comme gestionnaire de paquets.

Gestionnaire de paquets :
-------------------------
- Homebrew (brew) : Le gestionnaire de paquets standard pour macOS (doit être installé au préalable)

Composants installables :
--------------------------
- elm         : Node.js + Elm (langage de programmation fonctionnel pour le web)
- rust        : Compilateur Rust et Cargo
- nasm        : Assembleur NASM + GDB (débogueur)
- qemu        : Émulateur de machines virtuelles
- postgresql  : Serveur de base de données PostgreSQL (avec initialisation automatique)
- graphviz    : Outil de visualisation de graphes (dot, neato, etc.)

Opérations PostgreSQL :
-----------------------
- postgres-start  : Démarre le serveur PostgreSQL
- postgres-stop   : Arrête le serveur PostgreSQL
- postgres-create : Crée une nouvelle base de données

Fonctions principales :
-----------------------
check_homebrew() -> bool
    Vérifie si Homebrew est installé.

executer(cmd: str)
    Exécute une commande shell.

install_package(package_name: str, brew_pkg: str, cask: bool = False)
    Installe un paquet via Homebrew.

postgres_init()
    Initialise PostgreSQL avec un superuser "padawan" et encodage UTF-8.

Utilisation en ligne de commande :
-----------------------------------
    python installs_macos.py <composant>

Exemples :
    python installs_macos.py rust
    python installs_macos.py postgresql

Prérequis :
-----------
Homebrew doit être installé au préalable. Pour l'installer, visitez https://brew.sh
"""

import subprocess
import sys
import os
from pathlib import Path
from components_info import confirm_installation


def check_homebrew():
    """Vérifie si Homebrew est installé"""
    result = subprocess.run("command -v brew", shell=True, capture_output=True)
    return result.returncode == 0


def executer(cmd: str):
    """
    Exécute une commande shell

    Args:
        cmd: Commande à exécuter
    """
    print(f"📦 Exécution: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True)

    if result.returncode != 0:
        print(f"❌ Erreur lors de l'exécution de: {cmd}")
        sys.exit(1)

    return result


def install_package(package_name: str, brew_pkg: str, cask: bool = False):
    """
    Installe un paquet via Homebrew

    Args:
        package_name: Nom du composant (pour affichage)
        brew_pkg: Nom du paquet Homebrew
        cask: Si True, utilise 'brew install --cask'
    """
    if not check_homebrew():
        print("❌ Homebrew n'est pas installé. Exécutez d'abord: python installs_macos.py homebrew")
        sys.exit(1)

    print(f"✨ Installation de {package_name}...")

    # Mise à jour de Homebrew
    executer("brew update")

    # Installation du paquet
    if cask:
        executer(f"brew install --cask {brew_pkg}")
    else:
        executer(f"brew install {brew_pkg}")

    print(f"✅ {package_name} installé avec succès")


def install_elm():
    """Installe nodejs et elm (via npm)"""
    if not confirm_installation("elm"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Node.js", brew_pkg="node")
    print("✨ Installation d'Elm via npm...")
    executer("npm install -g elm")
    print("✅ Elm installé avec succès")


def install_rust():
    """Installe Rust via rustup (méthode recommandée) ou Homebrew"""
    if not confirm_installation("rust"):
        print("ℹ️  Installation annulée.")
        return

    print("✨ Installation de Rust...")

    # Vérifier si rustup est déjà installé
    result = subprocess.run("command -v rustup", shell=True, capture_output=True)

    if result.returncode != 0:
        # Demander à l'utilisateur sa préférence
        print("ℹ️  Deux méthodes d'installation disponibles:")
        print("   1. rustup (recommandé) - permet de gérer plusieurs versions de Rust")
        print("   2. Homebrew - plus simple mais moins flexible")
        print()

        # Installer via rustup par défaut
        print("📥 Installation via rustup (recommandé)...")
        executer("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")

        # Source le fichier d'environnement
        home = os.path.expanduser("~")
        cargo_env = f"{home}/.cargo/env"
        if Path(cargo_env).exists():
            print(f"ℹ️  Pour utiliser Rust, exécutez: source {cargo_env}")
    else:
        # Mettre à jour rustup
        executer("rustup update")

    print("✅ Rust installé avec succès")


def install_nasm():
    """Installe NASM et GDB"""
    if not confirm_installation("nasm"):
        print("ℹ️  Installation annulée.")
        return

    install_package("NASM", brew_pkg="nasm")
    install_package("GDB", brew_pkg="gdb")


def install_qemu():
    """Installe QEMU"""
    if not confirm_installation("qemu"):
        print("ℹ️  Installation annulée.")
        return

    install_package("QEMU", brew_pkg="qemu")


def install_graphviz():
    """Installe Graphviz"""
    if not confirm_installation("graphviz"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Graphviz", brew_pkg="graphviz")


def install_postgresql():
    """Installe et initialise PostgreSQL"""
    if not confirm_installation("postgresql"):
        print("ℹ️  Installation annulée.")
        return

    install_package("PostgreSQL", brew_pkg="postgresql@16")
    postgres_init()


def get_database_dir():
    """Retourne le chemin du répertoire DATABASE dans le home de l'utilisateur"""
    home = os.path.expanduser("~")
    return f"{home}/DATABASE"


def postgres_init():
    """
    Initialise PostgreSQL avec un superuser "padawan" et mot de passe "padawan"
    """
    database_dir = get_database_dir()

    # Vérification si le répertoire existe déjà
    if Path(database_dir).exists():
        print(f"⚠️  Le répertoire {database_dir} existe déjà.")
        reponse = input("Voulez-vous le supprimer et réinitialiser PostgreSQL ? (oui/non) : ").strip().lower()
        if reponse not in ("oui", "o", "yes", "y"):
            print("ℹ️  Initialisation annulée.")
            return
        # Suppression du répertoire existant
        import shutil
        shutil.rmtree(database_dir)
        print("ℹ️  Répertoire supprimé.")

    print("✨ Initialisation de PostgreSQL...")

    # Démarrer le service PostgreSQL
    print("📦 Démarrage du service PostgreSQL...")
    executer("brew services start postgresql@16")

    # Attendre que PostgreSQL démarre
    print("⏳ Attente du démarrage de PostgreSQL...")
    import time
    time.sleep(3)

    # Créer l'utilisateur padawan
    print("👤 Création de l'utilisateur padawan...")

    # Créer l'utilisateur avec mot de passe
    create_user_cmd = """psql postgres -c "CREATE USER padawan WITH SUPERUSER PASSWORD 'padawan';" 2>/dev/null || echo "L'utilisateur existe déjà" """
    subprocess.run(create_user_cmd, shell=True)

    # Créer la base de données
    create_db_cmd = """psql postgres -c "CREATE DATABASE padawan OWNER padawan;" 2>/dev/null || echo "La base de données existe déjà" """
    subprocess.run(create_db_cmd, shell=True)

    print(f"✅ PostgreSQL initialisé")
    print(f"ℹ️  Utilisateur: padawan")
    print(f"ℹ️  Mot de passe: padawan")
    print(f"ℹ️  Base de données: padawan")
    print(f"ℹ️  Pour démarrer PostgreSQL: brew services start postgresql@16")
    print(f"ℹ️  Pour arrêter PostgreSQL: brew services stop postgresql@16")


def postgres_start():
    """Démarre l'instance PostgreSQL"""
    # Vérifier si déjà démarré
    result = subprocess.run(
        "brew services list | grep postgresql@16",
        shell=True,
        capture_output=True,
        text=True
    )
    if "started" in result.stdout:
        print("✅ Le serveur PostgreSQL est déjà démarré")
        return

    print("✨ Démarrage de PostgreSQL...")
    executer("brew services start postgresql@16")
    print("✅ Serveur PostgreSQL démarré")


def postgres_stop():
    """Arrête l'instance PostgreSQL"""
    print("✨ Arrêt de PostgreSQL...")
    executer("brew services stop postgresql@16")
    print("✅ Serveur PostgreSQL arrêté")


def postgres_create_db(nom: str):
    """Crée une base de données PostgreSQL"""
    print(f"✨ Création de la base de données '{nom}'...")
    executer(f'psql postgres -c "CREATE DATABASE {nom} OWNER padawan ENCODING \'UTF8\';"')
    print(f"✅ Base de données '{nom}' créée")


# Dictionnaire des fonctions d'installation
INSTALLATIONS = {
    "elm": install_elm,
    "rust": install_rust,
    "nasm": install_nasm,
    "qemu": install_qemu,
    "postgresql": install_postgresql,
    "graphviz": install_graphviz
}

# Dictionnaire des opérations PostgreSQL
OPERATIONS = {
    "postgres-start": postgres_start,
    "postgres-stop": postgres_stop,
    "postgres-create": postgres_create_db
}

# Liste des composants installables (pour tasks.json)
AVAILABLE_COMPONENTS = list(INSTALLATIONS.keys())


if __name__ == "__main__":
    # Fusion des deux dictionnaires pour la CLI
    ALL_COMMANDS = {**INSTALLATIONS, **OPERATIONS}

    if len(sys.argv) < 2:
        print(f"Installations disponibles: {', '.join(INSTALLATIONS.keys())}")
        print(f"Opérations disponibles: {', '.join(OPERATIONS.keys())}")
        print(f"\nUsage: python installs_macos.py <composant|opération> [args]")
        sys.exit(1)

    choix = sys.argv[1].lower()

    if choix == "postgres-create":
        if len(sys.argv) < 3:
            print("Usage: python installs_macos.py postgres-create <nom>")
            sys.exit(1)
        try:
            postgres_create_db(sys.argv[2])
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    elif choix in ALL_COMMANDS:
        try:
            # Vérifier que Homebrew est installé pour les installations
            if choix in INSTALLATIONS and not check_homebrew():
                print("❌ Homebrew n'est pas installé")
                print("ℹ️  Installez d'abord Homebrew en suivant les instructions sur https://brew.sh")
                sys.exit(1)

            ALL_COMMANDS[choix]()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    else:
        print(f"Option inconnue: {choix}")
        print(f"Installations disponibles: {', '.join(INSTALLATIONS.keys())}")
        print(f"Opérations disponibles: {', '.join(OPERATIONS.keys())}")
        sys.exit(1)
