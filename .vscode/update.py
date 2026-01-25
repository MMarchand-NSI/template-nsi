"""
TODO Revoir
Mise à jour des fichiers depuis le web
"""

import urllib.request
from pathlib import Path

# URL de base où se trouvent les fichiers à télécharger
BASE_URL = "https://raw.githubusercontent.com/votre-repo/config/main/.vscode"

def update_all_files():
    """
    Télécharge et remplace tous les fichiers .py de ce répertoire.
    Les fichiers sont téléchargés depuis BASE_URL avec le même nom.
    """
    # Récupération du répertoire courant (.vscode)
    vscode_dir = Path(__file__).parent

    # Liste de tous les fichiers .py du répertoire
    py_files = list(vscode_dir.glob("*.py"))

    if not py_files:
        print("Aucun fichier .py trouvé dans le répertoire.")
        return

    print(f"Mise à jour de {len(py_files)} fichier(s)...")
    print("-" * 50)

    success_count = 0
    failed_count = 0

    for py_file in py_files:
        filename = py_file.name
        url = f"{BASE_URL}/{filename}"

        print(f"Téléchargement de {filename}...", end=" ")

        try:
            # Téléchargement du fichier
            with urllib.request.urlopen(url, timeout=10) as response:
                data = response.read()

            # Sauvegarde du fichier
            py_file.write_bytes(data)
            print("✓")
            success_count += 1

        except urllib.error.HTTPError as e:
            print(f"✗ (Erreur HTTP {e.code})")
            failed_count += 1
        except urllib.error.URLError as e:
            print(f"✗ (Erreur réseau: {e.reason})")
            failed_count += 1
        except Exception as e:
            print(f"✗ (Erreur: {e})")
            failed_count += 1

    # Résumé
    print("-" * 50)
    print(f"Terminé: {success_count} réussi(s), {failed_count} échoué(s)")

    return failed_count == 0