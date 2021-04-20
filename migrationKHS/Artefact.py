class Artefact:
    id: str
    nom: str
    modele: str
    dateProd: int
    dateIn: int
    longueur: float
    largeur: float
    hauteur: float
    poids: float
    description: str
    # table des images liées à l'artefact
    image = []
    # id table externe de KHS
    stock: int
    producteur: int
    etat: int
    collection: int
    def __init__(self,id):
        self.id = id
        self.largeur = None
        self.longueur =None
        self.hauteur = None
        self.poids = None
        self.description = None

    def addImage(self, image1):
        self.image.append(image1)
    def clearList (self):
        self.image.clear()

    def getId(self):
            return self.id

    def getNom(self):
            return self.nom
    def setNom(self,nom):
          self.nom = nom

    def getModele(self):
            return self.modele
    def setModele(self,modele):
          self.modele = modele

    def getDateProd(self):
            return self.dateProd
    def setDateProd(self,dprod):
          self.dateProd = dprod
    def getDateIn(self):
            return self.dateIn
    def setDateIn(self,dIn):
          self.dateIn = dIn

    def getLongueur(self):
            return self.longueur
    def setLongueur(self,L):
          self.longueur = L

    def getLargeur(self):
        return self.largeur
    def setLargeur(self, l):
        self.largeur = l

    def getHauteur(self):
        return self.hauteur
    def setHauteur(self, h):
        self.hauteur = h

    def getPoids(self):
        return self.poids
    def setPoids(self, p):
        self.poids = p

    def getStock(self):
        return self.stock
    def setStock(self,stock):
        self.stock = stock

    def getProducteur(self):
         return self.producteur
    def setProducteur(self,prod):
         self.producteur = prod

    def getEtat(self):
        return self.etat
    def setEtat(self,etat):
        self.etat = etat

    def getCollection(self):
        return self.collection
    def setCollection(self, c):
        self.collection = c

    def getDescription(self):
        return self.description
    def setDescription(self, d):
        self.description = d

    def toString(self):
        print(self.id, self.nom)
