"""
update.py - Mise à jour des fichiers depuis le template distant

Ce module permet de synchroniser le projet avec le template du professeur
tout en préservant les dépendances personnelles ajoutées par l'élève.
"""

import subprocess
import tomllib
from pathlib import Path
from utils import log_info, log_success, log_error

# Ce repo contient le template que constitue ce projet
# Les personnes ont fait
#      - git clone https://github.com/MMarchand-NSI/template-nsi.git monrepertoire
#      - cd mon-projet
#      - git remote rename origin template

REPO_URL = "https://github.com/MMarchand-NSI/template-nsi.git"


def update_from_template():
    """
    Met à jour tous les fichiers et répertoires d'après le template distant.

    Cette fonction effectue les opérations suivantes:
    1. Sauvegarde les dépendances actuelles du pyproject.toml
    2. Récupère les dernières modifications du remote 'template' (git fetch template)
    3. Liste tous les fichiers présents dans template/main
    4. Écrase tous les fichiers locaux avec ceux du template (git checkout template/main -- ...)
    5. Réinjecte les dépendances personnelles qui n'étaient pas dans le template avec 'uv add'

    Cette approche permet de synchroniser complètement avec le template tout en
    préservant les dépendances personnelles ajoutées au projet.

    Returns:
        bool: True si la mise à jour s'est bien déroulée, False en cas d'erreur
    """
    remote_name = "template"
    pyproject_path = Path("pyproject.toml")

    # Sauvegarder les dépendances actuelles si pyproject.toml existe
    saved_dependencies = []

    if pyproject_path.exists():
        log_info("Sauvegarde des dépendances actuelles...")
        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                saved_dependencies = data.get("project", {}).get("dependencies", [])
                log_info(f"{len(saved_dependencies)} dépendances sauvegardées")
        except Exception as e:
            log_error(f"Erreur lors de la lecture de pyproject.toml: {e}")
            # On continue quand même

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

    # Récupérer la liste de tous les fichiers du template
    log_info("Récupération de la liste des fichiers du template...")
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", f"{remote_name}/main"],
            capture_output=True,
            text=True,
            check=True
        )
        files_to_update = result.stdout.strip().split('\n')
        files_to_update = [f for f in files_to_update if f]  # Enlever les lignes vides
        log_info(f"{len(files_to_update)} fichiers à mettre à jour")
    except subprocess.CalledProcessError as e:
        log_error(f"Erreur lors de la récupération de la liste des fichiers: {e}")
        return False

    # Mise à jour de tous les fichiers du template (écrasement)
    log_info("Écrasement des fichiers avec ceux du template...")
    try:
        subprocess.run(
            ["git", "checkout", f"{remote_name}/main", "--"] + files_to_update,
            check=True
        )
        log_success(f"Tous les fichiers ({len(files_to_update)}) ont été écrasés depuis le template")
    except subprocess.CalledProcessError as e:
        log_error(f"Erreur lors de la mise à jour: {e}")
        return False

    # Réinjecter les dépendances sauvegardées
    if saved_dependencies:
        log_info("Réinjection des dépendances personnelles...")

        # Lire les nouvelles dépendances du template
        try:
            with open(pyproject_path, "rb") as f:
                new_data = tomllib.load(f)
                template_dependencies = set(new_data.get("project", {}).get("dependencies", []))
        except Exception as e:
            log_error(f"Erreur lors de la lecture du nouveau pyproject.toml: {e}")
            return False

        # Trouver les dépendances à ajouter (celles qui étaient dans l'ancien mais pas dans le nouveau)
        deps_to_add = [d for d in saved_dependencies if d not in template_dependencies]

        # Ajouter les dépendances avec uv
        if deps_to_add:
            log_info(f"Ajout de {len(deps_to_add)} dépendances personnelles...")
            try:
                subprocess.run(
                    ["uv", "add"] + deps_to_add,
                    check=True
                )
                log_success("Dépendances personnelles réinjectées")
            except subprocess.CalledProcessError as e:
                log_error(f"Erreur lors de l'ajout des dépendances: {e}")

    return True


if __name__ == "__main__":
    import sys
    success = update_from_template()
    sys.exit(0 if success else 1)