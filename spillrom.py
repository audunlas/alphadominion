from Spilleske import Spilleske, lag_kort
from config import TYPER
from Spiller import Spiller

class Spillrom:
    def __init__(self):
        pass

    def gjor_klar(self, spillere):
        spilleske = Spilleske(TYPER)
        for spiller in spillere:
            spiller.klart_for_nytt_spill(lag_kort(), spilleske)
