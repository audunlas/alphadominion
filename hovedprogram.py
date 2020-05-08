from Spiller import Spiller, _sorter_onskeliste, fjern_tomme
from Kort import MyntSeierKort, Smie, Landsby
from Spilleske import Spilleske, lag_kort
from pickle import dump, load
import logging
from spillrom import Spillrom
from config import TYPER
from time import time

tid_for=time()

antall_tester = 10
antall_runder = 10
antall_spillere = 1024
manuelle_spillere = ["manuellmynter.csv", "manuell1.csv", "manuellsmiland.csv"]
manuelle = ["manuelleSpillere/"+manuell for manuell in manuelle_spillere]


atyper = ["Sm", "Gu","So","Ko","La"]

def lag_filnavn(type, antall, navn):
    return "resultater/"+str(type)+str(antall)+navn+ ".csv"

def lag_filnavnmanu(navn):
    return "resultatermanuelle/" + navn+ ".csv"

def lag_filnavnsespill(navn, runde):
    return "resultatersespill/" + navn+str(runde)+ ".csv"

def lag_filnavnmrunde(type, antall, runde, navn):
    return "resultater/" + str(type) + str(runde)+"_"+ str(antall) +navn+ ".csv"


def test_trekk_hand():
    kortene = []
    spilleske = Spilleske(["Sm", "Gu", "Pr", "So","Ko","La"])
    for i in range(7):
        kortene.append(MyntSeierKort(1,0))
    for i in range(3):
        kortene.append(MyntSeierKort(0, 1))
    spiller = Spiller(kortene, spilleske, TYPER)
    spiller.stokk()
    spiller.trekk_hand()
    assert len(spiller.hand)==5

def test_tell_penger():
    kortene = []
    spilleske = Spilleske(["Sm", "Gu", "Pr", "So", "Ko", "La"])
    for i in range(4):
        kortene.append(MyntSeierKort(1, 0))
    for i in range(1):
        kortene.append(MyntSeierKort(0, 1))
    spiller = Spiller(kortene, spilleske, TYPER)
    spiller.stokk()
    spiller.trekk_hand()
    assert spiller.tell_penger(spiller.hand) == 4

def test_bruk_kort():
    kortene = []
    spilleske = Spilleske(["Sm", "Gu", "Pr", "So", "Ko", "La"])
    for i in range(3):
        kortene.append(MyntSeierKort(1, 0))
    for i in range(1):
        kortene.append(Smie())
    for i in range(1):
        kortene.append(Landsby())
    for i in range(2):
        kortene.append(Smie())
    for i in range(13):
        kortene.append(MyntSeierKort(0, 1))
    spiller = Spiller(kortene, spilleske, TYPER)
    spiller.trekk_hand()
    assert len(spiller.hand) == 5
    spiller.bruk_befaling()
    assert len(spiller.hand) == 9, [len(spiller.hand), spiller.hand]
    assert len(spiller.kastebunke) == 3, spiller.kastebunke
    spiller.kast_hand()
    assert len(spiller.trekkbunke) == 8, spiller.trekkbunke
    assert len(spiller.kastebunke) == 12, spiller.kastebunke

    spiller.trekk_hand()
    spiller.bruk_befaling()
    spiller.kast_hand()
    assert len(spiller.trekkbunke) == 3, spiller.trekkbunke
    assert len(spiller.kastebunke) == 17, spiller.kastebunke

def test_finn_score():
    typer = ["Ko", "So"]
    spilleske = Spilleske(typer)
    spiller = Spiller(lag_kort(), spilleske, typer)
    spiller.prioriteringer = {'Ko': [1, 6, 3], "So": [0, 3, 6]}
    spiller.trekkbunke = [MyntSeierKort(1, 0), MyntSeierKort(1, 0), MyntSeierKort(2, 0)]
    spiller.kort["Ko"] = 2
    spiller.kort["So"] = 1
    svar = spiller.finn_score()
    assert svar["Ko"] == 6
    assert svar["So"] == 4


    kortene = [MyntSeierKort(1, 0), MyntSeierKort(2, 0), MyntSeierKort(2, 0), MyntSeierKort(2, 0)]
    spiller.prioriteringer = {'Ko': [2, 4, 2], "So": [0, 8, 4]}
    score = spiller.finn_scorel(kortene)
    assert score["Ko"] == 4.5
    assert score["So"] == 5
    assert spiller.finn_andelu(MyntSeierKort(1, 0), kortene) == 0.25




