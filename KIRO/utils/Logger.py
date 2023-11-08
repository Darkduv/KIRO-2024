"""
Génère et gère l'ensemble des fichiers de logs de l'application.
"""

# Bibliothèque standard de Python
import logging
from logging import (
    StreamHandler,
)
from logging.handlers import (
    RotatingFileHandler,
)
import os

# Import des constantes module
from KIRO import USER_DIR,__name__

# ----------------------------------------------------------------------------
# Configuration du rootLogger

# Création du logger
rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)

# ----- Handler n°1 --> FileHandler (pour sauvegarde messages)

# -- Paramètres
NAME_SIZE = 16
LOG_MFMT  = '%(asctime)s %(name)-' + \
    str(NAME_SIZE) + 's %(levelname)-7s : %(message)s'
LOG_DFMT = '%Y%m%d %H:%M:%S'
FORMATTER = logging.Formatter(LOG_MFMT, LOG_DFMT)
LOGFILEPATH = os.path.join(USER_DIR, f"{__name__}.log")

# --Création
fh = RotatingFileHandler(LOGFILEPATH, 'a', maxBytes=1000000,
                         backupCount=4,encoding='utf-8')
fh.setFormatter(FORMATTER)
fh.setLevel(logging.DEBUG)

# ----- Handler n°2 --> Console
ch = StreamHandler()
cformatter = logging.Formatter(
    '%(name)-' + str(NAME_SIZE) + 's %(levelname)-7s : %(message)s')
ch.setFormatter(cformatter)
ch.setLevel(logging.INFO)

# -------- Ajout des handlers au rootLogger
rootlogger.addHandler(ch)
rootlogger.addHandler(fh)

# ----------------------------------------------------------------------------
# Fonctions pour la création des loggers

def getLogger(
    name:str=f'{__name__}_ROOT',
):
    """Renvoie un logger qui hérite de la paramétrisation du root logger.

    Args:
        name (str, optional): Nom du logger renvoyé. La longeur du nom est 
        cappée à 16.
    """
    tag = name[:NAME_SIZE].ljust(NAME_SIZE)
    return logging.getLogger(tag)
