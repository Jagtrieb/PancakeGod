import pygame
import party
import characters
from equipment import Crystal, Weapon, Armor
from additonals import randchek, load_image
from visuals import draw_battle_layout
import config
import sys

class Battle:
    def __init__(self, team1:party.PlayerParty, team2:party.EnemyParty, screen = None, clock = None):
        self.team1 = team1
        self.team2 = team2
        self.screen = screen
        self.clock = clock
        self.service_sprites_group = pygame.sprite.Group()
        self.crosshair = pygame.sprite.Sprite(self.service_sprites_group)
        self.crosshair.image = pygame.transform.scale(load_image(config.CROSSHAIR), (100, 100))
        self.crosshair.rect = self.crosshair.image.get_rect()

        if randchek(75):
            print('Player Andvantage!')
            self.current_team = self.team1
            self.target_team = self.team2
        else:
            print('Enemy Andvantage!')
            self.current_team = self.team2
            self.target_team = self.team1
    
    def fight_process(self):
        self.action_card, self.battle_cards = draw_battle_layout(self.screen, self.team1, self.team2)
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
                self.clock.tick(config.FPS)
        else:
            print('Hee ho!')

    def choose_target(self):
        target_index = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        target_index += 1 if target_index + 1 < len(self.target_team.members) else 0
                    elif event.key == pygame.K_LEFT:
                        target_index -= 1 if target_index - 1 >= 0 else 0
                    elif event.key == pygame.K_z:
                        draw_battle_layout(self.screen, self.team1, self.team2)
                        pygame.display.flip()
                        return self.target_team.members[target_index]
                    elif event.key == pygame.K_x:
                        draw_battle_layout(self.screen, self.team1, self.team2)
                        pygame.display.flip()
                        return 0
            self.crosshair.rect.x, self.crosshair.rect.y = self.team2.members[target_index].sprite_center()
            self.crosshair.rect.x -= self.crosshair.rect.width // 2
            self.crosshair.rect.y -= self.crosshair.rect.height // 2
            draw_battle_layout(self.screen, self.team1, self.team2)
            self.service_sprites_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(config.FPS)
    
    def choose_ability(self, char):
        chosen = False
        while not chosen:
            for i, skill in enumerate(char.crystal.abilities):
                print(f'{i + 1}. {skill}')
            answer = int(input())
            if 0 < answer < self.target_team:
                chosen = True
        return char.crystal.abilities[answer - 1]
        