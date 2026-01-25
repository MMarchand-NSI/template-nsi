#!/usr/bin/env bash

# ============================================================================
# Script d'installation et configuration d'un projet NSI (Linux)
# ============================================================================
# Ce script :
# 1. Installe uv (gestionnaire de paquets Python)
# 2. Installe git
# 3. Clone le template https://github.com/MMarchand-NSI/template-nsi.git depuis GitHub dans le répertoire PROG-NSI (pas de choix de nom)
# 4. Configure le remote "template" pour les futures mises à jour
# 5. Installe VSCode
# 6. Ouvre vscode dans le répertoire cloné
# ============================================================================

set -e  # Arrêter en cas d'erreur

echo ""
echo "========================================"
echo "Installation NSI (Linux)"
echo "========================================"
echo ""

# Nom fixe du répertoire du projet
PROJET_DIR="PROG-NSI"

# Vérifier si le répertoire existe déjà
if [ -d "$PROJET_DIR" ]; then
    echo "Erreur: Le répertoire '$PROJET_DIR' existe déjà"
    echo "Veuillez le supprimer ou le renommer avant de continuer"
    exit 1
fi

# Détecter la distribution Linux
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)

# Déterminer le gestionnaire de paquets
if [[ "$DISTRO" == "ubuntu" ]] || [[ "$DISTRO" == "debian" ]] || [[ "$DISTRO" == "linuxmint" ]] || [[ "$DISTRO" == "pop" ]]; then
    PKG_MANAGER="apt"
    PKG_UPDATE="sudo apt update"
    PKG_INSTALL="sudo apt install -y"
elif [[ "$DISTRO" == "fedora" ]] || [[ "$DISTRO" == "rhel" ]] || [[ "$DISTRO" == "centos" ]] || [[ "$DISTRO" == "rocky" ]]; then
    PKG_MANAGER="dnf"
    PKG_UPDATE="sudo dnf check-update || true"
    PKG_INSTALL="sudo dnf install -y"
else
    echo "Distribution non reconnue: $DISTRO"
    echo "Ce script supporte Debian/Ubuntu (apt), Fedora/RHEL (dnf) et dérivées"
    exit 1
fi

echo "Distribution détectée: $DISTRO (gestionnaire de paquets: $PKG_MANAGER)"
echo ""

echo "========================================"
echo "Etape 1/6 : Installation de uv"
echo "========================================"
echo ""

# Vérifier si uv est déjà installé
if command -v uv &> /dev/null; then
    echo "uv est déjà installé"
    uv --version
else
    echo "Installation de uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Ajouter uv au PATH pour cette session
    export PATH="$HOME/.local/bin:$PATH"

    if command -v uv &> /dev/null; then
        echo "uv installé avec succès"
    else
        echo "Erreur lors de l'installation de uv"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Etape 2/6 : Installation de Git"
echo "========================================"
echo ""

# Vérifier si git est déjà installé
if command -v git &> /dev/null; then
    echo "Git est déjà installé"
    git --version
else
    echo "Installation de Git via $PKG_MANAGER..."
    $PKG_UPDATE
    $PKG_INSTALL git

    if command -v git &> /dev/null; then
        echo "Git installé avec succès"
    else
        echo "Erreur lors de l'installation de Git"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Etape 3/6 : Clonage du template NSI"
echo "========================================"
echo ""

# Cloner le repository dans PROG-NSI
echo "Clonage du template dans le répertoire '$PROJET_DIR'..."
git clone https://github.com/MMarchand-NSI/template-nsi.git "$PROJET_DIR"

echo "Template cloné avec succès"

echo ""
echo "========================================"
echo "Etape 4/6 : Configuration du remote"
echo "========================================"
echo ""

# Se déplacer dans le répertoire du projet
cd "$PROJET_DIR"

# Renommer le remote origin en template
echo "Renommage du remote 'origin' en 'template'..."
git remote rename origin template

# Vérifier la configuration
echo ""
echo "Configuration des remotes :"
git remote -v

echo ""
echo "========================================"
echo "Etape 5/6 : Installation de VSCode"
echo "========================================"
echo ""

# Revenir au répertoire parent
cd ..

# Vérifier si VSCode est déjà installé
if command -v code &> /dev/null; then
    echo "Visual Studio Code est déjà installé"
else
    echo "Installation de Visual Studio Code..."

    if [[ "$PKG_MANAGER" == "apt" ]]; then
        # Installation pour Debian/Ubuntu
        echo "Téléchargement et installation du package .deb de VSCode..."

        # Installer les dépendances nécessaires
        $PKG_UPDATE
        $PKG_INSTALL wget gpg apt-transport-https

        # Ajouter la clé GPG de Microsoft
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

        # Ajouter le repository VSCode
        echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

        # Nettoyer le fichier temporaire
        rm -f packages.microsoft.gpg

        # Installer VSCode
        sudo apt update
        sudo apt install -y code

    elif [[ "$PKG_MANAGER" == "dnf" ]]; then
        # Installation pour Fedora/RHEL
        echo "Ajout du repository VSCode pour Fedora/RHEL..."

        # Importer la clé GPG de Microsoft
        sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

        # Ajouter le repository VSCode
        echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

        # Installer VSCode
        $PKG_INSTALL code
    fi

    if command -v code &> /dev/null; then
        echo "Visual Studio Code installé avec succès"
    else
        echo "Avertissement: Erreur lors de l'installation de VSCode"
        echo "Vous pouvez l'installer manuellement depuis https://code.visualstudio.com/"
    fi
fi

echo ""
echo "========================================"
echo "Etape 6/6 : Ouverture de VSCode"
echo "========================================"
echo ""

# Ouvrir VSCode dans le répertoire du projet
echo "Ouverture de VSCode dans '$PROJET_DIR'..."

if command -v code &> /dev/null; then
    code "$PROJET_DIR"
else
    echo "VSCode n'est pas accessible. Ouvrez manuellement le dossier '$PROJET_DIR' dans VSCode."
fi

echo ""
echo "========================================"
echo "Installation terminée avec succès !"
echo "========================================"
echo ""
echo "Le projet est prêt dans le répertoire '$PROJET_DIR'"
echo ""
echo "Prochaines étapes dans VSCode :"
echo "1. Créez un environnement virtuel avec : uv venv"
echo "2. Installez les dépendances avec : uv sync"
echo "3. Pour mettre à jour depuis le template : git fetch template"
echo ""
