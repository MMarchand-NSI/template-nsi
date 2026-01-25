"""Script pour exécuter la fonction sauvegarde"""
import sys
from cleusb import sauvegarde

if __name__ == "__main__":
    try:
        # Demande de confirmation
        print("⚠️  ATTENTION ⚠️")
        print("Les données de votre clé USB vont être écrasées.")
        print("Tous les dossiers existants dans PROG_NSI seront remplacés.")
        print()
        reponse = input("Êtes-vous sûr de vouloir continuer ? (oui/non) : ").strip().lower()

        if reponse not in ['oui', 'o', 'yes', 'y']:
            print("Sauvegarde annulée.")
            sys.exit(0)

        print()
        sauvegarde()
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
