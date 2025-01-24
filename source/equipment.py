class Weapon:
    def __init__(self, dmg = 0, ac = 0):
        self.base_damage = dmg
        self.accuracy = ac

class Armor:
    def __init__(self, defense = 0):
        self.defense = defense