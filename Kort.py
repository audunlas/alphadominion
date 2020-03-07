from hendelse import Hendelse

class Kort:
    pass

class MyntSeierKort(Kort):
    def __init__(self, peng,poeng):
        self.peng = peng
        self.poeng = poeng

    def bruk(self):
        return Hendelse(kort=0, befa=-0, kjop=0, til_=0)

    def __repr__(self):
        if self.peng>0:
            return "Mynt-"+str(self.peng)
        else:
            return "Seier-" +str(self.poeng)

    def __hash__(self):
        return hash(self.peng) + hash(self.poeng)

    def __eq__(self, other):
        if other.__class__ == self.__class__ and \
            self.peng == other.peng and self.poeng==other.poeng:
            return True
        else:
            return False

class Befalingskort(Kort):
    pass

class Smie(Befalingskort):
    kostnad = 4

    def __init__(self):
        self.peng = 0
        self.poeng = 0

    def __repr__(self):
        return "Smie"

    def __hash__(self):
        return hash("Kort-Smie")

    def __eq__(self, other):
        return other.__class__ == self.__class__



    def bruk(self):
        #return Hendelse(4, -1, 0, True)
        return Hendelse(kort=3, befa=-1, kjop=0, til_=True)

class Landsby(Befalingskort):
    kostnad = 3

    def __init__(self):
        self.peng = 0
        self.poeng = 0

    def __repr__(self):
        return "Landsby"

    def __hash__(self):
        return hash("Kort-Landsby")

    def __eq__(self, other):
        return other.__class__ == self.__class__



    def bruk(self):
        #return Hendelse(4, -1, 0, True)
        return Hendelse(kort=1, befa=1, kjop=0, til_=True)