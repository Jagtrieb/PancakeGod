class Weapon:
    def __init__(self, dmg = 0, ac = 0):
        self.base_damage = dmg
        self.accuracy = ac

class Armor:
    def __init__(self, defense = 0):
        self.defense = defense


class Crystal:
    def __init__(self):
        self.abilities = []
        self.unavailable_abilities = None
        self.weak_resist = {'phys': 0,
                            'fire': 0,
                            'ice': 0,
                            'wind': 0,
                            'elec': 0}
    
    def add_ability(self, ability):
        self.abilities.append(ability)