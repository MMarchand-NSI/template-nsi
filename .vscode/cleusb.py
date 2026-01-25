

import psutil
import os
import shutil
import sys
from pathlib import Path
from utils import log_info, log_success, log_warning, log_error

def get_usb_drives():
    """
    Détecte les clés USB (lecteurs amovibles)
    
    Source: documentation psutil

    # Utilisation
    usb_drives = get_usb_drives()
    for drive in usb_drives:
        print(f"Clé USB détectée: {drive['device']}")
    """
    usb_drives = []
    
    for partition in psutil.disk_partitions():
        # Sur Windows, opts contient 'removable' pour les clés USB
        if 'removable' in partition.opts.lower():
            usb_drives.append({
                'device': partition.device,      # Ex: 'E:\\'
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype       # Ex: 'FAT32', 'NTFS'
            })
    
    return usb_drives


def sauvegarde():
    """
    - S'il y a plusieurs clés USB connectées ayant un dossier PROG_NSI à la racine -> Erreur
    - S'il y a plusieurs clés USB connectées et qu'aucune n'a de répertoire PROG_NSI à la racine -> Erreur
    - S'il n'y a pas de clé USB -> erreur
    - sinon:
        - s'il n'y a qu'une clé et pas de répertoire PROG_NSI à la racine, le créer
        - copie tous les répertoires sauf .venv, .git et .pytest_cache dans le répertoire PROG_NSI de la clé
        - copie tous les fichiers à la racine dans le répertoire PROG_NSI de la clé.
    """
    # Récupère les clés USB
    usb_drives = get_usb_drives()

    # Cas 1: Pas de clé USB -> erreur
    if not usb_drives:
        log_error("Aucune clé USB détectée")
        sys.exit(1)

    # Cas 2: Plusieurs clés USB -> vérifier les dossiers PROG_NSI
    if len(usb_drives) > 1:
        # Cherche les dossiers PROG_NSI à la racine des clés USB
        prog_nsi_paths = []
        for drive in usb_drives:
            prog_nsi_path = Path(drive['mountpoint']) / 'PROG_NSI'
            if prog_nsi_path.exists() and prog_nsi_path.is_dir():
                prog_nsi_paths.append(prog_nsi_path)

        if len(prog_nsi_paths) > 0:
            log_error(f"Plusieurs clés USB avec dossier PROG_NSI détectées: {prog_nsi_paths}")
            sys.exit(1)
        else:
            log_error("Plusieurs clés USB connectées mais aucune n'a de répertoire PROG_NSI")
            sys.exit(1)

    # Cas 3: Une seule clé USB
    drive = usb_drives[0]
    destination = Path(drive['mountpoint']) / 'PROG_NSI'

    # Créer le dossier PROG_NSI s'il n'existe pas
    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)
        log_info(f"Création du dossier PROG_NSI dans {drive['mountpoint']}")

    # Dossier source (répertoire courant)
    source = Path.cwd()

    # Répertoires à exclure
    exclusions = {'.venv', '.git', '.pytest_cache'}

    # Copie tous les répertoires sauf ceux exclus
    for item in source.iterdir():
        if item.is_dir() and item.name not in exclusions:
            dest_path = destination / item.name

            # Supprime le dossier de destination s'il existe déjà
            if dest_path.exists():
                shutil.rmtree(dest_path)

            # Copie le répertoire
            shutil.copytree(item, dest_path)
            log_info(f"Copie de {item.name} vers {dest_path}")

    # Copie tous les fichiers à la racine
    for item in source.iterdir():
        if item.is_file():
            dest_path = destination / item.name
            shutil.copy2(item, dest_path)
            log_info(f"Copie de {item.name} vers {dest_path}")

    log_success(f"Sauvegarde terminée dans {destination}")


def import_cle_vers_vscode():
    """
    Restaure tous les fichiers et répertoires de la clé dans le répertoire de vscode.
    - S'il n'y a qu'une clé avec un répertoire PROG_NSI à la racine:
        - copie tous les répertoires et fichiers du répertoire PROG_NSI de la clé dans le répertoire de VSCode
    - Sinon: Erreur
    """
    # Récupère les clés USB
    usb_drives = get_usb_drives()

    # Cas 1: Pas de clé USB -> erreur
    if not usb_drives:
        log_error("Aucune clé USB détectée")
        sys.exit(1)

    # Cherche les dossiers PROG_NSI à la racine des clés USB
    prog_nsi_paths = []
    for drive in usb_drives:
        prog_nsi_path = Path(drive['mountpoint']) / 'PROG_NSI'
        if prog_nsi_path.exists() and prog_nsi_path.is_dir():
            prog_nsi_paths.append(prog_nsi_path)

    # Vérifie qu'il y a exactement un dossier PROG_NSI
    if len(prog_nsi_paths) == 0:
        log_error("Aucun dossier PROG_NSI trouvé sur les clés USB")
        sys.exit(1)
    elif len(prog_nsi_paths) > 1:
        log_error(f"Plusieurs dossiers PROG_NSI trouvés: {prog_nsi_paths}")
        sys.exit(1)

    # Source : dossier PROG_NSI de la clé
    source = prog_nsi_paths[0]

    # Destination : répertoire courant (VSCode workspace)
    destination = Path.cwd()

    # Copie tous les répertoires
    for item in source.iterdir():
        if item.is_dir():
            dest_path = destination / item.name

            # Supprime le dossier de destination s'il existe déjà
            if dest_path.exists():
                shutil.rmtree(dest_path)

            # Copie le répertoire
            shutil.copytree(item, dest_path)
            log_info(f"Import de {item.name} vers {dest_path}")

    # Copie tous les fichiers à la racine
    for item in source.iterdir():
        if item.is_file():
            dest_path = destination / item.name
            shutil.copy2(item, dest_path)
            log_info(f"Import de {item.name} vers {dest_path}")

    log_success(f"Import terminé depuis {source}")
