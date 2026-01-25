"""Script pour exécuter la fonction import_cle_vers_vscode"""
import sys
from cleusb import import_cle_vers_vscode

if __name__ == "__main__":
    try:
        # Demande de confirmation
        print("⚠️  ATTENTION ⚠️")
        print("Les données de votre répertoire VSCode vont être écrasées.")
        print("Tous les dossiers existants seront remplacés par ceux de la clé USB.")
        print()
        reponse = input("Êtes-vous sûr de vouloir continuer ? (oui/non) : ").strip().lower()

        if reponse not in ['oui', 'o', 'yes', 'y']:
            print("Import annulé.")
            sys.exit(0)

        print()
        import_cle_vers_vscode()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
