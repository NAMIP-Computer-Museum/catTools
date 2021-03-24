class Artefact:
    id: str
    nom: str
    modele: str
    dateProd: int
    dateIn: int
    longueur: float
    largeur: float
    hauteur:float
    poids:float
    # table des images liées à l'artefact
    image = []
    # id table externe de KHS
    stock: int
    producteur: int
    etat: int
    collection: int

    def addImage(self, image1):
        self.image.append(image1)
    def clearList (self):
        self.image.clear()
    def toString(self):
        print(self.id, self.nom)
