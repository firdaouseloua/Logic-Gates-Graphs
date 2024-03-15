import os

# Obtenez le chemin du répertoire parent
chemin_modules = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
print(os.listdir(chemin_modules))