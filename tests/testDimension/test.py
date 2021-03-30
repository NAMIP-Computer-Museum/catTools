import unittest
from catTools.migrationKHS import utilitaireKhs, Artefact
import xml.etree.ElementTree as ET

class TestSetDimension(unittest.TestCase):
    """test ok"""
    def test_Alldimension(self):
        file = "/khs/data/V0000300.xml"
        tree = ET.parse(str(file))
        root = tree.getroot()
        artefact = Artefact.Artefact()
        artefact.id = utilitaireKhs.idArtefact(root)
        utilitaireKhs.dimensionArtefact(root, artefact)
        print(artefact.hauteur)
        self.assertEqual(artefact.longueur, "125")
        self.assertEqual(artefact.largeur, "62")
        self.assertEqual(artefact.poids, "180")

    """test ok"""
    def testKGdimension(self):
        artefact = Artefact.Artefact()
        file = "/khs/data/V0000293.xml"
        tree = ET.parse(str(file))
        root = tree.getroot()
        utilitaireKhs.dimensionArtefact(root, artefact)
        self.assertEqual(artefact.poids, "18")

    """test pas ok"""
    def testDeuxdimension(self):
        artefact = Artefact.Artefact()
        file = "/khs/data/V0000298.xml"
        tree = ET.parse(str(file))
        root = tree.getroot()
        utilitaireKhs.dimensionArtefact(root, artefact)
        self.assertEqual(artefact.longueur, "59")
        self.assertEqual(artefact.largeur, "50")
    """test pas ok"""
    def testTroisdimension(self):
        artefact = Artefact.Artefact()
        file = "/khs/data/V0000295.xml"
        tree = ET.parse(str(file))
        root = tree.getroot()
        utilitaireKhs.dimensionArtefact(root, artefact)
        self.assertEqual(artefact.longueur, "48")
        self.assertEqual(artefact.largeur, "38")
        self.assertEqual(artefact.hauteur, "93")

if '__main__' == __name__:
  unittest.main()