"""
update.py - Mise à jour du dossier .vscode depuis le template distant

Ce module permet de synchroniser la configuration VSCode avec le template
du professeur sans toucher aux fichiers de travail de l'élève.
"""

import subprocess
from utils import log_info, log_success, log_error

REPO_URL = "https://github.com/MMarchand-NSI/template-nsi.git"


def update_from_template():
    """
    Met à jour le dossier .vscode depuis le template distant.

    Cette fonction effectue les opérations suivantes:
    1. Sauvegarde l'état actuel avec un commit "pre update" (si des changements existent)
    2. Récupère les dernières modifications du remote 'template' (git fetch template)
    3. Restaure le dossier .vscode depuis template/main

    Les fichiers de travail de l'élève (python/, web/, etc.) ne sont pas modifiés.

    Returns:
        bool: True si la mise à jour s'est bien déroulée, False en cas d'erreur
    """
    remote_name = "template"

    # Sauvegarder l'état actuel avant la mise à jour
    log_info("Sauvegarde de l'état actuel...")
    try:
        # Vérifier s'il y a des changements à commiter
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(
                ["git", "commit", "-m", "pre update config "],
                check=True
            )
            log_success("État sauvegardé (commit 'pre update')")
        else:
            log_info("Aucun changement à sauvegarder")
    except subprocess.CalledProcessError as e:
        log_error(f"Erreur lors de la sauvegarde: {e}")
        return False

    # Récupérer les dernières modifications du template
    log_info(f"Récupération des modifications depuis {remote_name}...")
    try:
        subprocess.run(
            ["git", "fetch", remote_name],
            check=True
        )
        log_success("Modifications récupérées")
    except subprocess.CalledProcessError as e:
        log_error(f"Erreur lors du fetch: {e}")
        return False

    # Mise à jour du dossier .vscode uniquement
    log_info("Mise à jour du dossier .vscode...")
    try:
        subprocess.run(
            ["git", "restore", "--source", f"{remote_name}/main", "--staged", "--worktree", ".vscode/"],
            check=True
        )
        log_success("Dossier .vscode mis à jour depuis le template")
    except subprocess.CalledProcessError as e:
        log_error(f"Erreur lors de la mise à jour: {e}")
        return False

    return True


if __name__ == "__main__":
    import sys
    success = update_from_template()
    sys.exit(0 if success else 1)