"""
installs_linux.py - Gestionnaire d'installation de composants pour Linux

Ce script facilite l'installation et la configuration de différents outils de développement
sous Linux. Il supporte les distributions basées sur apt (Debian/Ubuntu) et yum (Red Hat/CentOS/Fedora).

Gestionnaires de paquets supportés :
------------------------------------
- apt  : Debian, Ubuntu, Linux Mint, etc.
- yum  : Red Hat, CentOS, Fedora (anciennes versions)
- dnf  : Fedora (nouvelles versions)

Composants installables :
--------------------------
- nodejs      : Node.js et npm
- elm         : Node.js + Elm (langage de programmation fonctionnel pour le web)
- rust        : Compilateur Rust et Cargo
- nasm        : Assembleur NASM + GDB (débogueur)
- qemu        : Émulateur de machines virtuelles
- postgresql  : Serveur de base de données PostgreSQL (avec initialisation automatique)

Fonctions principales :
-----------------------
detect_package_manager() -> str
    Détecte le gestionnaire de paquets disponible sur le système.

executer(cmd: str)
    Exécute une commande shell avec sudo si nécessaire.

install_package(package_name: str, apt_pkg: str, yum_pkg: str)
    Installe un paquet selon le gestionnaire de paquets détecté.

postgres_init()
    Initialise PostgreSQL avec un superuser "padawan" et encodage UTF-8.

Utilisation en ligne de commande :
-----------------------------------
    python installs_linux.py <composant>

Exemples :
    python installs_linux.py rust
    python installs_linux.py postgresql

Note :
------
Certaines commandes nécessitent les privilèges sudo pour s'exécuter.
"""

import subprocess
import sys
import os
from pathlib import Path

# Détection du gestionnaire de paquets
def detect_package_manager():
    """Détecte le gestionnaire de paquets disponible sur le système"""
    if Path("/usr/bin/apt").exists() or Path("/usr/bin/apt-get").exists():
        return "apt"
    elif Path("/usr/bin/dnf").exists():
        return "dnf"
    elif Path("/usr/bin/yum").exists():
        return "yum"
    else:
        raise RuntimeError("Aucun gestionnaire de paquets supporté détecté (apt, yum, dnf)")


