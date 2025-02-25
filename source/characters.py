from additonals import randchek, Damage, load_image
from equipment import Weapon, Armor, Crystal
from abilities import Ability, AttackAbility, SupportAbility
import config
import pygame
import sys

class Character():
    def __init__(self, name = 'Void', max_HP = 0, max_SP = 0, crystal = Crystal(), weapon = Weapon()):
        self.name = name
        self.MaxHP = max_HP
        self.MaxSP = max_SP
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
        self.SP = max_SP
        self.weakness_bonus = 1

        self.effects = []

        self.isActive = False
        self.battle_card = None

    def __str__(self):
        return self.name

    def weapon_attack(self, target = None):
        if not randchek(self.weapon.accuracy):
            return 0
        dmg = int((0.5 * self.weapon.base_damage * self.stats['St']) ** 0.5 * self.bonuses['ATK'])
        dealt_damage, attack_result = target.take_damage(Damage(dmg, 'phys'))
        command = 'one_more' if attack_result else 'next'
        return dealt_damage, command

    def use_skill(self, ability_id = -1,  target = None):
        ability = self.crystal.abilities[ability_id]
        if ability.cost > self.SP:
            print("Not Enough SP!\n")
            return 0, 'next'
        self.SP -= ability.cost
        if type(ability) == AttackAbility:
            return self.use_attack_skill(ability, target)
        elif type(ability) == SupportAbility:
            self.use_support_skill(ability, target)
            return 2
        
    def use_attack_skill(self, ability = AttackAbility(), target = None):
        element = ability.element
        dmg = round((ability.base_damage * self.stats[ability.stat]) ** 0.5 * self.bonuses['ATK'])
        dealt_damage, attack_result = target.take_damage(Damage(dmg, element))
        command = 'one_more' if attack_result else 'next'
        return dealt_damage, command 

    def use_support_skill(self, ability = Ability(),  target = None):
        pass

    def take_damage(self, incoming_damage):
        result = 0
        evade_odds = self.bonuses['AG'] * self.stats['Ag'] // 2
        if randchek(evade_odds):
            return 0, result
        if self.crystal.weak_resist[incoming_damage.type] == -1:
            self.weakness_bonus = 1.5
            print("!WEAK!")
            result = 1
        elif self.crystal.weak_resist[incoming_damage.type] == 1:
            self.weakness_bonus = 0.2
            print("!RESIST!")

        taken_damage = round((incoming_damage.value * self.weakness_bonus) / (self.bonuses['DEF'] * self.stats['En'] ** 0.5)) + 1
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        self.weakness_bonus = 1
        self.bonuses['ATK'] = 1
        self.bonuses['DEF'] = 1
        self.bonuses['AG'] = 1
        print(f'{self.HP}/{self.MaxHP}')
        return taken_damage, result
    
    def __str__(self):
        return self.name


class Enemy(Character, pygame.sprite.Sprite):
    def __init__(self, name = 'Void', max_HP = 0, max_SP = 0, crystal = Crystal(), weapon = Weapon(), img_path = 'assets/images/enemyPlaceholder.png'):
        super().__init__(name, max_HP, max_SP, crystal, weapon)
        pygame.sprite.Sprite.__init__(self)
        self.EXP_reward = 0
        self.money_reward = 0
        self.pattern = None
        self.image = pygame.transform.scale(load_image(img_path), (100, 100))
        self.rect = self.image.get_rect()
    
    def sprite_center(self):
        #print(f'x: {self.rect.x} y: {self.rect.y} w: {self.rect.width} h:{self.rect.height}')
        return (self.rect.x + self.rect.width // 2 - 50), (self.rect.y + self.rect.height // 2 - 50)


class Ally(Character):
    def __init__(self, name = 'Void', max_HP = 0, max_SP = 0, crystal = Crystal(), weapon = Weapon(), armor = Armor(), img_path = 'assets/images/iconPlaceholder.png'):
        super().__init__(name, max_HP, max_SP, crystal, weapon)
        self.armor = armor
        self.icon = pygame.transform.scale(load_image(img_path), (100, 100))

    def take_damage(self, incoming_damage):
        result = 0
        evade_odds = self.bonuses['AG'] * self.Ag // 2
        if randchek(evade_odds):
            return 0
        
        if self.crystal.weak_resist[incoming_damage.type] == -1:
            self.weakness_bonus = 1.5
            result = 1
        elif self.crystal.weak_resist[incoming_damage.type] == 1:
            self.weakness_bonus = 0.2
        
        taken_damage = round((incoming_damage * self.weakness_bonus) // (self.bonuses['DEF'] * (self.En + self.armor.defense) ** 0.5)) + 1
        self.HP -= taken_damage
        if self.HP <= 0:
            self.HP = 0
            self.state = False
        self.battle_card.update()
        self.weakness_bonus = 1
        self.bonuses['ATK'] = 1
        self.bonuses['DEF'] = 1
        self.bonuses['AG'] = 1
        return result
    
    def guard(self):
        self.bonuses['DEF'] *= 2

    def use_item(self):
        pass


class MainCharacter(Ally):
    def __init__(self, name = 'Void', max_HP = 0, max_SP = 0, crystal = Crystal(), weapon = Weapon(), armor = Armor(), img_path = 'assets/images/iconPlaceholder.png'):
        super().__init__(name, max_HP, max_SP, crystal, weapon, armor, img_path)
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
    group = pygame.sprite.Group()
    en = Enemy('churka', 25, c1, wp)
    group.add(en)
    en.rect.x = 100
    en.rect.y = 100
    f = AttackAbility("Agi", 4, 'Ma', 'fire', 50)


    pygame.init()
    size = width, height = config.WIDTH, config.HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        group.draw(screen)
        pygame.display.flip()
        clock.tick(config.FPS)