def test_kjop():
    kortene = []
    spilleske = Spilleske(["Sm", "Gu", "Pr", "So", "Ko", "La"])
    for i in range(1):
        kortene.append(MyntSeierKort(1, 0))
    for i in range(1):
        kortene.append(MyntSeierKort(2, 0))
    for i in range(3):
        kortene.append(MyntSeierKort(0, 1))
    spiller = Spiller(kortene, spilleske, TYPER)
    spiller.trekk_hand()
    spiller.bruk_befaling()
#    assert spiller.finn_kjop() == "Sm", spiller.finn_kjop()
    spiller.kjop()
    spiller.kast_hand()
#    assert spiller.kastebunke[0] == Smie() , spiller.kastebunke[0]

#test_kjop()

def kjor(runder, typer):
    samling = {}
    for i in range(runder):
        kortene = []
        spilleske = Spilleske(typer)
        for i in range(7):
            kortene.append(MyntSeierKort(1, 0))
        for i in range(3):
            kortene.append(MyntSeierKort(0, 1))
        spiller = Spiller(kortene, spilleske, typer)
        for nummer in range(100):
            spiller.utfor_runde()
        runden = spiller.tell_korttyper()
        for kort in runden:
            if not kort in samling:
                samling[kort] = []
            samling[kort] += [runden[kort]]
    for kortet in samling:
        summen = sum(samling[kortet])
        gjennomsnitt = summen/runder
        print(kortet , gjennomsnitt)
def test_sorter_onskeliste():
    Score = {}
    Score["Sm"] = 4
    Score["Gu"] = 6
    Score["Pr"] = 8
    Score["So"] = 3
    Score["Ko"] = 0
    onskeliste = _sorter_onskeliste(Score)
    assert onskeliste == ["Pr", "Gu", "Sm", "So", "Ko"], onskeliste

def test_finn_andel():
    kortene = []
    spilleske = Spilleske(["Sm", "Gu", "Pr", "So", "Ko", "La"])
    for i in range(7):
        kortene.append(MyntSeierKort(1, 0))
    for i in range(3):
        kortene.append(MyntSeierKort(0, 1))
    spiller = Spiller(kortene, spilleske, TYPER)
    assert spiller.finn_andel(MyntSeierKort(1, 0)) == 0.7

def test_fjern():
    onskeliste = ["La", "So"]
    spilleske = Spilleske(onskeliste)
    for i in range(10):
        spilleske.trekk_fra("La")
    assert fjern_tomme(onskeliste, spilleske) ==["So"], fjern_tomme(onskeliste, spilleske)

def alle_tester():
    test_trekk_hand()
    test_bruk_kort()
    test_fjern()
    test_sorter_onskeliste()
    test_finn_andel()
    test_kjop()
    test_tell_penger()

# def spill_mothverandre(spillere):
#     while spilleske.skjekk("Pr") == True:
#         for spiller in spillere:
#             if spilleske.skjekk("Pr") == True:
#                 spiller.utfor_runde()
#     for spill in spillere:
#         print(spill.tell_poeng())

def lag_spillere(spilleske):
    spillere = []
    for telling in range(antall_spillere):
        spillere.append(Spiller(lag_kort(), spilleske, TYPER))
    for ab in range(len(spillere)):
        spillere[ab].navn = "s"+str(ab)
    return spillere

