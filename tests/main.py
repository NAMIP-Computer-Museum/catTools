import config
import test
"""
boucle pour lire les fichiers
"""
for file in config.os.listdir(config.path):
     if config.re.match('V[0-9]*.xml', file):
      test.extract(str(file))