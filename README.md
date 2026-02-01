# Guide de l'élève - Template NSI

Bienvenue ! Ce guide t'explique comment utiliser ce projet pour tes cours de NSI.

---

## Première installation

### 1. Récupérer le script d'installation

Télécharge le fichier correspondant à ton système avec cette commande dans un terminal :

**Windows** (PowerShell) :
```powershell
curl -o setup-nsi.bat https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/refs/heads/main/.vscode/setup-nsi.bat
```

**Linux** :
```bash
curl -o setup-nsi.sh https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/refs/heads/main/.vscode/setup-nsi.sh
```

**macOS** :
```bash
curl -o setup-nsi-macos.sh https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/refs/heads/main/.vscode/setup-nsi-macos.sh
```

### 2. Lancer le script

#### Windows
Double-clique sur `setup-nsi.bat`

#### Linux / macOS
Ouvre un terminal dans le dossier où se trouve le script et tape :
```bash
# Linux
chmod +x setup-nsi.sh && ./setup-nsi.sh

# macOS
chmod +x setup-nsi-macos.sh && ./setup-nsi-macos.sh
```

### 3. C'est tout !

Le script fait tout automatiquement :
1. Installe `uv` (gestionnaire Python)
2. Installe `git`
3. Clone le projet dans un dossier `PROG-NSI`
4. Installe VSCode (si nécessaire)
5. Ouvre VSCode dans le projet

**Attends que VSCode affiche "ENVIRONNEMENT PRÊT"** dans le terminal.

---

## Utilisation quotidienne

### Ouvrir ton projet

1. Lance VSCode
2. **Fichier → Ouvrir le dossier** → sélectionne `PROG-NSI`

Ou en ligne de commande :
```bash
code PROG-NSI
```

### Lancer les tâches

Accède aux tâches via : **Terminal → Exécuter la tâche**

| Tâche | Quand l'utiliser |
|-------|------------------|
| ♻️ **uv sync** | Si tu as des erreurs "module not found" |
| 🛠️ **Setup Environment NSI** | Pour vérifier que tout est bien configuré |
| 🔄 **Mise à jour depuis le template** | Quand le prof annonce des nouveaux fichiers |

---

## Sauvegarder ton travail

### Option A : Sur clé USB (au lycée)

| Tâche | Action |
|-------|--------|
| 💻 ⟶ 🔑 **Sauvegarde USB** | Copie ton projet vers la clé |
| 🔑 ⟶ 💻 **Import depuis USB** | Restaure depuis la clé |

> ⚠️ Ces opérations **écrasent** les fichiers existants !

### Option B : Avec GitHub (recommandé)

#### Première fois : créer ton dépôt personnel

1. Crée un compte sur [github.com](https://github.com)
2. Crée un **nouveau dépôt vide** :
   - Clique sur **+** puis **New repository**
   - **NE PAS** cocher "Add a README file"
   - **NE PAS** ajouter de .gitignore
3. Lance la tâche : **🔗 Configurer mon dépôt personnel**
4. Colle l'URL de ton dépôt quand demandé

#### Ensuite : sauvegarder régulièrement

Dans le terminal VSCode (`Ctrl+ù`) :
```bash
git add .
git commit -m "Mon travail du jour"
git push
```

Ou utilise l'onglet **Contrôle de code source** (icône avec 3 branches à gauche).

---

## Recevoir les mises à jour du prof

Quand ton professeur ajoute de nouveaux exercices :

1. Lance : **🔄 Mise à jour depuis le template**
2. Tes fichiers sont mis à jour
3. Tes propres ajouts (dépendances, etc.) sont préservés

---

## Installer des outils supplémentaires

Certains cours nécessitent des outils en plus.

Lance : **🧩 Installer Composant**

| Composant | Description |
|-----------|-------------|
| `elm` | Langage fonctionnel pour le web |
| `rust` | Langage système performant |
| `nasm` | Assembleur + débogueur |
| `qemu` | Émulateur de machines virtuelles |
| `postgresql` | Base de données |
| `graphviz` | Visualisation de graphes |

> **Windows** : `msys2` doit être installé en premier pour les autres composants.

### PostgreSQL

Lance la tâche **🐘 PostgreSQL** puis choisis :
- `postgres-start` pour démarrer le serveur
- `postgres-stop` pour l'arrêter

---

## Structure du projet

```
PROG-NSI/
├── python/
│   ├── exos/           ← Tes exercices Python
│   ├── projets/        ← Tes projets
│   └── structures/     ← Structures de données
│
├── web/                ← Projets HTML/CSS/JS
├── elm/                ← Projets Elm
│
├── pyproject.toml      ← Configuration Python
└── .vscode/            ← Configuration (ne pas toucher !)
```

---

## Problèmes fréquents

| Problème | Solution |
|----------|----------|
| "Module not found" | Lance ♻️ **uv sync** |
| Les tests ne marchent pas | `uv run pytest` dans le terminal |
| Je ne trouve pas les tâches | `Ctrl+Shift+P` → "Tasks: Run Task" |
| Git demande un mot de passe | `git config --global credential.helper store` |
| Mise à jour échoue | Vérifie avec `git remote -v` que "template" existe |

---

## Raccourcis utiles

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Shift+P` | Palette de commandes |
| `Ctrl+ù` | Terminal |
| `Ctrl+Shift+E` | Explorateur |
| `Ctrl+Shift+G` | Git |
| `F5` | Déboguer |

---

