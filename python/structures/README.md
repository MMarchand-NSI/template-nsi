# Les Packages Python

## Qu'est-ce qu'un package Python ?

Un **package Python** est un moyen d'organiser des modules Python en une hiérarchie de répertoires. C'est essentiellement un dossier contenant un fichier spécial `__init__.py` qui indique à Python que ce dossier doit être traité comme un package.

### Structure d'un package

```
structures/                 # Package principal
├── __init__.py            # Fichier d'initialisation du package
├── lineaires/             # Sous-package
│   └── __init__.py
├── hierarchiques/         # Sous-package
│   └── __init__.py
└── graphes/               # Sous-package
    └── __init__.py
```

Cette organisation permet de regrouper du code lié de manière logique et de créer des espaces de noms (namespaces) pour éviter les conflits de noms.

## La nécessité des fichiers `__init__.py`

Le fichier `__init__.py` joue plusieurs rôles essentiels :

### 1. **Marqueur de package**
La présence de `__init__.py` indique à Python qu'un répertoire doit être traité comme un package. Sans ce fichier, Python ne pourra pas importer le contenu du répertoire.

### 2. **Initialisation du package**
Le code dans `__init__.py` est exécuté lors du premier import du package. On peut y mettre :
- Des initialisations nécessaires au package
- Des imports pour simplifier l'API du package
- Des variables ou constantes du package

Exemple de `__init__.py` :
```python
# structures/__init__.py

# Exposer les sous-packages au niveau du package principal
from . import lineaires
from . import hierarchiques
from . import graphes

# Version du package
__version__ = "0.1.0"

# Liste de ce qui est exporté par défaut
__all__ = ["lineaires", "hierarchiques", "graphes"]
```

### 3. **Simplification des imports**
Le fichier `__init__.py` permet de rendre certains éléments directement accessibles :

```python
# structures/lineaires/__init__.py
from .pile import Pile
from .file import File

# Maintenant on peut faire :
# from structures.lineaires import Pile
# au lieu de :
# from structures.lineaires.pile import Pile
```

## Les imports relatifs à l'intérieur d'un package

Les **imports relatifs** permettent d'importer des modules depuis l'intérieur même du package, sans avoir à spécifier le chemin complet.

### Syntaxe des imports relatifs

- `.` : répertoire courant
- `..` : répertoire parent
- `...` : répertoire grand-parent

### Exemples

Supposons la structure suivante :
```
structures/
├── __init__.py
├── utils.py
└── lineaires/
    ├── __init__.py
    ├── pile.py
    └── file.py
```

Dans `pile.py`, on peut faire des imports relatifs :

```python
# structures/lineaires/pile.py

# Import depuis le même répertoire (lineaires/)
from .file import File

# Import depuis le package parent (structures/)
from ..utils import une_fonction

# Import absolu (équivalent, mais moins flexible)
from structures.utils import une_fonction
```

### Avantages des imports relatifs

1. **Portabilité** : Le package reste fonctionnel même si on le renomme
2. **Clarté** : On voit immédiatement la structure relative des modules
3. **Évite les conflits** : Pas de dépendance au nom global du package

### Limitations

- Les imports relatifs **ne fonctionnent que dans les packages**
- Ils ne peuvent pas être utilisés dans les scripts exécutés directement
- Ils nécessitent que le fichier `__init__.py` soit présent

## Configuration pour `import structures` n'importe où

Pour pouvoir faire `import structures` depuis n'importe quel fichier Python de votre projet, il faut configurer deux fichiers.

### 1. Configuration dans `pyproject.toml`

Le fichier `pyproject.toml` définit la structure de votre projet Python. Voici la configuration pertinente :

```toml
[tool.hatch.build.targets.wheel]
packages = ["python/structures"]
```

Cette ligne indique que le package `structures` se trouve dans le répertoire `python/structures`. Cela permet à Python de résoudre correctement les imports.

**Explication** :
- `packages` : liste des packages à inclure dans la distribution
- `"python/structures"` : chemin vers le package depuis la racine du projet
- Grâce à cette configuration, quand vous faites `import structures`, Python sait qu'il doit chercher dans `python/structures`

### 2. Configuration dans `.vscode/settings.json`

Pour que l'éditeur VS Code et les outils d'analyse (comme Pylance) comprennent où chercher les modules, on configure `python.analysis.extraPaths` :

```json
{
  "python.analysis.extraPaths": [
    "./python/projets/lsystems",
    "./python/projets/clientserveur"
  ]
}
```

**Note** : Dans ce projet, `python/structures` n'a pas besoin d'être dans `extraPaths` car il est déjà déclaré comme package dans `pyproject.toml`. La configuration `extraPaths` est surtout utile pour les répertoires qui ne sont pas des packages installés.

### Comment ça fonctionne ensemble ?

1. **Environnement virtuel** : Le projet utilise un environnement virtuel (`.venv`)
2. **Installation en mode développement** : Avec `uv` ou `pip install -e .`, le package est installé en mode "editable"
3. **Python trouve le package** : Grâce au `pyproject.toml`, Python ajoute automatiquement le chemin correct
4. **L'IDE comprend le code** : VS Code utilise `extraPaths` pour l'autocomplétion et la navigation

### Installation du package en mode développement

Pour que `import structures` fonctionne partout dans votre projet :

```bash
# Avec uv (recommandé)
uv pip install -e .

# Ou avec pip classique
pip install -e .
```

L'option `-e` (editable) permet de modifier le code source sans avoir à réinstaller le package à chaque fois.

## Résumé

| Concept | Rôle | Exemple |
|---------|------|---------|
| **Package** | Organiser le code en modules | `structures/` |
| **`__init__.py`** | Marquer un répertoire comme package | Présent dans chaque sous-dossier |
| **Import relatif** | Importer depuis l'intérieur du package | `from .pile import Pile` |
| **`pyproject.toml`** | Déclarer le package pour Python | `packages = ["python/structures"]` |
| **`settings.json`** | Aider l'IDE à comprendre la structure | `python.analysis.extraPaths` |

Cette organisation permet de créer du code réutilisable, maintenable et facilement partageable !
