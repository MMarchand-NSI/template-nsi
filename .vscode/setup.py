"""
setup.py - Script de vérification et configuration automatique de l'environnement

Ce script est exécuté automatiquement à chaque ouverture du workspace dans VSCode
via une task configurée dans tasks.json (runOn: "folderOpen").

Fonctionnalités :
-----------------
1. Vérification du fichier pyproject.toml
   - Vérifie la présence du fichier pyproject.toml à la racine du projet
   - Si absent, tente de le télécharger depuis l'URL de référence configurée

2. Gestion des extensions VSCode
   - Vérifie que toutes les extensions requises sont installées
   - Installe automatiquement les extensions manquantes
   - Liste des extensions dans REQUIRED_EXTENSIONS :
     * ms-python.python : Support Python
     * tomoki1207.pdf : Visualisation PDF
     * aaron-bond.better-comments : Amélioration des commentaires
     * fill-labs.dependi : Gestion des dépendances
     * sanaajani.taskrunnercode : UI pour les tasks
3. Configuration de l'environnement
   - Configure l'encodage UTF-8 pour Windows (stdout/stderr)
   - Affichage coloré avec emojis pour un meilleur feedback visuel

Résultat :
----------
- Code de retour 0 si tout est OK
- Code de retour 1 si des avertissements/erreurs sont détectés
- Affiche un résumé avec le statut de chaque vérification

Note :
------
Ce script peut également être exécuté manuellement via la task "Manual Setup Check"
pour forcer une vérification de l'environnement.
"""

import sys
import subprocess
import urllib.request
from pathlib import Path
import platform
import io
import utils


# Configuration de l'encodage UTF-8 pour Windows
if platform.system() == "Windows":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================================================
# CONFIGURATION
# ============================================================================

# URL du pyproject.toml de référence
PYPROJECT_URL = "https://raw.githubusercontent.com/votre-repo/config/main/pyproject.toml"

# Liste des extensions VSCode requises
REQUIRED_EXTENSIONS = [
    # Python
    "ms-python.python",
    # Pfd
    "tomoki1207.pdf",
    # Utilitaires
    "aaron-bond.better-comments",
    "fill-labs.dependi",
    "sanaajani.taskrunnercode",
    "tamasfe.even-better-toml"
]

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================


# ============================================================================
# GESTION DU PYPROJECT.TOML
# ============================================================================

def download_file(url: str, destination: Path) -> bool:
    """
    Télécharge un fichier depuis une URL.
    
    Args:
        url: URL du fichier à télécharger
        destination: Chemin de destination
    
    Returns:
        bool: True si le téléchargement a réussi
    """
    try:
        utils.log_info(f"Téléchargement depuis {url}...")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
        
        destination.write_bytes(data)
        utils.log_success(f"Fichier téléchargé: {destination.name}")
        return True
        
    except urllib.error.URLError as e:
        utils.log_error(f"Échec du téléchargement: {e.reason}")
        return False
    except Exception as e:
        utils.log_error(f"Erreur inattendue lors du téléchargement: {e}")
        return False

def check_pyproject_toml() -> bool:
    """
    Vérifie et télécharge si nécessaire le pyproject.toml.
    
    Returns:
        bool: True si le fichier existe ou a été téléchargé avec succès
    """
    pyproject_path = Path("pyproject.toml")
    
    if pyproject_path.exists():
        utils.log_success("pyproject.toml ✓")
        return True
    
    utils.log_warning("pyproject.toml manquant")
    utils.log_info("Téléchargement du pyproject.toml de référence...")
    
    return download_file(PYPROJECT_URL, pyproject_path)

# ============================================================================
# GESTION DES EXTENSIONS VSCODE
# ============================================================================

def get_vscode_command() -> str:
    """
    Retourne la commande appropriée pour VSCode selon le système d'exploitation.

    Returns:
        str: 'code.cmd' sur Windows, 'code' ailleurs
    """
    return "code.cmd" if platform.system() == "Windows" else "code"

