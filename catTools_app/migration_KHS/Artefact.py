class Artefact:
    id: str
    fichier_source: str
    nom: str
    modele: str
    date_production: int
    date_entree: int
    longueur: float
    largeur: float
    hauteur: float
    poids: float
    description: str
    images = []
    stock: int
    producteur: int
    etat: int
    collection: int
    categorie: int

    def __init__(self, id, fichier_source):
        self.id = id
        self.fichier_source = fichier_source
        self.date_entree = None
        self.date_production = None
        self.longueur = None
        self.largeur = None
        self.hauteur = None
        self.poids = None
        self.description = None
        self.stock = None
        self.producteur = None
        self.etat = None
        self.collection = None
        self.categorie = None

    def ajouter_image(self, image):
        self.images.append(image)

    def supprimer_images(self):
        self.images.clear()

    def toString(self):
        print(self.id, self.nom)
