"""
components_info.py - Informations sur les composants installables

Ce module centralise les descriptions et estimations de taille pour tous
les composants installables, partagées entre les scripts d'installation
de chaque plateforme.
"""

# Composants communs à toutes les plateformes
COMPONENT_INFO = {
    "elm": {
        "description": "Elm - Langage fonctionnel pour le développement web",
        "details": [
            "Node.js (runtime JavaScript)",
            "Compilateur Elm",
            "Elm REPL et outils de développement"
        ],
        "size": "~300 Mo"
    },
    "rust": {
        "description": "Rust - Langage système performant et sûr",
        "details": [
            "Compilateur rustc",
            "Gestionnaire de paquets Cargo",
            "Documentation et outils"
        ],
        "size": "~800 Mo"
    },
    "nasm": {
        "description": "NASM + GDB - Outils pour la programmation assembleur",
        "details": [
            "NASM (Netwide Assembler)",
            "GDB (GNU Debugger)"
        ],
        "size": "~100 Mo"
    },
    "qemu": {
        "description": "QEMU - Émulateur de machines virtuelles",
        "details": [
            "Émulation de processeurs (x86, ARM, etc.)",
            "Virtualisation matérielle",
            "Support de nombreux systèmes d'exploitation"
        ],
        "size": "~400 Mo"
    },
    "postgresql": {
        "description": "PostgreSQL - Système de gestion de base de données",
        "details": [
            "Serveur PostgreSQL",
            "Outils clients (psql, pg_dump, etc.)",
            "Configuration automatique avec utilisateur 'padawan'"
        ],
        "size": "~200 Mo"
    },
    "graphviz": {
        "description": "Graphviz - Outil de visualisation de graphes",
        "details": [
            "dot, neato, fdp, circo (moteurs de rendu)",
            "Génération d'images (PNG, SVG, PDF)",
            "Langage DOT pour décrire les graphes"
        ],
        "size": "~50 Mo"
    }
}

# Composant spécifique à Windows
MSYS2_INFO = {
    "msys2": {
        "description": "MSYS2 - Environnement de développement UNIX pour Windows",
        "details": [
            "Fournit un shell bash et des outils GNU",
            "Gestionnaire de paquets pacman",
            "Base pour installer les autres composants"
        ],
        "size": "~500 Mo"
    }
}


def get_component_info(component: str) -> dict | None:
    """
    Retourne les informations d'un composant.

    Args:
        component: Nom du composant

    Returns:
        Dictionnaire avec description, details et size, ou None si non trouvé
    """
    # Cherche d'abord dans les composants communs, puis dans MSYS2
    if component in COMPONENT_INFO:
        return COMPONENT_INFO[component]
    return MSYS2_INFO.get(component)


def confirm_installation(component: str) -> bool:
    """
    Affiche les informations sur le composant et demande confirmation.

    Args:
        component: Nom du composant à installer

    Returns:
        True si l'utilisateur confirme, False sinon
    """
    info = get_component_info(component)
    if not info:
        return True  # Pas d'info, on continue sans confirmation

    print()
    print("=" * 60)
    print(f"📦 {info['description']}")
    print("=" * 60)
    print()
    print("Ce qui sera installé :")
    for detail in info['details']:
        print(f"   • {detail}")
    print()
    print(f"💾 Espace disque estimé : {info['size']}")
    print()

    reponse = input("Voulez-vous continuer l'installation ? (oui/non) : ").strip().lower()
    print()

    return reponse in ("oui", "o", "yes", "y")