def get_installed_extensions() -> set:
    """Retourne l'ensemble des extensions VSCode installées."""
    try:
        vscode_cmd = get_vscode_command()
        result = subprocess.run(
            [vscode_cmd, "--list-extensions"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return set(result.stdout.strip().split('\n'))
    except Exception:
        return set()

def install_extension(extension_id: str) -> bool:
    """
    Installe une extension VSCode.
    """
    try:
        vscode_cmd = get_vscode_command()
        subprocess.run(
            [vscode_cmd, "--install-extension", extension_id, "--force"],
            capture_output=True,
            check=True,
            timeout=120
        )
        return True
    except Exception:
        return False

def check_vscode_extensions() -> tuple[int, int, int]:
    """
    Vérifie et installe les extensions VSCode requises.
    """
    installed_extensions = get_installed_extensions()
    
    installed_count = 0
    present_count = 0
    failed_count = 0
    
    missing_extensions = [ext for ext in REQUIRED_EXTENSIONS if ext not in installed_extensions]
    
    if not missing_extensions:
        utils.log_success(f"Extensions VSCode ✓ ({len(REQUIRED_EXTENSIONS)} installées)")
        return (0, len(REQUIRED_EXTENSIONS), 0)
    
    utils.log_warning(f"{len(missing_extensions)} extension(s) manquante(s)")
    
    for extension in missing_extensions:
        utils.log_info(f"  Installation de {extension}...")
        if install_extension(extension):
            utils.log_success(f"    ✓ Installée")
            installed_count += 1
        else:
            utils.log_error(f"    ✗ Échec")
            failed_count += 1
    
    present_count = len(REQUIRED_EXTENSIONS) - len(missing_extensions)
    
    return (installed_count, present_count, failed_count)

# ============================================================================
# GESTION DES VARIABLES D'ENVIRONNEMENT
# ============================================================================

def check_set_env_var() -> bool:
    """
    Sous windows seulement, le PATH utilisateur doit avoir PATH_MSYS2\\ucrt64\\bin
    """
    if platform.system() != "Windows":
        return True

    import msys2
    from installs import get_env_var, set_env_var

    # Vérifier si MSYS2 est installé
    msys2_path = msys2.get_path()
    if not msys2_path.exists():
        # MSYS2 pas installé, pas de vérification nécessaire
        return True

    ucrt64_bin = str(msys2_path / "ucrt64" / "bin")
    current_path = get_env_var("Path")

    if ucrt64_bin.lower() in current_path.lower():
        utils.log_success(f"PATH contient {ucrt64_bin} ✓")
        return True

    # Ajouter au PATH
    utils.log_warning(f"{ucrt64_bin} manquant dans le PATH")
    utils.log_info("Ajout au PATH utilisateur...")
    new_path = f"{ucrt64_bin};{current_path}" if current_path else ucrt64_bin
    set_env_var("Path", new_path)
    utils.log_success(f"PATH mis à jour (redémarrage de VSCode recommandé)")
    return True


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale du setup."""
    print("=" * 70)
    print("🔍 VÉRIFICATION DE L'ENVIRONNEMENT")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 1. Vérifier pyproject.toml
    utils.log_info("1/3 Vérification de pyproject.toml...")
    try:
        if not check_pyproject_toml():
            all_ok = False
    except Exception as e:
        utils.log_error(f"Erreur: {e}")
        all_ok = False
    print()

    # 2. Vérifier les extensions VSCode
    utils.log_info("2/3 Vérification des extensions VSCode...")
    try:
        installed, present, failed = check_vscode_extensions()
        if failed > 0:
            all_ok = False
    except Exception as e:
        utils.log_error(f"Erreur: {e}")
        all_ok = False
    print()

    # 3. Vérifier les variables d'environnement (PATH MSYS2)
    utils.log_info("3/3 Vérification des variables d'environnement...")
    try:
        if not check_set_env_var():
            all_ok = False
    except Exception as e:
        utils.log_error(f"Erreur: {e}")
        all_ok = False
    print()
    
    # Résumé
    print("=" * 70)
    if all_ok:
        utils.log_success("✨ ENVIRONNEMENT PRÊT !")
    else:
        utils.log_warning("⚠️  ENVIRONNEMENT CONFIGURÉ AVEC AVERTISSEMENTS")
        utils.log_info("Certaines vérifications ont échoué, vérifiez les messages ci-dessus")
    print("=" * 70)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Vérification interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        utils.log_error(f"Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)