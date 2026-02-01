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
from components_info import confirm_installation


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


def install_elm():
    """Installe nodejs et elm (via npm)"""
    if not confirm_installation("elm"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Node.js", apt_pkg="nodejs npm", yum_pkg="nodejs npm")
    print("✨ Installation d'Elm via npm...")
    executer("npm install -g elm", use_sudo=True)
    print("✅ Elm installé avec succès")


def install_rust():
    """Installe Rust via rustup"""
    if not confirm_installation("rust"):
        print("ℹ️  Installation annulée.")
        return

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
    if not confirm_installation("nasm"):
        print("ℹ️  Installation annulée.")
        return

    install_package("NASM + GDB", apt_pkg="nasm gdb", yum_pkg="nasm gdb")


def install_qemu():
    """Installe QEMU"""
    if not confirm_installation("qemu"):
        print("ℹ️  Installation annulée.")
        return

    install_package("QEMU", apt_pkg="qemu-system", yum_pkg="qemu")


def install_graphviz():
    """Installe Graphviz"""
    if not confirm_installation("graphviz"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Graphviz", apt_pkg="graphviz", yum_pkg="graphviz")


def install_postgresql():
    """Installe et initialise PostgreSQL"""
    if not confirm_installation("postgresql"):
        print("ℹ️  Installation annulée.")
        return

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
    # Vérifier si déjà démarré
    result = subprocess.run(
        "systemctl is-active postgresql",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout.strip() == "active":
        print("✅ Le serveur PostgreSQL est déjà démarré")
        return

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
        print(f"\nUsage: python installs_linux.py <composant|opération> [args]")
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
    elif choix in ALL_COMMANDS:
        try:
            if choix in INSTALLATIONS:
                pm = detect_package_manager()
                print(f"🐧 Système détecté: {pm}")
            ALL_COMMANDS[choix]()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    else:
        print(f"Option inconnue: {choix}")
        print(f"Installations disponibles: {', '.join(INSTALLATIONS.keys())}")
        print(f"Opérations disponibles: {', '.join(OPERATIONS.keys())}")
        sys.exit(1)
