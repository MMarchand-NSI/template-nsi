from pathlib import Path
import subprocess
import sys
import utils
import os


def installer():
    """Installe MSYS2 avec winget (--source winget) si nécessaire et si possible.
    Met à jour dans tous les cas"""

    if not utils.lycee() and not get_path().exists():
        try:
            subprocess.run(["winget", "install", "--source", "winget", "MSYS2.MSYS2"], check=True)
        except subprocess.CalledProcessError as e:
            utils.log_error(f"Erreur: {e}")

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
