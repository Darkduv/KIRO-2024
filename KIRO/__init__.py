"""
Permet d'initialiser l'application.
Crée automatiquement un dossier à la racine du dossier utilisateur.
Ce dossier permettra de stocker des fichiers utiles à l'application, par exemple
les fichiers de logs.
"""

import os
from pathlib import Path
import platform

# ----- Variables du module 

# Chemin du dossier utilisateur
USERPROFILE_PATH = Path('./')
USER_DIR = USERPROFILE_PATH / f'./.{__name__}'

# Création du dossier -- Contient notamment les logs
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# ----- Variables du package
__name__='KIRO'