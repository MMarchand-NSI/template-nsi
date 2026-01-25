"""
installs_macos.py - Gestionnaire d'installation de composants pour macOS

Ce script facilite l'installation et la configuration de différents outils de développement
sous macOS. Il utilise Homebrew comme gestionnaire de paquets.

Gestionnaire de paquets :
-------------------------
- Homebrew (brew) : Le gestionnaire de paquets standard pour macOS

Composants installables :
--------------------------
- homebrew    : Installation de Homebrew (si non installé)
- nodejs      : Node.js et npm
- elm         : Node.js + Elm (langage de programmation fonctionnel pour le web)
- rust        : Compilateur Rust et Cargo
- nasm        : Assembleur NASM + GDB (débogueur)
- qemu        : Émulateur de machines virtuelles
- postgresql  : Serveur de base de données PostgreSQL (avec initialisation automatique)

Fonctions principales :
-----------------------
check_homebrew() -> bool
    Vérifie si Homebrew est installé.

install_homebrew()
    Installe Homebrew si non présent.

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

Note :
------
Homebrew sera automatiquement installé s'il n'est pas déjà présent sur le système.
"""

import subprocess
import sys
import os
from pathlib import Path


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


def install_homebrew():
    """Installe Homebrew si non présent"""
    if check_homebrew():
        print("✅ Homebrew est déjà installé")
        return

    print("✨ Installation de Homebrew...")
    print("ℹ️  Vous devrez peut-être entrer votre mot de passe")

    # Script officiel d'installation de Homebrew
    install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    executer(install_script)

    print("✅ Homebrew installé avec succès")

    # Ajouter Homebrew au PATH selon l'architecture
    arch_check = subprocess.run("uname -m", shell=True, capture_output=True, text=True)
    arch = arch_check.stdout.strip()

    if arch == "arm64":  # Apple Silicon (M1/M2/M3)
        brew_path = "/opt/homebrew/bin/brew"
    else:  # Intel
        brew_path = "/usr/local/bin/brew"

    print(f"ℹ️  Pour utiliser Homebrew, vous devrez peut-être exécuter:")
    print(f'    eval "$({brew_path} shellenv)"')


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


def install_nodejs():
    """Installe Node.js et npm"""
    install_package("Node.js", brew_pkg="node")


def install_elm():
    """Installe nodejs et elm (via npm)"""
    install_nodejs()
    print("✨ Installation d'Elm via npm...")
    executer("npm install -g elm")
    print("✅ Elm installé avec succès")


def install_rust():
    """Installe Rust via rustup (méthode recommandée) ou Homebrew"""
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
    install_package("NASM", brew_pkg="nasm")
    install_package("GDB", brew_pkg="gdb")


def install_qemu():
    """Installe QEMU"""
    install_package("QEMU", brew_pkg="qemu")


def install_postgresql():
    """Installe et initialise PostgreSQL"""
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


# Dictionnaire des fonctions d'installation et opérations
INSTALLATIONS = {
    "homebrew": install_homebrew,
    "nodejs": install_nodejs,
    "elm": install_elm,
    "rust": install_rust,
    "nasm": install_nasm,
    "qemu": install_qemu,
    "postgresql": install_postgresql,
    "postgres-start": postgres_start,
    "postgres-stop": postgres_stop
}

# Liste des composants disponibles
AVAILABLE_COMPONENTS = list(INSTALLATIONS.keys())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python installs_macos.py [{' | '.join(INSTALLATIONS.keys())} | postgres-create <nom>]")
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
    elif choix in INSTALLATIONS:
        try:
            # Vérifier que Homebrew est installé (sauf si on installe Homebrew)
            if choix != "homebrew" and not check_homebrew():
                print("⚠️  Homebrew n'est pas installé")
                print("ℹ️  Installation automatique de Homebrew...")
                install_homebrew()
                print()

            INSTALLATIONS[choix]()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    else:
        print(f"Option inconnue: {choix}")
        print(f"Options disponibles: {', '.join(INSTALLATIONS.keys())}, postgres-create")
        sys.exit(1)
