from typing import List, Dict
from random import shuffle, random, randint, choice
from Kort import Kort, Smie, MyntSeierKort, Landsby, Befalingskort
import logging

class Spiller:
    def __init__(self, kortene, spilleske, typer):
        self.trekkbunke = kortene
        self.kastebunke = []
        self.hand = []
        self.bruktekort = []
        self.spilleske = spilleske
        self.typer = typer
        self.prioriteringer = self.lag_prioriteringer()
        self.forsterunde = None
        self.kort = {}
#        self.onskeliste = ["Pr", "Gu","Sm", "So", "Ko"]
        #self.onskeliste = ["Pr", "Gu", "So", "Ko"]
        #self.onskeliste = ["Pr", "Sm", "So", "Ko"]


    def _resirkuler_kastebunke(self):
        assert self.trekkbunke == []
        assert not None in self.trekkbunke
        assert not None in self.kastebunke
        self.trekkbunke = self.kastebunke
        assert not None in self.trekkbunke
        self.kastebunke = []
        self.stokk()

    def klart_for_nytt_spill(self, kortene, spilleske):
        self.kastebunke = []
        self.hand = []
        self.bruktekort = []
        self.trekkbunke = kortene
        self.spilleske = spilleske
        for type in self.typer:
            self.kort[type] = 0
        self.oppdater_antall("Ko", 7)

    def oppdater_antall(self, kort, antallet):
        self.kort[kort] += antallet


    def lage_barn(self):
        nye_barn = [self]
        for telling in range(3):
            kortene = []
            for i in range(7):
                kortene.append(MyntSeierKort(1, 0))
            for i in range(3):
                kortene.append(MyntSeierKort(0, 1))
            nye_barn.append(Spiller(kortene, self.spilleske, self.typer))
        return nye_barn

    def mutasjon(self):
        nye_barn = self.lage_barn()
        for barnet in nye_barn:
            for i in range(3):
                barnet.prioriteringer[choice(self.typer)][randint(0,6)] += random()/5 - 0.1
        return nye_barn






    def tell_poeng(self):
        poeng = 0
        for kortet in self.alle_kort():
            poeng += kortet.poeng
        return poeng


    def finn_onskeliste(self) -> List[str]:
        Score = {}
        for kort in self.prioriteringer:
            Score[kort] = self.prioriteringer[kort][0]
            Score[kort] += self.prioriteringer[kort][1]*self.finn_andel(Smie())
            Score[kort] += self.prioriteringer[kort][2]*self.finn_andel(MyntSeierKort(1,0))
            Score[kort] += self.prioriteringer[kort][3]*self.finn_andel(MyntSeierKort(2,0))
            Score[kort] += self.prioriteringer[kort][4]*self.finn_andel(MyntSeierKort(3,0))
            Score[kort] += self.prioriteringer[kort][5]*self.finn_andel(Landsby())
            Score[kort] += self.prioriteringer[kort][6]*self.finn_andel(MyntSeierKort(0,6))
        # Score["Sm"] = 4 - self.finn_andel(Smie())*30 + self.finn_andel(Landsby()) * 35
        # Score["Gu"] = 6 + self.finn_andel(Smie())*3
        # Score["Pr"] = 8 + 10-self.finn_andel(MyntSeierKort(0,6))
        # Score["So"] = 3 + self.finn_andel(Smie())*3
        # Score["Ko"] = 1 - self.finn_andel(MyntSeierKort(2,0))*10 - self.finn_andel(MyntSeierKort(3,0))*20
        # Score["La"] = 3 + self.finn_andel(Smie())*20 - self.finn_andel(Landsby())*20
        #print(Score["Ko"], Score["Pr"])
        #print(self.prioriteringer)
        onskeliste = _sorter_onskeliste(Score)
        onskeliste = fjern_tomme(onskeliste, self.spilleske)
        return onskeliste

    def finn_andel(self, kort) -> float:
        if kort == "Pr":
            return self.spilleske.igjen["Pr"]
        antall = self.kort[self.spilleske.kort_til_kode(kort)]
        return antall/len(self.alle_kort())


    def alle_kort(self) -> List[Kort]:
        ny_kastebunke = self.kastebunke + self.hand + self.trekkbunke
        assert not None in ny_kastebunke
        return ny_kastebunke


    def stokk(self):
        shuffle(self.trekkbunke)


    def trekk_hand(self):
        antall_kort = 5
        assert self.hand == []
        for nummer in range(antall_kort):
            if len(self.trekkbunke) == 0:
                self._resirkuler_kastebunke()
                if len(self.trekkbunke) == 0:
                    return
            assert not None in self.hand
            self.hand.append(self.trekkbunke.pop(0))
            assert not None in self.hand

    def trekk_kort(self, nye_kort):
        for nummer in range(nye_kort):
            if len(self.trekkbunke) == 0:
                self._resirkuler_kastebunke()
                if len(self.trekkbunke) == 0:
                    return
            self.hand.append(self.trekkbunke.pop(0))


    def tell_penger(self) -> int:
        self.penger = 0
        for kortet in self.hand:
            self.penger += kortet.peng
        return self.penger

    def sorter_hand(self) -> List[Kort]:
        assert not None in self.hand
        ny_hand = []
        for kort in self.hand:
            fortsett = True
            plass = 0
            while fortsett == True:
                if ny_hand == []:
                    ny_hand.append(kort)
                    fortsett = False
                else:
                    if not plass + 1 > len(ny_hand):
                        hendelse = kort.bruk()
                        hendelse1 = ny_hand[plass].bruk()
                        if hendelse.befalinger > hendelse1.befalinger:
                            ny_hand = ny_hand[:plass] + [kort] + ny_hand[plass:]
                            fortsett = False
                        else:
                            plass += 1
                    else:
                        ny_hand.append(kort)
                        fortsett = False
        assert not None in ny_hand
        return ny_hand

    def bruk_befaling(self):
        assert self.bruktekort==[]
        befalinger = 1
        kjop = 1
        hendelse = None
        while befalinger >= 1 and hendelse != False:
            # print(befalinger,len(self.hand), self.hand,len(self.alle_kort()), self.alle_kort())
            hendelse = self.bruk_en_befaling()
            if not hendelse == False:
                befalinger += hendelse.befalinger
                nye_kort = hendelse.kort
                kjop += hendelse.kjop
                self.trekk_kort(nye_kort)
        self.kastebunke += self.bruktekort
        assert not None in self.kastebunke
        self.bruktekort = []

    def bruk_en_befaling(self): #-> Hendelse/False
        self.hand = self.sorter_hand()
        for i in range(len(self.hand)):
            kortet = self.hand[i]
            if isinstance(kortet, Befalingskort):
                hendelse = kortet.bruk()
                self.hand.pop(i)
                self.bruktekort.append(kortet)
                return hendelse
        return False

    def kast_hand(self):
        for kort in self.hand:
            assert not kort is None
            self.kastebunke.append(kort)
        self.hand = []

    def lag_prioriteringer(self):
        prioriteringer = {}
        for typen in self.typer:
            prioriteringer[typen] = []
            for i in range(len(self.typer)+1):
                prioriteringer[typen].append(random())
        return prioriteringer


    def finn_kjop(self): #->Kort/None
        for onske in self.finn_onskeliste():
            if onske == "Sm" and self.tell_penger() >= 4:
                return onske
            elif onske == "So" and self.tell_penger() >= 3:
                return onske
            elif onske == "Gu" and self.tell_penger() >= 6:
                return onske
            elif onske == "Pr" and self.tell_penger() >= 8:
                return onske
            elif onske == "Ko":
                return onske
            elif onske == "La" and self.tell_penger() >= 3:
                return onske
            elif onske == "He" and self.tell_penger() >= 2:
                return onske
        return None




    def kjop(self):
        kjop = self.finn_kjop()
        logging.debug("kjop" + str(kjop)+ "  penger:" + str(self.tell_penger()) + "  onskeliste:"+str(self.finn_onskeliste()))
        if not kjop is None:
            self.kastebunke.append(self.spilleske.kode_til_kort(kjop))
            logging.debug("Foer: " + str(self.spilleske.igjen))
            self.spilleske.trekk_fra(kjop)
            logging.debug("Etter: " + str(self.spilleske.igjen))
            self.oppdater_antall(kjop, 1)




    def utfor_runde(self):
        assert not None in self.hand
        assert not None in self.trekkbunke
        self.trekk_hand()
        assert not None in self.hand
        self.bruk_befaling()
        self.kjop()
        self.kast_hand()
        assert not None in self.trekkbunke

    def tell_korttyper(self) -> int:
        antall = {}
        for kort in self.trekkbunke:
            if not kort in antall:
                antall[kort] = 0
            antall[kort] += 1
        for kortet in self.kastebunke:
            if not kortet in antall:
                antall[kortet] = 0
            antall[kortet] += 1
        return antall








