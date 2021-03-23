class Artefact:
    id: str
    nom: str
    image = []
    ref = []
    stock: str
    dateIn: int
    modele: str
    producteur: str
    dateProd: int
    dimension = []
    etat: str
    collection: str

    def addImage(self, image1):
        self.image.append(image1)

    def addRef(self, ref1):
        self.ref.append(ref1)

    def addDim(self, dim1):
        self.dimension.append(dim1)

    def clearList (self):
        self.dimension.clear()
        self.image.clear()
        self.ref.clear()

    def toString(self):
        print(self.id, self.nom, self.dimension)
