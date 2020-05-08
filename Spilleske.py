from Kort import Smie, MyntSeierKort, Landsby

class Spilleske:
    def __init__(self, typer):
        self.typer = typer
        self.igjen = {}
        for type in self.typer:
            self.igjen[type] = 10
        self.igjen["Ko"] = 50
        self.igjen["So"] = 40
        self.igjen["Gu"] = 30

    def __repr__(self):
        return str(self.igjen)


    def trekk_fra(self, kort):
        self.igjen[kort] -= 1


    def skjekk(self, kort):
        if self.igjen[kort] > 0:
            return True
        else:
            return False

    def uferdig(self):
        antall = 0
        if self.skjekk("Pr") == False:
            return False
        for typen in self.typer:
            if self.skjekk(typen) == False:
                antall += 1
        if antall >= 3:
            return False
        return True


    def kode_til_kort(self, kode):
        onske = kode
        if onske == "Sm":
            return Smie()
        elif onske == "So":
            return MyntSeierKort(2, 0)
        elif onske == "Gu":
            return MyntSeierKort(3, 0)
        elif onske == "Pr":
            return MyntSeierKort(0, 6)
        elif onske == "Ko":
            return MyntSeierKort(1, 0)
        elif onske == "La":
            return Landsby()
        # elif onske == "He":
        #     return MyntSeierKort(0,1)

    def kort_til_kode(self, kort):
        if kort == Smie():
            return "Sm"
        elif kort == MyntSeierKort(2, 0):
            return "So"
        elif kort == MyntSeierKort(3, 0):
            return "Gu"
        elif kort == MyntSeierKort(0, 6):
            return "Pr"
        elif kort == MyntSeierKort(1, 0):
            return "Ko"
        elif kort == Landsby():
            return "La"
        elif kort == MyntSeierKort(0,1):
            return "He"


def lag_kort():
    kortene = []
    for i in range(7):
        kortene.append(MyntSeierKort(1, 0))
    for i in range(3):
        kortene.append(MyntSeierKort(0, 1))
    return kortene