def executer(cmd: str, use_sudo: bool = False):
    """
    Exécute une commande shell

    Args:
        cmd: Commande à exécuter
        use_sudo: Si True, préfixe la commande avec sudo
    """
    if use_sudo and os.geteuid() != 0:
        cmd = f"sudo {cmd}"

    print(f"📦 Exécution: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True)

    if result.returncode != 0:
        print(f"❌ Erreur lors de l'exécution de: {cmd}")
        sys.exit(1)

    return result


def install_package(package_name: str, apt_pkg: str = None, yum_pkg: str = None, dnf_pkg: str = None):
    """
    Installe un paquet selon le gestionnaire de paquets

    Args:
        package_name: Nom du composant (pour affichage)
        apt_pkg: Nom du paquet pour apt
        yum_pkg: Nom du paquet pour yum
        dnf_pkg: Nom du paquet pour dnf (si None, utilise yum_pkg)
    """
    pm = detect_package_manager()

    if dnf_pkg is None:
        dnf_pkg = yum_pkg

    print(f"✨ Installation de {package_name}...")

    if pm == "apt":
        if apt_pkg is None:
            raise ValueError(f"Pas de paquet apt défini pour {package_name}")
        executer(f"apt update", use_sudo=True)
        executer(f"apt install -y {apt_pkg}", use_sudo=True)
    elif pm == "dnf":
        if dnf_pkg is None:
            raise ValueError(f"Pas de paquet dnf défini pour {package_name}")
        executer(f"dnf install -y {dnf_pkg}", use_sudo=True)
    elif pm == "yum":
        if yum_pkg is None:
            raise ValueError(f"Pas de paquet yum défini pour {package_name}")
        executer(f"yum install -y {yum_pkg}", use_sudo=True)

    print(f"✅ {package_name} installé avec succès")


def install_nodejs():
    """Installe Node.js et npm"""
    install_package("Node.js", apt_pkg="nodejs npm", yum_pkg="nodejs npm")


def install_elm():
    """Installe nodejs et elm (via npm)"""
    install_nodejs()
    print("✨ Installation d'Elm via npm...")
    executer("npm install -g elm", use_sudo=True)
    print("✅ Elm installé avec succès")


def install_rust():
    """Installe Rust via rustup"""
    print("✨ Installation de Rust...")

    # Vérifier si rustup est déjà installé
    result = subprocess.run("command -v rustup", shell=True, capture_output=True)

    if result.returncode != 0:
        # Installer rustup
        print("📥 Téléchargement et installation de rustup...")
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
    install_package("NASM + GDB", apt_pkg="nasm gdb", yum_pkg="nasm gdb")


def install_qemu():
    """Installe QEMU"""
    install_package("QEMU", apt_pkg="qemu-system", yum_pkg="qemu")


def install_postgresql():
    """Installe et initialise PostgreSQL"""
    install_package("PostgreSQL", apt_pkg="postgresql postgresql-contrib", yum_pkg="postgresql-server postgresql-contrib")
    postgres_init()


def get_database_dir():
    """Retourne le chemin du répertoire DATABASE dans le home de l'utilisateur"""
    home = os.path.expanduser("~")
    return f"{home}/DATABASE"


def postgres_init():
    """
    Initialise PostgreSQL avec un superuser "padawan" et mot de passe "padawan"
    """
    pm = detect_package_manager()
    database_dir = get_database_dir()

    print("✨ Initialisation de PostgreSQL...")

    # Créer le répertoire pour la base de données
    Path(database_dir).mkdir(parents=True, exist_ok=True)

    if pm == "apt":
        # Sur Debian/Ubuntu, PostgreSQL est déjà initialisé et démarré
        print("📦 Démarrage du service PostgreSQL...")
        executer("systemctl start postgresql", use_sudo=True)
        executer("systemctl enable postgresql", use_sudo=True)

        # Créer l'utilisateur padawan
        print("👤 Création de l'utilisateur padawan...")
        executer("sudo -u postgres psql -c \"CREATE USER padawan WITH SUPERUSER PASSWORD 'padawan';\" || true")
        executer("sudo -u postgres psql -c \"CREATE DATABASE padawan OWNER padawan;\" || true")

    elif pm in ["yum", "dnf"]:
        # Sur Red Hat/CentOS/Fedora, il faut initialiser manuellement
        print("📦 Initialisation de la base de données...")

        # Initialiser PostgreSQL (pour RHEL/CentOS)
        if pm == "yum":
            executer("postgresql-setup --initdb", use_sudo=True)
        else:  # dnf
            executer("postgresql-setup --initdb --unit postgresql", use_sudo=True)

        # Démarrer le service
        executer("systemctl start postgresql", use_sudo=True)
        executer("systemctl enable postgresql", use_sudo=True)

        # Créer l'utilisateur padawan
        print("👤 Création de l'utilisateur padawan...")
        executer("sudo -u postgres psql -c \"CREATE USER padawan WITH SUPERUSER PASSWORD 'padawan';\" || true")
        executer("sudo -u postgres psql -c \"CREATE DATABASE padawan OWNER padawan;\" || true")

    print(f"✅ PostgreSQL initialisé")
    print(f"ℹ️  Utilisateur: padawan")
    print(f"ℹ️  Mot de passe: padawan")
    print(f"ℹ️  Base de données: padawan")


def postgres_start():
    """Démarre l'instance PostgreSQL"""
    print("✨ Démarrage de PostgreSQL...")
    executer("systemctl start postgresql", use_sudo=True)
    print("✅ Serveur PostgreSQL démarré")


def postgres_stop():
    """Arrête l'instance PostgreSQL"""
    print("✨ Arrêt de PostgreSQL...")
    executer("systemctl stop postgresql", use_sudo=True)
    print("✅ Serveur PostgreSQL arrêté")


def postgres_create_db(nom: str):
    """Crée une base de données PostgreSQL"""
    print(f"✨ Création de la base de données '{nom}'...")
    executer(f'sudo -u postgres psql -c "CREATE DATABASE {nom} OWNER padawan ENCODING \'UTF8\';"')
    print(f"✅ Base de données '{nom}' créée")


# Dictionnaire des fonctions d'installation et opérations
INSTALLATIONS = {
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
        print(f"Usage: python installs_linux.py [{' | '.join(INSTALLATIONS.keys())} | postgres-create <nom>]")
        sys.exit(1)

    choix = sys.argv[1].lower()

    if choix == "postgres-create":
        if len(sys.argv) < 3:
            print("Usage: python installs_linux.py postgres-create <nom>")
            sys.exit(1)
        try:
            postgres_create_db(sys.argv[2])
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    elif choix in INSTALLATIONS:
        try:
            pm = detect_package_manager()
            print(f"🐧 Système détecté: {pm}")
            INSTALLATIONS[choix]()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    else:
        print(f"Option inconnue: {choix}")
        print(f"Options disponibles: {', '.join(INSTALLATIONS.keys())}, postgres-create")
        sys.exit(1)
