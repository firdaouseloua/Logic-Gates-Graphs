import os

# Obtenez le chemin du répertoire parent
chemin_modules = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
from os.listdir(chemin_modules)[0] import*