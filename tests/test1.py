import unittest
import sys
import os

# Obtenir le chemin absolu du répertoire parent
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ajouter le chemin du répertoire parent au chemin de recherche de modules Python
sys.path.append(root)

# Importer les modules depuis le répertoire parent
from modules.open_digraph import *

G = OpenDigraph()
