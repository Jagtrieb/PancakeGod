from random import randint

ELEMENTAL_EFFECTS = {'phys': None,
                     'fire': None,
                     'ice': None,
                     'wind': None,
                     'elec': None,
                     'almight': None,}

class Damage:
    def __init__(self, val, type):
        self.value = val
        self.type = type
        self.effect = ELEMENTAL_EFFECTS[self.type]


def randchek(base_odds):
    return True if randint(0, 100) < base_odds else False
