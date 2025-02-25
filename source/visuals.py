import pygame
import config
import characters
from additonals import load_image

class UniversalFrame(pygame.sprite.Sprite):
    def __init__(self, rect_value, img_path = 'assets/images/iconPlaceholder.png', img_size = (100, 100)):
        super().__init__()
        self.image = pygame.transform.scale(load_image(img_path), img_size)
        self.rect = self.image.get_rect()
        self.frame = pygame.Rect((rect_value[0], rect_value[1], rect_value[2], rect_value[3]))
    
    def update(self):
        pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)

class HintFrame(UniversalFrame):
    def __init__(self, rect_value, text, img_path='assets/images/iconPlaceholder.png', img_size=(100, 100)):
        super().__init__(rect_value, img_path, img_size)
        self.text = text
        self.isActive = False
    
    def update(self, screen):
        if self.isActive:
            pygame.draw.rect(screen, pygame.Color((255, 255, 255)), self.frame, 5)
            font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 12)
            text = font.render(self.text, True, (116, 250, 161))
            self.screen.blit(text, (self.frame[0] + 10, self.frame[1] + 10))


class CharacterFrame(UniversalFrame):
    def __init__(self, rect_value, character=None, screen = None):
        super().__init__(rect_value)
        self.character = character
        self.screen = screen
        self.offset_X = self.frame.left
        self.offset_Y = self.frame.top
        self.color = pygame.Color('white')
    

    def update(self):
        self.color = pygame.Color('yellow') if self.character.isActive else pygame.Color('white')
        pygame.draw.rect(self.screen, self.color, self.frame, 5)

        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 12)
        text = font.render(self.character.name, True, ('white'))
        self.screen.blit(text, (self.offset_X + 5, self.offset_Y + 10))

        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 12)
        string_y = self.offset_Y + config.STATUS_STRING_Y
        text = font.render(f'HP {self.character.HP}/{self.character.MaxHP}', True, (116, 250, 161))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.HP / self.character.MaxHP * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (16, 150, 61), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (116, 250, 161), (self.offset_X + 10, string_y, hp_len, 15))

        string_y += 25
        text = font.render(f'SP {self.character.SP}/{self.character.MaxSP}', True, (196, 99, 175))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.SP / self.character.MaxSP * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (96, 0, 175), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (226, 129, 205), (self.offset_X + 10, string_y, hp_len, 15))

