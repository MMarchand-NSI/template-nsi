# Elm

## Installation d'Elm

Pour installer Elm, utilisez la tâche VSCode prévue à cet effet :

1. Sélectionnez la tâche **🧩 Installer Composant**
2. Choisissez **elm** dans la liste

Cette tâche installera automatiquement Elm sur votre système.

## Initialisation d'un projet Elm

Une fois Elm installé, pour initialiser un nouveau projet :

```bash
elm init
```

Cette commande créera :
- Un fichier `elm.json` contenant la configuration du projet
- Un répertoire `src/` pour votre code source

## Compilation et exécution

Pour compiler un fichier Elm :

```bash
elm make src/Main.elm
```

Pour lancer le serveur de développement avec rechargement automatique :

```bash
elm reactor
```

Ouvrez ensuite votre navigateur à l'adresse `http://localhost:8000`