def overste_general(manuelle):
    #spilleske = Spilleske(typer)
    spilleske = None
    spillere = lag_spillere(spilleske)
    mutasjon = kjor_cup(spillere)
    finalister = kjor_cup_utenm(mutasjon, spilleske)
    vinner = spille_mothverandre(finalister)
    finalister.remove(vinner)
    print_ut(finalister, vinner)
    test_spiller(vinner)
    test_spillerm_manuelle(vinner, manuelle)


def test_spillerm_manuelle(vinner, manuelle):
    telling = {vinner.navn: 0}
    spillere = [vinner]
    for manuelltnavn in manuelle:
        navnet = selvalgt_spiller(manuelltnavn)
        telling[navnet.navn] = 0
        spillere.append(navnet)
    logging.info("Begynner testing med manuelle")
    for o in range(antall_tester):
        vinneren = spille_mothverandre_medskriv(spillere, o)
        telling[vinneren.navn] += 1
        print_losning(vinneren, lag_filnavnmanu(vinneren.navn))
    print("manuelle kommer nå!")
    for spiller in spillere:
        print(spiller.navn, "vant: ", telling[spiller.navn], "/", antall_tester)

def spille_mothverandre(spillere):
    runde = 0
    spillrom = Spillrom(spillere)
    while spillrom.spilleske.uferdig() == False:
        logging.debug("Spilleske: " + str(spillrom.spilleske.igjen))
        for spiller in spillere:
            if spillrom.spilleske.uferdig():
                spiller.utfor_runde()
        runde += 1

    maks_score = 0
    hoyest = None
    for spill in spillere:
        if spill.tell_poeng()>maks_score:
            maks_score = spill.tell_poeng()
            hoyest = spill
    return hoyest

def spille_mothverandre_medskriv(spillere,runden):
    flere_filer = {}

    for spiller in spillere:
        flere_filer[spiller] = open(lag_filnavnsespill(spiller.navn, runden), "w")

    spillrom = Spillrom(spillere)
    while spillrom.spilleske.uferdig():
        logging.debug("Spilleske: " + str(spillrom.spilleske.igjen))
        for spiller in spillere:
            if spillrom.spilleske.uferdig():
                printen = []
                for liste in spiller.utfor_runde_medskriv():
                     printen.append(";".join(liste))
                flere_filer[spiller].write(";".join(printen))
                flere_filer[spiller].write("\n")
    maks_score = 0
    hoyest = None
    for spill in spillere:
        if spill.tell_poeng() > maks_score:
            maks_score = spill.tell_poeng()
            hoyest = spill
    return hoyest

def print_ut(finalister, vinner):
    print(len(finalister))
    for ab in range(len(finalister)):
        print_losning(finalister[ab], lag_filnavn("finalist", ab, finalister[ab].navn))
    print("vinneren:")
    print_losning(vinner, lag_filnavn("vinneren", "", vinner.navn))



def kjor_cup(spillere):
    logging.info("antall spillere"+str(len(spillere)))
    cup_kamp = []
    nye_spillere = spillere
    for a in range(antall_runder):
        antall = 1
        logging.info("starter runde")
        spillere = nye_spillere
        nye_spillere = []
        for spiller in spillere:
            cup_kamp.append(spiller)
            if len(cup_kamp)==4:
                vinner = spille_mothverandre(cup_kamp)
                print_losning(vinner, lag_filnavnmrunde("mutasjon", antall, a, vinner.navn))
                antall += 1
                nye_spillere += vinner.mutasjon()
                cup_kamp = []

    return nye_spillere


def test_spiller(vinneren):
    seire = 0
    logging.info("Begynner testing")
    for o in range(antall_tester):
        seire += test_mtilfeldig(vinneren)
    print("vant: ", seire, "/", antall_tester)

