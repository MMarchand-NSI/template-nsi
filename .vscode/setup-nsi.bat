@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: Script d'installation et configuration d'un projet NSI
:: ============================================================================
:: Ce script :
:: 1. Installe uv (gestionnaire de paquets Python)
:: 2. Installe git
:: 3. Clone le template https://github.com/MMarchand-NSI/template-nsi.git depuis GitHub dans le répertoire PROG-NSI (pas de choix de nom)
:: 4. Configure le remote "template" pour les futures mises à jour
:: 5. Installe VSCode
:: 6. Ouvre vscode dans le répertoire cloné
:: ============================================================================

echo.
echo ========================================
echo Installation NSI
echo ========================================
echo.

:: Nom fixe du répertoire du projet
set "PROJET_DIR=PROG-NSI"

:: Vérifier si le répertoire existe déjà
if exist "%PROJET_DIR%" (
    echo Erreur: Le repertoire "%PROJET_DIR%" existe deja
    echo Veuillez le supprimer ou le renommer avant de continuer
    pause
    exit /b 1
)

echo.
echo ========================================
echo Etape 1/6 : Installation de uv
echo ========================================
echo.

:: Vérifier si uv est déjà installé
where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo uv est deja installe
    uv --version
) else (
    echo Installation de uv via PowerShell...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    if !errorlevel! neq 0 (
        echo Erreur lors de l'installation de uv
        pause
        exit /b 1
    )

    echo uv installe avec succes
)

:: Ajouter uv au PATH pour cette session
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

echo.
echo ========================================
echo Etape 2/6 : Installation de Git
echo ========================================
echo.

:: Vérifier si git est déjà installé
where git >nul 2>&1
if %errorlevel% equ 0 (
    echo Git est deja installe
    git --version
) else (
    echo Installation de Git via winget...
    winget install --id Git.Git --source winget --silent

    if !errorlevel! neq 0 (
        echo Erreur lors de l'installation de Git
        echo Veuillez installer Git manuellement depuis https://git-scm.com/
        pause
        exit /b 1
    )

    echo Git installe avec succes
    echo Actualisation du PATH...
    :: Recharger le PATH
    call refreshenv >nul 2>&1
)

echo.
echo ========================================
echo Etape 3/6 : Clonage du template NSI
echo ========================================
echo.

:: Vérifier à nouveau git après installation potentielle
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Git n'est pas accessible. Redemarrez ce script apres avoir ferme et rouvert le terminal.
    pause
    exit /b 1
)

:: Cloner le repository dans PROG-NSI
echo Clonage du template dans le repertoire "%PROJET_DIR%"...
git clone https://github.com/MMarchand-NSI/template-nsi.git "%PROJET_DIR%"

if %errorlevel% neq 0 (
    echo Erreur lors du clonage du repository
    pause
    exit /b 1
)

echo Template clone avec succes

echo.
echo ========================================
echo Etape 4/6 : Configuration du remote
echo ========================================
echo.

:: Se déplacer dans le répertoire du projet
cd "%PROJET_DIR%"

:: Renommer le remote origin en template
echo Renommage du remote "origin" en "template"...
git remote rename origin template

if %errorlevel% neq 0 (
    echo Erreur lors du renommage du remote
    pause
    exit /b 1
)

:: Vérifier la configuration
echo.
echo Configuration des remotes :
git remote -v

echo.
echo ========================================
echo Etape 5/6 : Installation de VSCode
echo ========================================
echo.

:: Revenir au répertoire parent
cd ..

:: Vérifier si VSCode est déjà installé
where code >nul 2>&1
if %errorlevel% equ 0 (
    echo Visual Studio Code est deja installe
) else (
    echo Installation de Visual Studio Code via winget...
    winget install --id Microsoft.VisualStudioCode --source winget --silent

    if !errorlevel! neq 0 (
        echo Avertissement: Erreur lors de l'installation de VSCode
        echo Vous pouvez l'installer manuellement depuis https://code.visualstudio.com/
    ) else (
        echo Visual Studio Code installe avec succes
    )
)

echo.
echo ========================================
echo Etape 6/6 : Ouverture de VSCode
echo ========================================
echo.

:: Ouvrir VSCode dans le répertoire du projet
echo Ouverture de VSCode dans "%PROJET_DIR%"...

:: Essayer avec la commande code si disponible
where code >nul 2>&1
if %errorlevel% equ 0 (
    code "%PROJET_DIR%"
) else (
    :: Sinon essayer le chemin d'installation standard
    if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" (
        start "" "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" "%PROJET_DIR%"
    ) else if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" (
        start "" "%ProgramFiles%\Microsoft VS Code\Code.exe" "%PROJET_DIR%"
    ) else (
        echo VSCode n'est pas accessible. Ouvrez manuellement le dossier "%PROJET_DIR%" dans VSCode.
    )
)

echo.
echo ========================================
echo Installation terminee avec succes !
echo ========================================
echo.
echo Le projet est pret dans le repertoire "%PROJET_DIR%"
echo.
pause