class ActionFrame(UniversalFrame):
    def __init__(self, rect_value, actions = [], screen = None, enemy_team = None, character = None, img_path='assets/images/crosshair.png', img_size=(100, 100)):
        super().__init__(rect_value, img_path, img_size)
        self.actions = actions
        self.screen = screen
        self.chosen_option = 0
        self.chosen_enemy = 0
        self.current_list = self.actions

        self.active_char = character
        self.enemies = enemy_team
        self.screen = screen

        self.skill_lines = 6
        self.shift = 0

        self.CHOOSING_ENEMY = True
        self.CHOOSING_ACTION = True
        self.CHOOSING_SKILL = False

        self.indent = 20

    def set_active_char(self, new_active_character):
        self.active_char = new_active_character

    def change_chosen_action(self, value):
        if (self.chosen_option + value) < len(self.current_list) and (self.chosen_option + value) >= 0:
            self.chosen_option += value
            if self.chosen_option >= self.skill_lines:
                self.shift += 1
            elif self.chosen_option < self.shift:
                self.shift -= 1
            self.update()
    
    def change_chosen_enemy(self, value):
        if (self.chosen_enemy + value) < len(self.enemies.members) and (self.chosen_enemy + value) >= 0:
            self.chosen_enemy += value
            self.update()

    def update(self):
        self.rect.x, self.rect.y = self.enemies.members[self.chosen_enemy].sprite_center()
        if self.CHOOSING_ACTION or self.CHOOSING_SKILL:
            pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)
            x = config.ACTION_X + 15
            y = config.ACTION_Y + self.indent
            font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 18)
            length = len(self.current_list) if len(self.current_list) < self.skill_lines else self.skill_lines
            margin = (config.ACTION_HEIGHT - 2 * self.indent) // (length * 2 - 1)  

            for i in range(length):
                text = font.render(f'{self.current_list[i + self.shift]}', True, ('white') if self.chosen_option != i + self.shift else ('yellow'))
                self.screen.blit(text, (x, y))
                y += 2 * margin

    def default_state(self):
        self.chosen_option = 0
        self.chosen_enemy = 0
        self.current_list = self.actions
        self.CHOOSING_ENEMY = True
        self.CHOOSING_ACTION = True
        self.shift = 0
        self.CHOOSING_ENEMY = True
        self.CHOOSING_ACTION = True
        self.CHOOSING_SKILL = False

    def key_events(self, key):
        if key == pygame.K_DOWN:
            self.change_chosen_action(1)
        elif key == pygame.K_UP:
            self.change_chosen_action(-1)
        elif key == pygame.K_RIGHT and self.CHOOSING_ENEMY:
            self.change_chosen_enemy(1)
        elif key == pygame.K_LEFT and self.CHOOSING_ENEMY:
            self.change_chosen_enemy(-1)

        elif key == pygame.K_z:
            print(self.current_list[self.chosen_option])
            command = ''
            if self.current_list[self.chosen_option] == "Attack":
                dmg, command = self.active_char.weapon_attack(self.enemies.members[self.chosen_enemy])
                #print(self.active_char)
                self.default_state()
            elif self.current_list[self.chosen_option] == 'Use Skill':
                self.chosen_option = 0
                self.shift = 0
                self.current_list = self.active_char.crystal.abilities
                self.CHOOSING_ENEMY = False
                self.CHOOSING_ACTION = False
                self.CHOOSING_SKILL = True
                #hint = HintFrame()
            elif self.CHOOSING_SKILL:
                self.CHOOSING_ENEMY = True
                self.CHOOSING_SKILL = False
                self.chosen_enemy = 0
            elif self.CHOOSING_ENEMY and not self.CHOOSING_ACTION and not self.CHOOSING_SKILL:
                dmg, command = self.active_char.use_skill(self.chosen_option, self.enemies.members[self.chosen_enemy])
                self.default_state()

            if command == 'one_more':
                print('ONE MORE!')
            return command
        elif key == pygame.K_x:
            if self.CHOOSING_ENEMY and not self.CHOOSING_ACTION:
                self.chosen_option = 0
                self.shift = 0
                self.current_list = self.active_char.crystal.abilities
                self.CHOOSING_SKILL = True
                self.CHOOSING_ENEMY = False

            elif self.CHOOSING_SKILL:
                self.chosen_option = 0
                self.shift = 0
                self.current_list = self.actions
                self.CHOOSING_SKILL = False
                self.CHOOSING_ACTION = True
                self.CHOOSING_ENEMY = True

    def return_value(self):
        return self.actions[self.chosen]

def draw_battle_layout(screen, player_team, enemy_team):
    a_frame = ActionFrame((config.ACTION_X, config.ACTION_Y, config.ACTION_WIDTH, config.ACTION_HEIGHT), config.ACTIONS, screen, enemy_team)
    #hint = HintFrame()
    screen.fill((0, 0, 0))
    battle_cards = draw_battle_cards(screen, player_team)
    a_frame.update()
    enemies = draw_enemies(screen, enemy_team)
    return a_frame, battle_cards, enemies


def draw_battle_cards(screen, team = None):
    cards_margin = (config.WIDTH - len(team.members) * config.CARD_WIDTH) // (len(team.members) + 1)
    cards = pygame.sprite.Group()
    for i, char in enumerate(team.members):
        x = i * (config.CARD_WIDTH + cards_margin) + cards_margin
        card = CharacterFrame((x, config.HEIGHT - config.CARD_HEIGHT, config.CARD_WIDTH, config.CARD_HEIGHT), char, screen)
        card.rect.x = card.offset_X + 5
        card.rect.y = card.offset_Y + 25
        card.update()
        cards.add(card)
        team.members[i].battle_card = card
    return cards

def draw_enemies(screen, team = None):
    enemies_sprite_group = pygame.sprite.Group()
    enemy_margin = config.EN_FRAME_WIDTH // (len(team.members) * 2 + 1)
    x = enemy_margin
    for member in team.members:
        member.rect.x = x
        member.rect.y = config.EN_START_Y
        enemies_sprite_group.add(member)
        x += 2 * enemy_margin
    enemies_sprite_group.draw(screen)
    return enemies_sprite_group

def update_screen(screen, a_frame, player_team, en_team):
    draw_battle_cards(screen, player_team)
    draw_enemies(screen, en_team)