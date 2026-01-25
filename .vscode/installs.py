"""
installs.py - Gestionnaire d'installation de composants pour l'environnement MSYS2

Ce script facilite l'installation et la configuration de différents outils de développement
dans l'environnement MSYS2 sous Windows. Il peut être exécuté via la ligne de commande
ou via la task VSCode "Installer Composant".

Architecture :
--------------
Le script distingue deux environnements possibles :
- Lycée : MSYS2 installé dans C:/Programmes_Portables/MSYS2_FR_1500
- Personnel : MSYS2 installé dans C:/msys64

Composants installables :
--------------------------
- msys2       : Installation de MSYS2 via winget (environnement personnel uniquement)
- elm         : Node.js + Elm (langage de programmation fonctionnel pour le web)
- rust        : Compilateur Rust et Cargo
- nasm        : Assembleur NASM + GDB (débogueur)
- qemu        : Émulateur de machines virtuelles
- postgresql  : Serveur de base de données PostgreSQL (avec initialisation automatique)

Fonctions principales :
-----------------------
msys2.executer(cmd: str)
    Exécute une commande dans l'environnement MSYS2 UCRT64.
    Affiche la sortie en temps réel caractère par caractère pour les barres de progression.

get_msys2_path() -> Path
    Retourne le chemin d'installation de MSYS2 selon l'environnement (lycée/perso).

get_database_dir() -> str
    Retourne le chemin du répertoire DATABASE dans le home Windows au format MSYS2.

set_env_var(var: str, val: str)
    Définit une variable d'environnement de manière persistante via le registre Windows.

postgres_init()
    Initialise PostgreSQL avec un superuser "padawan" et encodage UTF-8 français.

Utilisation en ligne de commande :
-----------------------------------
    python installs.py <composant>

Exemples :
    python installs.py rust
    python installs.py postgresql

Utilisation via VSCode :
-------------------------
Lancer la task "Installer Composant" qui présente un menu de sélection.

Note technique :
----------------
Les commandes sont exécutées dans l'environnement MSYS2 UCRT64, qui offre
une compatibilité native avec les outils Windows tout en fournissant un
environnement POSIX complet.
"""

import subprocess
import sys
import os
import msys2
import utils

if sys.platform == "win32":
    import winreg

def set_env_var(var: str, val: str):
    """
    Met de manière persistante la variable d'environnement var à val
    """

    # Ouverture de la clé de registre pour les variables d'environnement utilisateur
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Environment',
        0,
        winreg.KEY_ALL_ACCESS
    )

    try:
        # Définition de la variable d'environnement
        winreg.SetValueEx(key, var, 0, winreg.REG_EXPAND_SZ, val)
        print(f"Variable d'environnement {var} définie à: {val}")

        # Notification du système que les variables d'environnement ont changé
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            'Environment',
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(result)
        )
    finally:
        winreg.CloseKey(key)


def install_msys2():
    """Installe MSYS2 avec winget (--source winget) si nécessaire et si possible.
    Met à jour dans tous les cas"""

    msys2.installer()


def install_elm():
    """Installe nodejs et elm (via npm) dans msys2"""
    msys2.executer("pacman -S --noconfirm mingw-w64-ucrt-x86_64-nodejs")
    msys2.executer("npm install -g elm")


def install_rust():
    """
    Installe Rust dans msys2
    """
    msys2.executer("pacman -S --noconfirm mingw-w64-ucrt-x86_64-rust")


def install_nasm():
    """
    Installe nasm dans msys2
    """
    msys2.executer("pacman -S --noconfirm mingw-w64-ucrt-x86_64-nasm mingw-w64-ucrt-x86_64-gdb")

def install_qemu():
    """
    Installe nasm dans msys2
    """
    msys2.executer("pacman -S --noconfirm mingw-w64-ucrt-x86_64-qemu")


def install_postgresql():
    """
    Installe et initialise postgresql
    """
    msys2.executer("pacman -S --noconfirm mingw-w64-ucrt-x86_64-postgresql")
    postgres_init()


def get_database_dir():
    home_windows = os.environ['USERPROFILE']

    # Conversion du chemin Windows vers le format MSYS2 avec cygpath
    database_msys2 = f"$(cygpath -u '{home_windows}')/DATABASE"
    return database_msys2

def postgres_init():
    """
    Initialise postgresql en UTF-8 français dans le home utilisateur/DATABASE
    le superuser est padawan et le mot de passe aussi
    """
    database_msys2 = get_database_dir()

    # Création du répertoire pour la base de données
    msys2.executer(f"mkdir -p {database_msys2}")

    # Création d'un fichier temporaire avec le mot de passe
    msys2.executer("echo 'padawan' > /tmp/pwfile")

    # Initialisation de la base de données PostgreSQL
    msys2.executer(f"initdb -D {database_msys2} -U padawan --locale=fr_FR.UTF-8 --encoding=UTF8 --pwfile=/tmp/pwfile")

    # Suppression du fichier de mot de passe temporaire
    msys2.executer("rm /tmp/pwfile")


def postgres_start():
    """Démarre l'instance PostgreSQL"""
    database_msys2 = get_database_dir()

    # Vérification du statut avant de démarrer
    try:
        msys2.executer(f"pg_ctl -D {database_msys2} status")
        # Si on arrive ici, le serveur tourne déjà
        utils.log_info("Le serveur PostgreSQL est déjà démarré")
        return
    except subprocess.CalledProcessError:
        # Le serveur n'est pas démarré, on continue
        pass

    # Démarrage du serveur (option -W pour ne pas attendre, mais test sans)
    msys2.executer(f"pg_ctl -D {database_msys2} -l {database_msys2}/logfile start")
    utils.log_success("Serveur PostgreSQL démarré")


def postgres_stop():
    """Arrête l'instance PostgreSQL"""
    database_msys2 = get_database_dir()
    msys2.executer(f"pg_ctl -D {database_msys2} -l {database_msys2}/logfile stop")
    utils.log_success("Serveur PostgreSQL arrêté")


def postgres_create_db(nom: str):
    """Crée une base de données PostgreSQL"""
    msys2.executer(f"createdb -U padawan -E UTF8 {nom}")
    utils.log_success(f"Base de données '{nom}' créée")


# Dictionnaire des fonctions d'installation et opérations
INSTALLATIONS = {
    "msys2": install_msys2,
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
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: python installs.py [{' | '.join(INSTALLATIONS.keys())} | postgres-create <nom>]")
        sys.exit(1)

    choix = sys.argv[1].lower()

    if choix == "postgres-create":
        if len(sys.argv) < 3:
            print("Usage: python installs.py postgres-create <nom>")
            sys.exit(1)
        postgres_create_db(sys.argv[2])
    elif choix in INSTALLATIONS:
        INSTALLATIONS[choix]()
    else:
        print(f"Option inconnue: {choix}")
        print(f"Options disponibles: {', '.join(INSTALLATIONS.keys())}, postgres-create")
        sys.exit(1)