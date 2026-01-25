#!/usr/bin/env bash

# ============================================================================
# Script d'installation et configuration d'un projet NSI (macOS)
# ============================================================================
# Ce script :
# 1. Installe Homebrew (gestionnaire de paquets macOS)
# 2. Installe uv (gestionnaire de paquets Python)
# 3. Installe git
# 4. Clone le template https://github.com/MMarchand-NSI/template-nsi.git depuis GitHub dans le répertoire PROG-NSI (pas de choix de nom)
# 5. Configure le remote "template" pour les futures mises à jour
# 6. Installe VSCode
# 7. Ouvre vscode dans le répertoire cloné
# ============================================================================

set -e  # Arrêter en cas d'erreur

echo ""
echo "========================================"
echo "Installation NSI (macOS)"
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

echo "========================================"
echo "Etape 1/7 : Installation de Homebrew"
echo "========================================"
echo ""

# Vérifier si Homebrew est déjà installé
if command -v brew &> /dev/null; then
    echo "Homebrew est déjà installé"
    brew --version
else
    echo "Installation de Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Ajouter Homebrew au PATH selon l'architecture
    if [[ $(uname -m) == "arm64" ]]; then
        # Apple Silicon (M1/M2/M3)
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        # Intel
        echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/usr/local/bin/brew shellenv)"
    fi

    if command -v brew &> /dev/null; then
        echo "Homebrew installé avec succès"
    else
        echo "Erreur lors de l'installation de Homebrew"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Etape 2/7 : Installation de uv"
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
echo "Etape 3/7 : Installation de Git"
echo "========================================"
echo ""

# Vérifier si git est déjà installé
if command -v git &> /dev/null; then
    echo "Git est déjà installé"
    git --version
else
    echo "Installation de Git via Homebrew..."
    brew install git

    if command -v git &> /dev/null; then
        echo "Git installé avec succès"
    else
        echo "Erreur lors de l'installation de Git"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Etape 4/7 : Clonage du template NSI"
echo "========================================"
echo ""

# Cloner le repository dans PROG-NSI
echo "Clonage du template dans le répertoire '$PROJET_DIR'..."
git clone https://github.com/MMarchand-NSI/template-nsi.git "$PROJET_DIR"

echo "Template cloné avec succès"

echo ""
echo "========================================"
echo "Etape 5/7 : Configuration du remote"
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
echo "Etape 6/7 : Installation de VSCode"
echo "========================================"
echo ""

# Revenir au répertoire parent
cd ..

# Vérifier si VSCode est déjà installé
if command -v code &> /dev/null || [ -d "/Applications/Visual Studio Code.app" ]; then
    echo "Visual Studio Code est déjà installé"
else
    echo "Installation de Visual Studio Code via Homebrew..."
    brew install --cask visual-studio-code

    if [ -d "/Applications/Visual Studio Code.app" ]; then
        echo "Visual Studio Code installé avec succès"
    else
        echo "Avertissement: Erreur lors de l'installation de VSCode"
        echo "Vous pouvez l'installer manuellement depuis https://code.visualstudio.com/"
    fi
fi

echo ""
echo "========================================"
echo "Etape 7/7 : Ouverture de VSCode"
echo "========================================"
echo ""

# Ouvrir VSCode dans le répertoire du projet
echo "Ouverture de VSCode dans '$PROJET_DIR'..."

if command -v code &> /dev/null; then
    code "$PROJET_DIR"
elif [ -d "/Applications/Visual Studio Code.app" ]; then
    open -a "Visual Studio Code" "$PROJET_DIR"
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
