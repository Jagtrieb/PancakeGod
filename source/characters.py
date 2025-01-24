from additonals import randchek, Damage
from equipment import Weapon, Armor


class Character():
    def __init__(self, max_HP = 0, max_SP = 0):
        self.MaxHP = max_HP
        self.MaxSP = max_SP
        self.MaxPP = 0
        self.EXP = 0
        self.LVL = 1
        self.current_abilities = []

        self.St = 3
        self.Ma = 3
        self.En = 3
        self.Ag = 3
        self.Lu = 3
        self.weak_resist = {'phys': 0,
                            'fire': 0,
                            'ice': 0,
                            'wind': 0,
                            'elec': 0}

        self.weapon = None

        self.party = None
        self.state = True
        self.HP = max_HP
        self.SP = max_SP
        self.PP = 0
        self.DMG_bonus = 1
        self.DEF_bouns = 1
        self.AG_bonus = 1
        self.weakness_bonus = 1

    def weapon_attack(self, target = None):
        if not randchek(self.weapon.accuracy):
            return 0
        dmg = int((0.5 * self.weapon.base_damage * self.St) ** 0.5)
        target.take_damage(Damage(dmg, 'phys'))
        return dmg

    def use_skill(self):
        pass

    def take_damage(self, incoming_damage):
        evade_odds = self.AG_bonus * self.Ag // 2
        if randchek(evade_odds):
            return 0
        taken_damage = int((incoming_damage * self.weakness_bonus) // (self.DEF_bouns * self.En ** 0.5) + 1)
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        return taken_damage


class Enemy(Character):
    def __init__(self, max_HP = 0, max_SP = 0):
        super().__init__(max_HP, max_SP)
        self.EXP_reward = 0
        self.money_reward = 0
        self.pattern = None


class Ally(Character):
    def __init__(self):
        super().__init__()
        self.armor = None

    def take_damage(self, incoming_damage):
        evade_odds = self.AG_bonus * self.Ag // 2
        if randchek(evade_odds):
            return 0
        taken_damage = int((incoming_damage * self.weakness_bonus) // (self.DEF_bouns * (self.En + self.armor.defense) ** 0.5) + 1)
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        return taken_damage
    
    def defend(self):
        pass

    def use_item(self):
        pass


class MainCharacter(Ally):
    def __init__(self):
        super().__init__()
        self.crystal = None
        self.crystals = []

    def escape(self):
        pass

    def change_crystal(self):
        pass
