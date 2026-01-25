# Installation du projet NSI

Ce guide explique comment installer automatiquement le projet NSI sur votre système sans avoir Git préalablement installé. Le script d'installation se chargera d'installer tous les outils nécessaires.

---

## Préparation (Tous systèmes)

**IMPORTANT** : Avant de lancer les commandes d'installation, vous devez :

1. **Ouvrir un terminal** (PowerShell sur Windows, Terminal sur Linux/macOS)
2. **Naviguer vers le répertoire** où vous souhaitez créer votre dossier de programmation

### Exemples de navigation

Sur **Windows** (PowerShell) :
```powershell
# Aller dans vos Documents
cd ~\Documents

# Ou créer un dossier dédié à la programmation
mkdir ~\Documents\Programmation
cd ~\Documents\Programmation
```

Sur **Linux/macOS** :
```bash
# Aller dans votre dossier personnel
cd ~

# Ou créer un dossier dédié à la programmation
mkdir ~/Programmation
cd ~/Programmation
```

Le script créera automatiquement un dossier `PROG-NSI` dans le répertoire où vous vous trouvez.

---

## Installation selon votre système

=== "Windows"

    ### Téléchargement et exécution

    Ouvrez **PowerShell** et exécutez les commandes suivantes :

    ```powershell
    # Télécharger le script d'installation
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/main/.vscode/setup-nsi.bat" -OutFile "setup-nsi.bat"

    # Exécuter le script
    .\setup-nsi.bat
    ```

    ### Alternative avec cmd

    Si vous préférez utiliser l'invite de commandes classique (cmd), vous pouvez utiliser `curl` (disponible depuis Windows 10) :

    ```cmd
    curl -o setup-nsi.bat https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/main/.vscode/setup-nsi.bat
    setup-nsi.bat
    ```

    ### Ce que fait le script

    Le script effectue automatiquement :

    1. Installation de **uv** (gestionnaire de paquets Python)
    2. Installation de **Git**
    3. Clonage du template dans le dossier `PROG-NSI`
    4. Configuration du remote Git
    5. Installation de **Visual Studio Code**
    6. Ouverture du projet dans VS Code

=== "Linux"

    ### Téléchargement et exécution

    Ouvrez un **terminal** et exécutez les commandes suivantes :

    ```bash
    # Télécharger le script d'installation
    curl -o setup-nsi.sh https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/main/.vscode/setup-nsi.sh

    # Rendre le script exécutable
    chmod +x setup-nsi.sh

    # Exécuter le script
    ./setup-nsi.sh
    ```

    ### Alternative avec wget

    Si `curl` n'est pas disponible, vous pouvez utiliser `wget` :

    ```bash
    # Télécharger le script d'installation
    wget -O setup-nsi.sh https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/main/.vscode/setup-nsi.sh

    # Rendre le script exécutable
    chmod +x setup-nsi.sh

    # Exécuter le script
    ./setup-nsi.sh
    ```

    ### Ce que fait le script

    Le script effectue automatiquement :

    1. Détection de votre distribution (Debian/Ubuntu ou Fedora/RHEL)
    2. Installation de **uv** (gestionnaire de paquets Python)
    3. Installation de **Git**
    4. Clonage du template dans le dossier `PROG-NSI`
    5. Configuration du remote Git
    6. Installation de **Visual Studio Code**
    7. Ouverture du projet dans VS Code

    **Note :** Le script vous demandera votre mot de passe utilisateur (sudo) pour installer les paquets système.

    **IMPORTANT** : Lorsque vous tapez votre mot de passe, **aucun caractère ne s'affichera à l'écran** (pas même des astérisques `***`). C'est un comportement normal de sécurité sous Linux. Tapez simplement votre mot de passe et appuyez sur Entrée.

=== "macOS"

    ### Téléchargement et exécution

    Ouvrez un **terminal** et exécutez les commandes suivantes :

    ```bash
    # Télécharger le script d'installation
    curl -o setup-nsi-macos.sh https://raw.githubusercontent.com/MMarchand-NSI/template-nsi/main/.vscode/setup-nsi-macos.sh

    # Rendre le script exécutable
    chmod +x setup-nsi-macos.sh

    # Exécuter le script
    ./setup-nsi-macos.sh
    ```

    ### Ce que fait le script

    Le script effectue automatiquement :

    1. Installation de **Homebrew** (gestionnaire de paquets macOS)
    2. Installation de **uv** (gestionnaire de paquets Python)
    3. Installation de **Git**
    4. Clonage du template dans le dossier `PROG-NSI`
    5. Configuration du remote Git
    6. Installation de **Visual Studio Code**
    7. Ouverture du projet dans VS Code

    **Note :** Le script s'adapte automatiquement à votre architecture (Apple Silicon M1/M2/M3 ou Intel).

---

## Après l'installation

Une fois le script terminé, VS Code s'ouvre automatiquement avec le projet `PROG-NSI`. Patientez, la configuration se fait automatiquement.

---

## Problèmes courants

### Le script ne se télécharge pas

Vérifiez votre connexion Internet et assurez-vous que vous avez accès à GitHub.

### Permission refusée (Linux/macOS)

Si vous obtenez "Permission denied", assurez-vous d'avoir rendu le script exécutable avec `chmod +x`.

### Le dossier PROG-NSI existe déjà

Le script s'arrête si le dossier existe déjà. Renommez ou supprimez le dossier existant avant de relancer le script.

### Git/VSCode ne s'ouvre pas après installation

Sur Windows, vous devrez peut-être redémarrer votre terminal après l'installation pour que les nouvelles commandes soient disponibles.
