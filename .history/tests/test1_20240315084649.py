import os
import importlib.util

# Chemin absolu du dossier test depuis le dossier courant
chemin_test = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test'))

# Chemin absolu du fichier mon_test.py
chemin_mon_test = os.path.join(chemin_test, 'mon_test.py')

# Charger le module mon_test.py
spec = importlib.util.spec_from_file_location('mon_test', chemin_mon_test)
mon_test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mon_test)

# Utiliser la fonction ma_fonction_test() de mon_test.py
mon_test.ma_fonction_test()