def kjor_cup_utenm(spillere, spilleske):
    logging.info("antall spillere: "+ str(len(spillere)))
    assert not spillere == []
    antall = 1
    cup_kamp = []
    nye_spillere = []
    if len(spillere) > 4:
        for spiller in spillere:
            cup_kamp.append(spiller)
            if len(cup_kamp)==4:
                vinneren = spille_mothverandre(cup_kamp)
                nye_spillere.append(vinneren)
                print_losning(vinneren, lag_filnavn("cup", antall, vinneren.navn))
                antall += 1
                cup_kamp = []
        kjor_cup_utenm(nye_spillere, spilleske)

    return spillere



#def finn_antall(spiller, kort):
#   kortene = spiller.alle_kort()
#   antall = 0
#    for kortet in kortene:
#        if kortet == kort:
#            antall += 1
#   return antall / len(kortene)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        )


def print_losning(spiller, filnavn):
    losning = spiller.prioriteringer
    fil = open(filnavn, "w")
    spilleske = Spilleske(TYPER)
    antall = spiller.tell_korttyper()
    scoreforste = spiller.finn_forste_score()
    scoresiste = spiller.finn_siste_score()

    rad1 = ["typer", "Grunntall", "Smie", "Kobber", "Solv", "Gull", "Landsby", "Provins", "antall", "forste score", "siste score"]
    fil.write(";".join(rad1)+"\n")
    for type in losning:
        mine_ting = [type, losning[type][0], losning[type][1], losning[type][2], losning[type][3],
                     losning[type][4], losning[type][5], losning[type][6], antall.get(spilleske.kode_til_kort(type)), scoreforste[type], scoresiste[type]]
        ny_liste = [str(ordet) for ordet in mine_ting]
        fil.write(";".join(ny_liste)+ "\n")



def test_mtilfeldig(spilleren):
    logging.info("Begynner testing gruppe")
    kampen = [spilleren]
    for telling in range(3):
        kampen.append(Spiller(lag_kort(), Spilleske(TYPER), TYPER))
    vinneren = spille_mothverandre(kampen)
    if vinneren == spilleren:
        return 1
    else:
        return 0

def les_inn(filnavn) -> dict:
    filen =open(filnavn)
    #print(_les_inn(filen, len(TYPER)), filnavn)
    return _les_inn(filen, len(TYPER))

def _les_inn(linjeSamling, antallTyper):
    score = {}
    for linje in linjeSamling:
        assert linje.strip() != ""
        biter = linje.split(";")
        if biter[0] == "typer":
            continue
        score[biter[0]] = []
        for b in range(antallTyper+1):
            #print(b)
            score[biter[0]].append(float(biter[b+1].replace(",",".")))
    for kort in score:
        assert len(score[kort]) == antallTyper+1
    return score


LES_INN_TEST = """typer;Grunntall;Smie;Kobber
Sm;1;-1;0.001
Ko;0.001;0.001;0.001""".split("\n")

def test_les_inn(testData):
    resultat = _les_inn(testData,2)
    assert resultat=={'Sm': [1.0, -1.0, 0.001], 'Ko': [0.001, 0.001, 0.001]}

test_les_inn(LES_INN_TEST)

def selvalgt_spiller(filnavn):
    spilleske = None
    spiller = Spiller(lag_kort(), spilleske, TYPER)
    spiller.prioriteringer = les_inn(filnavn)
    navnet = filnavn.split("/")
    spiller.navn = navnet[-1]
    return spiller




#kjor(100, typer)
#alle_tester()
#kjor(1, typer)
# spilleske = Spilleske(typer)
# spillere = []
# antall_spillere = 4
#
# for telling in range(antall_spillere):
#     kortene = []
#     for i in range(7):
#         kortene.append(MyntSeierKort(1, 0))
#     for i in range(3):
#         kortene.append(MyntSeierKort(0, 1))
#     spillere.append(Spiller(kortene, spilleske, typer))
open("min_logg","w").close()
logging.basicConfig(filename="min_logg",level=0)
overste_general(manuelle)

#test_finn_score()
#selvalgt_spiller("manuelleSpillere/"+"manuell1.csv")
kjoretid = time() - tid_for

print("tid(sek): ", int(kjoretid))