def _sorter_onskeliste(Score: Dict[str,float]) -> List[str]:
    onskeliste = []
    for type in Score:
        fortsett = True
        plass = 0
        while fortsett == True:
            if onskeliste == []:
                onskeliste.append(type)
                fortsett = False
            else:
                if not plass+1>len(onskeliste):
                    if Score[type] > Score[onskeliste[plass]]:
                        onskeliste = onskeliste[:plass] + [type] + onskeliste[plass:]
                        fortsett = False
                    else:
                        plass += 1
                else:
                    onskeliste.append(type)
                    fortsett = False
    return onskeliste


#
# def _fjern_tomme(onskeliste):
#     spilleske = Spilleske(onskeliste)
#     lengde = len(onskeliste)
#     for nummer in lengde:
#         skjekk = spilleske.trekk_fra(onskeliste[nummer])
#         if skjekk == False:
#             #print(onskeliste[nummer])
#             onskeliste.pop(nummer)
#     return onskeliste

def fjern_tomme(onskeliste, spilleske):
    ny = [onskeliste[nummer] for nummer in range(len(onskeliste)) if spilleske.skjekk(onskeliste[nummer]) == True ]
    # for nummer in range(lengde):
    #     skjekk = spilleske.skjekk(onskeliste[nummer])
    #     if skjekk == False:
    #         #print(onskeliste[nummer])
    #         pass
    #     else:
    #         ny.append(onskeliste[nummer])
    return ny

def skjekk():
    liste = ["a","b","c","b","c"]
    for antall in range(len(liste)):
        if liste[antall] == "b":
            liste.pop(antall)
    print(liste)



