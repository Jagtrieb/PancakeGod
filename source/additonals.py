from random import randint

ELEMENTAL_EFFECTS = {'phys': None,
                     'fire': None,
                     'ice': None,
                     'wind': None,
                     'elec': None,
                     'almight': None,}

class Damage:
    def __init__(self, val = 0, type = 'almight'):
        self.value = val
        self.type = type
        self.effect = ELEMENTAL_EFFECTS[self.type]


class Effect:
    def __init__(self, id = -1, name = 'void', duration = 0, host = None):
        self.id = id
        self.name = name
        self.duration = duration
        self.host = host
    
    def apply(self):
        print(f'{self.name} test')
    
    def remove(self):
        print(f'{self.name} remove test')

    def turn(self):
        if self.duration == 0:
            self.remove()
            return 1
        self.duration -= 1

class Buff(Effect):
    def __init__(self, id = -1, name='voidbuff', duration=0, host=None, kind = 'NONE', value = 0):
        super().__init__(id, name, duration, host)
        self.kind = kind
        self.value = value
    
    def apply(self):
        self.host.bonuses[self.kind] *= self.value
    
    def remove(self):
        self.host.bonuses[self.kind] /= self.value


def randchek(base_odds):
    return True if randint(0, 100) < base_odds else False
