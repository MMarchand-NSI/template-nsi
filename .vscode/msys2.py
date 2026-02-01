"""
msys2.py - Gestionnaire MSYS2 pour Windows

Ce module fournit des fonctions pour installer, configurer et utiliser MSYS2.

Deux décorateurs sont disponibles :

@msys2_required - Vérifie simplement que MSYS2 est installé (pour les opérations rapides)
@msys2_update   - Vérifie + met à jour MSYS2 (pour les installations de composants)

Exemples:
    from msys2 import msys2_required, msys2_update

    @msys2_required
    def postgres_start():
        # Opération rapide, pas besoin de mise à jour
        ...

    @msys2_update
    def install_rust():
        # Installation, on veut s'assurer que MSYS2 est à jour
        msys2.executer("pacman -S --needed --noconfirm mingw-w64-ucrt-x86_64-rust")
"""

from pathlib import Path
import subprocess
import sys
import utils
import os
from functools import wraps


def _check_msys2_installed(func_name: str) -> bool:
    """
    Vérifie si MSYS2 est installé.

    Args:
        func_name: Nom de la fonction appelante (pour le message d'erreur)

    Returns:
        True si MSYS2 est installé, False sinon
    """
    if not get_path().exists():
        utils.log_error(f"MSYS2 n'est pas installé. La fonction '{func_name}' nécessite MSYS2.")
        utils.log_info("Installez MSYS2 en exécutant la tâche '🧩 Installer Composant' et en choisissant 'msys2'")
        return False
    return True


def msys2_required(func):
    """
    Décorateur pour les fonctions nécessitant MSYS2.
    Vérifie que MSYS2 est installé avant d'exécuter la fonction.
    Ne met PAS à jour MSYS2 (utilisez @msys2_update pour cela).

    Usage:
        @msys2_required
        def postgres_start():
            # opération rapide
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not _check_msys2_installed(func.__name__):
            return None
        return func(*args, **kwargs)
    return wrapper


def msys2_update(func):
    """
    Décorateur pour les fonctions d'installation nécessitant MSYS2.
    Vérifie que MSYS2 est installé ET met à jour MSYS2 avant d'exécuter la fonction.

    Usage:
        @msys2_update
        def install_rust():
            msys2.executer("pacman -S ...")
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not _check_msys2_installed(func.__name__):
            return None
        utils.log_info("Mise à jour de MSYS2...")
        mettre_a_jour()
        utils.log_info("Fin de mise à jour")
        return func(*args, **kwargs)
    return wrapper


def ouvrir_terminal_ucrt64():
    """
    Ouvre un terminal UCRT64 pour initialiser la configuration MSYS2.
    Le terminal s'ouvre brièvement pour permettre l'initialisation.
    """
    if not get_path().exists():
        return

    msys2_path = get_path()
    ucrt64_exe = msys2_path / "msys2_shell.cmd"

    if not ucrt64_exe.exists():
        utils.log_error("msys2_shell.cmd introuvable")
        return

    try:
        utils.log_info("Initialisation du terminal UCRT64...")
        # Lance le shell UCRT64 pour initialisation
        # -ucrt64 : utilise l'environnement UCRT64
        # -defterm : utilise le terminal par défaut (conhost)
        # -here : démarre dans le répertoire courant
        # -c "echo 'Initialisation...' && sleep 1" : commande simple qui se termine
        subprocess.run(
            [str(ucrt64_exe), "-ucrt64", "-defterm", "-here", "-c", "echo 'MSYS2 UCRT64 initialisé' && sleep 1"],
            check=True
        )
        utils.log_success("Terminal UCRT64 initialisé")
    except subprocess.CalledProcessError as e:
        utils.log_error(f"Erreur lors de l'initialisation du terminal: {e}")


def installer():
    """Installe MSYS2 avec winget (--source winget) si nécessaire et si possible.
    Met à jour dans tous les cas"""

    if not utils.lycee() and not get_path().exists():
        try:
            subprocess.run(["winget", "install", "--source", "winget", "MSYS2.MSYS2"], check=True)
        except subprocess.CalledProcessError as e:
            utils.log_error(f"Erreur: {e}")

    # Ouvre un terminal UCRT64 pour que le terminal se configure tout seul
    ouvrir_terminal_ucrt64()
    add_usrt64_2_path()

    if get_path().exists():
        mettre_a_jour()
    else:
        utils.log_error("Attention, MSYS2 n'a pas été installé sur cette machine")

def get_path():
    """
    Si on est au lycée, le root MSYS2 est  C:/Programmes_Portables/MSYS2_FR_1500
    Sinon on est chez soi et le root MSYS2 est C:/msys64
    Ne s'applique que si on est sous windows.
    """
    if sys.platform != "win32":
        raise RuntimeError("Cette fonction ne s'applique que sous Windows")

    if utils.lycee():
        return Path(r"C:\Programmes_Portables\MSYS2_FR_1500")
    else:
        return Path(r"C:\msys64")


def add_usrt64_2_path():
    """
    ajoute le répertoire ucrt64/bin au path windows utilisateur.
    """
    if sys.platform != "win32":
        raise RuntimeError("Cette fonction ne s'applique que sous Windows")

    # Vérifier que MSYS2 est installé
    if not get_path().exists():
        utils.log_error("MSYS2 n'est pas installé. Impossible d'ajouter ucrt64/bin au PATH.")
        return

    # Import local pour éviter l'import circulaire
    from installs import get_env_var, set_env_var

    # Récupération du PATH actuel
    current_path = get_env_var("Path")

    # Construction du chemin ucrt64/bin
    msys2_path = get_path()
    ucrt64_bin = str(msys2_path / "ucrt64" / "bin")

    # Vérification si déjà présent dans le PATH
    if ucrt64_bin in current_path:
        utils.log_success(f"{ucrt64_bin} est déjà dans le PATH")
        return

    # Ajout au PATH (au début pour priorité)
    new_path = f"{ucrt64_bin};{current_path}" if current_path else ucrt64_bin

    # Mise à jour persistante via set_env_var
    set_env_var("Path", new_path)
    utils.log_success(f"Ajouté {ucrt64_bin} au PATH utilisateur")

@msys2_required
def executer(cmd: str):
    """
    Exécute une commande dans msys2 ucrt64.
    Affiche la progression en temps réel grâce à la lecture caractère par caractère
    """
    msys2_path = get_path()
    bash_exe = msys2_path / "usr" / "bin" / "bash.exe"
    
    # Injection de variable d'envt
    env = os.environ.copy()
    env['MSYSTEM'] = 'UCRT64'
    
    cmd = [
        str(bash_exe),
        "-lc",
        cmd
    ]
    
    process = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=0  #! pas de buffering
    )
    
    # Lecture caractère par caractère
    while True:
        char = process.stdout.read(1)
        if not char:
            if process.poll() is not None:
                break
            continue
        
        # Affiche immédiatement (garde les \r pour les progress bars)
        sys.stdout.write(char.decode('utf-8', errors='replace'))
        sys.stdout.flush()
    
    rc = process.poll()
    if rc != 0:
        raise subprocess.CalledProcessError(rc, cmd)
    
    return rc



def mettre_a_jour():
    """Met à jour MSYS2 via pacman -Syu --no-confirm
    Le faire 2 fois en cas de core upgrade pour full upgrade
    """
    executer("pacman -Syu --noconfirm")
    executer("pacman -Syu --noconfirm")
