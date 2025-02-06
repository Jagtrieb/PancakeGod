from additonals import randchek, Damage, load_image
from equipment import Weapon, Armor, Crystal
from abilities import Ability, AttackAbility, SupportAbility
import pygame

class Character():
    def __init__(self, name = 'Void', max_HP = 0, crystal = Crystal(0), weapon = Weapon()):
        self.name = name
        self.MaxHP = max_HP
        self.EXP = 0
        self.LVL = 1
        self.weapon = weapon
        self.crystal = crystal

        self.stats = {'St': 3,
                      'Ma': 3,
                      'En': 3,
                      'Ag': 3,
                      'Lu': 3}

        self.bonuses = {'ATK': 1,
                        'DEF': 1,
                        'AG': 1}

        self.party = None
        self.state = 'alive'
        self.HP = max_HP
        self.weakness_bonus = 1

        self.effects = []

        self.battle_card = None

    def __str__(self):
        return self.name

    def weapon_attack(self, target = None):
        if not randchek(self.weapon.accuracy):
            return 0
        dmg = int((0.5 * self.weapon.base_damage * self.stats['St']) ** 0.5 * self.bonuses['ATK'])
        target.take_damage(Damage(dmg, 'phys'))
        return dmg

    def use_skill(self, ability = Ability(),  target = None):
        if ability.cost > self.crystal.charge:
            print("Not Enough Crystal charge!\n")
            return 0
        self.crystal.charge -= ability.cost
        if type(ability) == AttackAbility:
            self.use_attack_skill(ability, target)
            return 1
        elif type(ability) == SupportAbility:
            self.use_support_skill(ability, target)
            return 2
        
    def use_attack_skill(self, ability = AttackAbility(), target = None):
        element = ability.element
        dmg = round((ability.base_damage * self.stats[ability.stat]) ** 0.5 * self.bonuses['ATK'])
        target.take_damage(Damage(dmg, element))
        return dmg

    def use_support_skill(self, ability = Ability(),  target = None):
        pass

    def take_damage(self, incoming_damage):
        evade_odds = self.bonuses['AG'] * self.stats['Ag'] // 2
        if randchek(evade_odds):
            return 0
        if self.crystal.weak_resist[incoming_damage.type] == -1:
            self.weakness_bonus = 1.5
            print("!WEAK!")
        elif self.crystal.weak_resist[incoming_damage.type] == 1:
            self.weakness_bonus = 0.2
            print("!RESIST!")
        self.battle_card.update()

        taken_damage = round((incoming_damage.value * self.weakness_bonus) / (self.bonuses['DEF'] * self.stats['En'] ** 0.5)) + 1
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        return taken_damage


class Enemy(Character):
    def __init__(self, name = 'Void', max_HP = 0, crystal = Crystal(), weapon = Weapon(), img_path = 'assets/images/enemyPlaceholder.png'):
        super().__init__(name, max_HP, crystal, weapon)
        self.EXP_reward = 0
        self.money_reward = 0
        self.pattern = None
        self.image = pygame.transform.scale(load_image(img_path), (100, 100))


class Ally(Character):
    def __init__(self, name = 'Void', max_HP = 0, crystal = Crystal(), weapon = Weapon(), armor = Armor(), img_path = 'assets/images/iconPlaceholder.png'):
        super().__init__(name, max_HP, crystal, weapon)
        self.armor = armor
        self.icon = pygame.transform.scale(load_image(img_path), (100, 100))

    def take_damage(self, incoming_damage):
        evade_odds = self.bonuses['AG'] * self.Ag // 2
        if randchek(evade_odds):
            return 0
        if self.crystal.weak_resist[incoming_damage.type] == -1:
            self.weakness_bonus = 1.5
        elif self.crystal.weak_resist[incoming_damage.type] == 1:
            self.weakness_bonus = 0.2
        taken_damage = round((incoming_damage * self.weakness_bonus) // (self.bonuses['DEF'] * (self.En + self.armor.defense) ** 0.5)) + 1
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        return taken_damage
    
    def guard(self):
        pass

    def use_item(self):
        pass


class MainCharacter(Ally):
    def __init__(self, name = 'Void', max_HP = 0, crystal = Crystal(), weapon = Weapon(), armor = Armor()):
        super().__init__(name, max_HP, crystal, weapon, armor)
        self.crystals = []

    def escape(self):
        pass

    def change_crystal(self):
        pass


if __name__ == '__main__':
    c = Crystal(3)
    c1 = Crystal(30)
    c1.weak_resist['fire'] = 0
    wp = Weapon(25, 85)
    chaar = Character('jokaa', 35, c, wp)
    en = Enemy('churka', 25, c1)
    f = AttackAbility("Agi", 4, 'Ma', 'fire', 50)
    c.add_ability(f)
    print(en.HP)
    chaar.use_skill(f)
    print(en.HP)