"""
init_repo.py - Configuration du dépôt personnel

Ce script aide les élèves à configurer leur propre dépôt Git après avoir
cloné le template du professeur.

Opérations effectuées :
1. Vérifie que le remote "template" existe (créé lors du clone)
2. Demande l'URL du dépôt personnel de l'élève
3. Ajoute ce dépôt comme nouveau remote "origin"
4. Pousse le code vers le nouveau dépôt

Prérequis :
- L'élève doit avoir créé un dépôt vide sur GitHub/GitLab
- Git doit être installé et configuré
"""

import subprocess
import sys
from utils import log_info, log_success, log_error, log_warning


def run_git(args: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    """Exécute une commande git."""
    cmd = ["git"] + args
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True)
    return subprocess.run(cmd)


def get_remotes() -> dict[str, str]:
    """Retourne un dictionnaire des remotes configurés."""
    result = run_git(["remote", "-v"], capture=True)
    remotes = {}
    for line in result.stdout.strip().split('\n'):
        if line and "(fetch)" in line:
            parts = line.split()
            if len(parts) >= 2:
                remotes[parts[0]] = parts[1]
    return remotes


def get_git_config(key: str) -> str:
    """Récupère une valeur de configuration git."""
    result = run_git(["config", "--get", key], capture=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def configure_git_user():
    """Configure l'identité git (user.name et user.email)."""

    current_name = get_git_config("user.name")
    current_email = get_git_config("user.email")

    print("📝 Configuration de votre identité Git")
    print("   (nécessaire pour signer vos commits)")
    print()

    # Nom d'utilisateur GitHub
    if current_name:
        print(f"   Nom actuel: {current_name}")
        name = input(f"   Nouveau nom GitHub (Entrée pour garder '{current_name}') : ").strip()
        if not name:
            name = current_name
    else:
        name = input("   Votre nom d'utilisateur GitHub : ").strip()

    if not name:
        log_error("Nom d'utilisateur requis.")
        return False

    # Email GitHub
    if current_email:
        print(f"   Email actuel: {current_email}")
        email = input(f"   Nouvel email (Entrée pour garder '{current_email}') : ").strip()
        if not email:
            email = current_email
    else:
        email = input("   Votre email GitHub : ").strip()

    if not email:
        log_error("Email requis.")
        return False

    # Appliquer la configuration
    run_git(["config", "user.name", name])
    run_git(["config", "user.email", email])

    log_success(f"Identité configurée: {name} <{email}>")
    return True


def show_prerequisites() -> bool:
    """
    Affiche les prérequis et demande confirmation avant de continuer.

    Returns:
        bool: True si l'utilisateur confirme avoir les prérequis
    """
    print("=" * 70)
    print("🚀 CONFIGURATION DU DÉPÔT PERSONNEL")
    print("=" * 70)
    print()
    print("📋 PRÉREQUIS")
    print("-" * 70)
    print()
    print("Avant de continuer, assurez-vous d'avoir :")
    print()
    print("   1. ✅ Un compte GitHub")
    print("      → Créez-en un sur https://github.com si ce n'est pas fait")
    print()
    print("   2. ✅ Un dépôt vide créé sur GitHub")
    print("      → Cliquez sur '+' puis 'New repository' sur GitHub")
    print("      → NE PAS cocher 'Add a README file'")
    print("      → NE PAS ajouter de .gitignore ou de licence")
    print()
    print("   3. ✅ L'URL de votre dépôt")
    print("      → Elle ressemble à : https://github.com/votre-nom/nom-du-repo.git")
    print("      → Vous la trouverez sur la page de votre dépôt (bouton 'Code')")
    print()
    print("-" * 70)
    print()

    reponse = input("Avez-vous ces prérequis ? (oui/non) : ").strip().lower()
    print()

    if reponse not in ("oui", "o", "yes", "y"):
        log_info("Configuration annulée.")
        print()
        log_info("Créez d'abord votre dépôt sur GitHub, puis relancez cette tâche.")
        return False

    return True


def init_personal_repo():
    """Configure le dépôt personnel de l'élève."""

    # Afficher les prérequis et demander confirmation
    if not show_prerequisites():
        return False

    # 1. Configurer l'identité git
    if not configure_git_user():
        return False
    print()

    remotes = get_remotes()
    log_info(f"Remotes actuels: {remotes if remotes else 'aucun'}")
    print()

    # Vérifier que "template" existe (créé lors du clone)
    if "template" in remotes:
        log_success("Remote 'template' configuré")
    else:
        log_warning("Remote 'template' non trouvé (le clone a-t-il été fait correctement ?)")

    # Vérifier si "origin" existe déjà
    if "origin" in remotes:
        log_warning(f"Un remote 'origin' existe déjà: {remotes['origin']}")
        reponse = input("Voulez-vous le remplacer ? (oui/non) : ").strip().lower()
        if reponse not in ("oui", "o", "yes", "y"):
            log_info("Configuration annulée.")
            return False
        run_git(["remote", "remove", "origin"])
        log_info("Ancien remote 'origin' supprimé")

    # Demander l'URL du dépôt personnel
    print()
    print("📝 Entrez l'URL de votre dépôt personnel.")
    print("   Exemple:")
    print("   - https://github.com/username/mon-projet.git")
    print()

    url = input("URL du dépôt : ").strip()

    if not url:
        log_error("URL vide, configuration annulée.")
        return False

    # Ajouter le remote origin
    log_info(f"Ajout du remote 'origin': {url}")
    result = run_git(["remote", "add", "origin", url], capture=True)

    if result.returncode != 0:
        log_error(f"Erreur lors de l'ajout du remote: {result.stderr}")
        return False

    log_success("Remote 'origin' ajouté avec succès")

    # Proposer de pousser vers le nouveau dépôt
    print()
    reponse = input("Voulez-vous pousser le code vers votre dépôt ? (oui/non) : ").strip().lower()

    if reponse in ("oui", "o", "yes", "y"):
        log_info("Push vers origin/main...")
        result = run_git(["push", "-u", "origin", "main"], capture=True)

        if result.returncode == 0:
            log_success("Code poussé avec succès vers votre dépôt !")
        else:
            log_error(f"Erreur lors du push: {result.stderr}")
            log_info("Vous pouvez réessayer manuellement avec: git push -u origin main")
            return False

    # Résumé final
    print()
    print("=" * 70)
    log_success("✨ CONFIGURATION TERMINÉE")
    print("=" * 70)

    remotes = get_remotes()
    print()
    log_info("Remotes configurés:")
    for name, url in remotes.items():
        print(f"   • {name}: {url}")

    print()
    log_info("Commandes utiles:")
    print("   • git push                    → Pousser vers votre dépôt")
    print("   • Task '🔄 Mise à jour...'    → Récupérer les mises à jour du prof")

    return True


if __name__ == "__main__":
    try:
        success = init_personal_repo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        log_error(f"Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
