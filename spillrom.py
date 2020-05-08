from Spilleske import Spilleske, lag_kort
from config import TYPER
from Spiller import Spiller

class Spillrom:
    def __init__(self, spillere):
        self.spilleske = Spilleske(TYPER)
        for spiller in spillere:
            spiller.klart_for_nytt_spill(lag_kort(), self.spilleske)



