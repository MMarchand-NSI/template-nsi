# Architecture des scripts `.vscode/`

Ce document décrit l'organisation et le fonctionnement des scripts de configuration du workspace VSCode pour le template NSI.

## Vue d'ensemble

```
.vscode/
├── Configuration VSCode
│   ├── settings.json           # Paramètres du workspace
│   └── tasks.json              # Définition des tâches (menu "Run Task")
│
├── Système d'installation (Multi-plateforme)
│   ├── install_wrapper.py      # Point d'entrée, détecte l'OS
│   ├── installs.py             # Windows (utilise MSYS2)
│   ├── installs_linux.py       # Linux (apt/yum/dnf)
│   ├── installs_macos.py       # macOS (Homebrew)
│   ├── msys2.py                # Gestion MSYS2 (Windows uniquement)
│   └── components_info.py      # Infos partagées sur les composants
│
├── Configuration & Mise à jour
│   ├── setup.py                # Vérification de l'environnement
│   ├── init_repo.py            # Configuration du dépôt Git personnel
│   └── update.py               # Mise à jour depuis le template distant
│
├── Sauvegarde USB
│   └── cleusb.py               # Sauvegarde/Import vers clé USB
│
├── Utilitaires
│   └── utils.py                # Fonctions de log (avec colorama)
│
└── Scripts initiaux (premier lancement)
    ├── setup-nsi.bat           # Windows
    ├── setup-nsi.sh            # Linux
    └── setup-nsi-macos.sh      # macOS
```

## Flux d'exécution

### Installation d'un composant

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ tasks.json  │────▶│ install_wrapper  │────▶│ installs_*.py   │
│ (UI VSCode) │     │ (détecte l'OS)   │     │ (selon l'OS)    │
└─────────────┘     └──────────────────┘     └─────────────────┘
                                                      │
                           ┌──────────────────────────┼──────────────────────────┐
                           ▼                          ▼                          ▼
                    ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
                    │ Windows     │           │ Linux       │           │ macOS       │
                    │ (MSYS2)     │           │ (apt/yum)   │           │ (Homebrew)  │
                    └─────────────┘           └─────────────┘           └─────────────┘
```

### Décorateurs MSYS2 (Windows)

```python
@msys2_required   # Vérifie que MSYS2 est installé (rapide)
@msys2_update     # Vérifie + met à jour MSYS2 (pour installations)
```

## Fichiers clés

### `components_info.py`

Module partagé contenant les descriptions de tous les composants installables.

```python
COMPONENT_INFO = {
    "nom_composant": {
        "description": "Description courte",
        "details": ["Point 1", "Point 2", "Point 3"],
        "size": "~XXX Mo"
    }
}
```

### `install_wrapper.py`

Point d'entrée unique pour toutes les installations. Détecte automatiquement l'OS et redirige vers le bon script.

### `utils.py`

Fonctions de logging avec support colorama :
- `log_info(message)` - Information (cyan)
- `log_success(message)` - Succès (vert)
- `log_warning(message)` - Avertissement (jaune)
- `log_error(message)` - Erreur (rouge)

---

## Exemple : Ajouter un nouveau composant

### Étape 1 : Ajouter les infos dans `components_info.py`

```python
COMPONENT_INFO = {
    # ... composants existants ...

    "nouveau_composant": {
        "description": "Mon Composant - Description courte",
        "details": [
            "Fonctionnalité 1",
            "Fonctionnalité 2",
            "Fonctionnalité 3"
        ],
        "size": "~100 Mo"
    }
}
```

### Étape 2 : Ajouter la fonction d'installation dans chaque fichier `installs_*.py`

**`installs.py` (Windows/MSYS2) :**

```python
@msys2_update
def install_nouveau_composant():
    """Installe nouveau_composant dans MSYS2"""
    if not confirm_installation("nouveau_composant"):
        utils.log_info("Installation annulée.")
        return

    msys2.executer("pacman -S --needed --noconfirm mingw-w64-ucrt-x86_64-nouveau_composant")
```

**`installs_linux.py` :**

```python
def install_nouveau_composant():
    """Installe nouveau_composant"""
    if not confirm_installation("nouveau_composant"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Nouveau Composant", apt_pkg="nouveau-composant", yum_pkg="nouveau-composant")
```

**`installs_macos.py` :**

```python
def install_nouveau_composant():
    """Installe nouveau_composant"""
    if not confirm_installation("nouveau_composant"):
        print("ℹ️  Installation annulée.")
        return

    install_package("Nouveau Composant", brew_pkg="nouveau-composant")
```

### Étape 3 : Enregistrer dans le dictionnaire `INSTALLATIONS`

Dans chaque fichier `installs_*.py`, ajouter au dictionnaire :

```python
INSTALLATIONS = {
    # ... existants ...
    "nouveau_composant": install_nouveau_composant
}
```

### Étape 4 : Ajouter l'option dans `tasks.json`

```json
{
    "id": "choixInstall",
    "type": "pickString",
    "options": [
        "msys2",
        "elm",
        "rust",
        "nasm",
        "qemu",
        "postgresql",
        "graphviz",
        "nouveau_composant"  // <-- Ajouter ici
    ]
}
```

---

## Conventions

| Convention | Description |
|------------|-------------|
| Noms de fonctions | `install_<composant>()` pour les installations |
| Décorateurs Windows | `@msys2_update` pour installations, `@msys2_required` pour opérations rapides |
| Confirmation | Toujours appeler `confirm_installation()` avant d'installer |
| Logs | Utiliser `utils.log_*()` ou `print()` avec emojis cohérents |
| Dictionnaires | `INSTALLATIONS` pour composants, `OPERATIONS` pour actions (start/stop) |

## Tests

Pour tester une installation manuellement :

```bash
# Via le wrapper (recommandé)
uv run python .vscode/install_wrapper.py nouveau_composant

# Directement (selon l'OS)
uv run python .vscode/installs.py nouveau_composant        # Windows
uv run python .vscode/installs_linux.py nouveau_composant  # Linux
uv run python .vscode/installs_macos.py nouveau_composant  # macOS
```
