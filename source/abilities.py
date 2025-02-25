class Ability:
    def __init__(self, name = "void", cost = -1, stat = 'St'):
        self.name = name
        self.cost = cost
        self.stat = stat
        self.kind = None

    def __str__(self):
        return str(self.name)

class AttackAbility(Ability):
    def __init__(self, name = "void", cost = -1, stat = 'St', element = None, dmg = -1):
        super().__init__(name, cost, stat)
        self.element = element
        self.base_damage = dmg

class SupportAbility(Ability):
    def __init__(self):
        super().__init__()
        self.value = 0
    
    def act(self):
        pass

class HealAbility(SupportAbility):
    def __init__(self):
        super().__init__()
        self.value = 0
    
    def act(self):
        pass

