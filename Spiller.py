from typing import List, Dict
from random import shuffle, random, randint, choice
from Kort import Kort, Smie, MyntSeierKort, Landsby, Befalingskort
import logging
from config import DEBUG_MODE
from Spilleske import lag_kort

class Spiller:
    def __init__(self, kortene, spilleske, typer):
        self.trekkbunke = kortene
        self.kastebunke = []
        self.hand = []
        self.bruktekort = []
        self.spilleske = spilleske
        self.typer = typer
        self.prioriteringer = self.lag_prioriteringer()
        assert len(self.prioriteringer) == len(self.typer)
        self.forsterunde = None
        self.kort = {}
        self.navn = None
#        self.onskeliste = ["Pr", "Gu","Sm", "So", "Ko"]
        #self.onskeliste = ["Pr", "Gu", "So", "Ko"]
        #self.onskeliste = ["Pr", "Sm", "So", "Ko"]


    def _resirkuler_kastebunke(self):
        if DEBUG_MODE:
            assert self.trekkbunke == []
            assert not None in self.trekkbunke
            assert not None in self.kastebunke
        self.trekkbunke = self.kastebunke
        if DEBUG_MODE:
            assert not None in self.trekkbunke
        self.kastebunke = []
        self.stokk()

    def finn_forste_score(self):
        kortene = lag_kort()
        return self.finn_scorel(kortene)


    def finn_siste_score(self):
        return self.finn_scorel(self.alle_kort())

    def klart_for_nytt_spill(self, kortene, spilleske):
        self.kastebunke = []
        self.hand = []
        self.bruktekort = []
        self.trekkbunke = kortene
        self.stokk()
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
        for ab in range(len(nye_barn)):
            if ab == 0:
                nye_barn[ab].navn = self.navn
            else:
                nye_barn[ab].navn = self.navn + str(ab)
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

    def finn_score(self):
        Score = {}
        for kort in self.prioriteringer:
            assert type(self.prioriteringer[kort][0]) == float, (type(self.prioriteringer[kort][0]), self.prioriteringer[kort][0])
            Score[kort] = self.prioriteringer[kort][0]
            for ab in range(len(self.typer)):
                #print(len(self.typer), len(self.prioriteringer[kort]), type(self.typer))
                Score[kort] += self.prioriteringer[kort][ab+1] * self.finn_andel(self.typer[ab])
        return Score

    def finn_scorel(self, kortete):
        kortene = [self.spilleske.kort_til_kode(kort) for kort in kortete]
        Score = {}
        for kort in self.prioriteringer:
            Score[kort] = self.prioriteringer[kort][0]
            for ab in range(len(self.typer)):
                Score[kort] += self.prioriteringer[kort][ab+1] * self.finn_andelu(self.typer[ab], kortene)
        return Score

    def finn_andelu(self, kort, kortene):
        if kort == "Pr":
            return self.spilleske.igjen["Pr"]
        antall = kortene.count(kort)
        return antall / len(kortene)


    def finn_onskeliste(self) -> List[str]:
        Score = self.finn_score()
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
        antall = self.kort[kort]
        return antall/len(self.alle_kort())


    def alle_kort(self) -> List[Kort]:
        ny_kastebunke = self.kastebunke + self.hand + self.trekkbunke
        if DEBUG_MODE:
            assert not None in ny_kastebunke
        return ny_kastebunke


    def stokk(self):
        shuffle(self.trekkbunke)


    def trekk_hand(self):
        antall_kort = 5
        if DEBUG_MODE:
            assert self.hand == []
        for nummer in range(antall_kort):
            if len(self.trekkbunke) == 0:
                self._resirkuler_kastebunke()
                if len(self.trekkbunke) == 0:
                    return
            if DEBUG_MODE:
                assert not None in self.hand
            self.hand.append(self.trekkbunke.pop(0))
            if DEBUG_MODE:
                assert not None in self.hand

    def trekk_kort(self, nye_kort):
        for nummer in range(nye_kort):
            if len(self.trekkbunke) == 0:
                self._resirkuler_kastebunke()
                if len(self.trekkbunke) == 0:
                    return
            self.hand.append(self.trekkbunke.pop(0))


    def tell_penger(self, hand) -> int:
        self.penger = 0
        for kortet in hand:
            self.penger += kortet.peng
        return self.penger

    def sorter_hand(self) -> List[Kort]:
        if DEBUG_MODE:
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
        if DEBUG_MODE:
            assert not None in ny_hand
        return ny_hand

    def bruk_befaling(self):
        if DEBUG_MODE:
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
        if DEBUG_MODE:
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
            if DEBUG_MODE:
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
            if onske == "Sm" and self.tell_penger(self.hand) >= 4:
                return onske
            elif onske == "So" and self.tell_penger(self.hand) >= 3:
                return onske
            elif onske == "Gu" and self.tell_penger(self.hand) >= 6:
                return onske
            elif onske == "Pr" and self.tell_penger(self.hand) >= 8:
                return onske
            elif onske == "Ko":
                return onske
            elif onske == "La" and self.tell_penger(self.hand) >= 3:
                return onske
            elif onske == "He" and self.tell_penger(self.hand) >= 2:
                return onske
        return None




    def kjop(self):
        kjop = self.finn_kjop()
        logging.debug("kjop" + str(kjop)+ "  penger:" + str(self.tell_penger(self.hand)) + "  onskeliste:"+str(self.finn_onskeliste()))
        if not kjop is None:
            self.kastebunke.append(self.spilleske.kode_til_kort(kjop))
            logging.debug("Foer: " + str(self.spilleske.igjen))
            self.spilleske.trekk_fra(kjop)
            logging.debug("Etter: " + str(self.spilleske.igjen))
            self.oppdater_antall(kjop, 1)
            #print (kjop)
            return kjop
        return "ingenting"




    def utfor_runde(self):
        if DEBUG_MODE:
            assert not None in self.hand
            assert not None in self.trekkbunke
        self.trekk_hand()
        if DEBUG_MODE:
            assert not None in self.hand
        self.bruk_befaling()
        self.kjop()
        self.kast_hand()
        if DEBUG_MODE:
            assert not None in self.trekkbunke

    def utfor_runde_medskriv(self):
        self.trekk_hand()
        if DEBUG_MODE:
            assert not None in self.hand
        self.bruk_befaling()
        kjopet=[self.kjop()]
        #print(self.hand)
        if DEBUG_MODE:
            assert self.spilleske.kort_til_kode(MyntSeierKort(1,0)) == "Ko"
        handa = self.hand
        hand = [self.spilleske.kort_til_kode(kortet) for kortet in self.hand]
        alle_kort =[self.spilleske.kort_til_kode(kortet) for kortet in self.alle_kort()]
        finn_kjop = self.finn_kjop()
        if DEBUG_MODE:
            assert not None in hand
        self.kast_hand()
        assert not None in hand
        assert not None in alle_kort
        assert not None in kjopet
        assert not None in [str(self.tell_penger(handa))]
        assert not None in [finn_kjop]
        return kjopet,[str(self.tell_penger(handa))] ,["I"],hand, ["I"],alle_kort,["I"], [finn_kjop]

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



