import characters

class Party:
    def __init__(self, members = None):
        self.members = members
        self.isDead = False

    def update_state(self):
        for i in self.members:
            if i.state != 'dead':
                return 0
        self.isDead = True
        return 1

class PlayerParty(Party):
    def __init__(self, members=None):
        super().__init__(members)
    
    def check_party(self):
        if characters.MainCharacter not in self.members:
            return 0

class EnemyParty(Party):
    def __init__(self, members=None):
        super().__init__(members)
        self.knocked_down = 0