import pygame
import party
import characters
from equipment import Crystal, Weapon, Armor
from additonals import randchek
from visuals import draw_battle_layout
import sys

class Battle:
    def __init__(self, team1:party.PlayerParty, team2:party.EnemyParty):
        self.team1 = team1
        self.team2 = team2
        if randchek(75):
            print('Player Andvantage!')
            self.current_team = self.team1
            self.target_team = self.team2
        else:
            print('Enemy Andvantage!')
            self.current_team = self.team2
            self.target_team = self.team1
    
    def fight_process(self, screen):
        self.action_card, self.battle_cards = draw_battle_layout(screen, self.team1)
        while (not self.team1.isDead) and (not self.team2.isDead):
            self.battle_round()


    def change_team(self):
        self.current_team = self.team1 if self.current_team == self.team2 else self.team2
        self.target_team = self.team1 if self.target_team == self.team2 else self.team2

    def battle_round(self):
        for char in self.current_team.members:
            print(char.name)
            char.battle_card.active()
            pygame.display.flip()
            self.make_turn(char)
            char.battle_card.inactive()
            pygame.display.flip()

        self.change_team()

        for char in self.current_team.members:
            print(char.name)
            self.make_turn(char)   


    def make_turn(self, char):
        if type(self.current_team) == party.PlayerParty:

            choiceFlag = False
            while not choiceFlag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            self.action_card.change_chosen(1)
                        elif event.key == pygame.K_UP:
                            self.action_card.change_chosen(-1)
                        elif event.key == pygame.K_z:
                            action = self.action_card.return_value().lower()
                            print(action)
                            if action == 'attack':
                                target = self.choose_target()
                                if target == 0:
                                    continue
                                char.weapon_attack(target)
                                print(f'{target.HP}/{target.MaxHP}')
                                return 1
                            elif action == 'use skill':
                                skill = self.choose_ability(char)
                                if skill == 0:
                                    continue
                                target = self.choose_target()
                                if target == 0:
                                    continue
                                char.use_skill(skill, target)
                                print(f'{target.HP}/{target.MaxHP}')
                                return 2
                            elif action == 'guard':
                                char.guard()
                                return 3

                pygame.display.flip()
        else:
            print('Hee ho!')

    def choose_target(self):
        target_index = 0
        choiceFlag = False
        while not choiceFlag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print('left')
                    elif event.key == pygame.K_RIGHT:
                        print('right')
                    elif event.key == pygame.K_x:
                        return 0
        # while not chosen:
        #     for i, enemy in enumerate(self.target_team.members):
        #         print(f'{i + 1}. {enemy}')
        #     answer = int(input())
        #     if 0 < answer <= len(self.target_team.members):
        #         chosen = True
        # return self.target_team.members[answer - 1]
    
    def choose_ability(self, char):
        chosen = False
        while not chosen:
            for i, skill in enumerate(char.crystal.abilities):
                print(f'{i + 1}. {skill}')
            answer = int(input())
            if 0 < answer < self.target_team:
                chosen = True
        return char.crystal.abilities[answer - 1]
        