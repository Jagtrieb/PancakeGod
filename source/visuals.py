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
        self.screen.blit(text, (self.offset_X + 10, self.offset_Y + 10))

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

        self.CHOOSING_ENEMY = False
        self.CHOOSING_ACTION = False
        self.CHOOSING_SKILL = False
        self.HINT_ACTIVE = False

        
        self.hint_frame = (config.HINT_X, config.HINT_Y, config.ACTION_WIDTH, config.HINT_HEIGHT)
        self.hint_font_size = config.HINT_FONT_SIZE
        self.hint_font = pygame.font.Font('data/fonts/Arsenal-Regular.ttf', self.hint_font_size)
        self.hint_text = ''

        self.indent = 20

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
        self.HINT_ACTIVE = False
    
    def awaiting_state(self):
        self.CHOOSING_ENEMY = False
        self.CHOOSING_ACTION = False
        self.CHOOSING_SKILL = False
        self.HINT_ACTIVE = False

    def split_text(self, raw_text):
        available_space = (self.hint_frame[2] - 10) * 0.9
        text_parts = []
        raw_words = raw_text.split()
        while len(raw_words) > 0:
            string = ''
            while (len(string) * self.hint_font_size * config.HINT_FONT_CORRECTIVE_K) < available_space:
                if len(raw_words) == 0:
                    break
                string = string[:] + raw_words.pop(0) + ' '
            text_parts.append(string)
        return text_parts
    
    def change_hint_text(self, raw_text):
        self.hint_text = self.split_text(raw_text)

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

    def draw_hint(self):
        pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), self.hint_frame)
        pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.hint_frame, 5)
        x = self.hint_frame[0] + self.hint_frame[2] * 0.1
        y = self.hint_frame[1] + self.hint_frame[3] * 0.1 
        interval = self.hint_font_size // 2 + self.hint_font_size
        for part in self.hint_text:
            text = self.hint_font.render(part, True, ('white'))
            self.screen.blit(text, (x, y))
            y += interval

    def update(self):
        self.rect.x, self.rect.y = self.enemies.members[self.chosen_enemy].sprite_center()
        if self.CHOOSING_ACTION or self.CHOOSING_SKILL:
            pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)
            x = config.ACTION_X + 15
            y = config.ACTION_Y + self.indent
            font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 20 if self.CHOOSING_ACTION else 16)
            length = len(self.current_list) if len(self.current_list) < self.skill_lines else self.skill_lines
            margin = (config.ACTION_HEIGHT - 2 * self.indent) // (length * 2 - 1)  

            for i in range(length):
                text = font.render(f'{self.current_list[i + self.shift]}', True, ('white') if self.chosen_option != i + self.shift else ('yellow'))
                self.screen.blit(text, (x, y))
                if self.CHOOSING_SKILL:
                    text = font.render(f'{self.current_list[i + self.shift].cost} SP', True, (226, 129, 205))
                    self.screen.blit(text, (config.ACTION_WIDTH * config.SP_COST_SHIFT + config.ACTION_X - text.get_size()[0], y))
                y += 2 * margin
        if self.HINT_ACTIVE:
            #print(self.current_list[self.chosen_option].description)
            self.change_hint_text(self.current_list[self.chosen_option].description)
            self.draw_hint()

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
                self.default_state()
            elif self.current_list[self.chosen_option] == 'Use Skill':
                self.chosen_option = 0
                self.shift = 0
                self.current_list = self.active_char.crystal.abilities
                self.CHOOSING_ENEMY = False
                self.CHOOSING_ACTION = False
                self.CHOOSING_SKILL = True
                self.HINT_ACTIVE = True
            elif self.CHOOSING_SKILL:
                self.CHOOSING_ENEMY = True
                self.CHOOSING_SKILL = False
                self.HINT_ACTIVE = False
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
                self.HINT_ACTIVE = True
                self.CHOOSING_ENEMY = False

            elif self.CHOOSING_SKILL:
                self.default_state()
            return 'back'

    def return_value(self):
        return self.actions[self.chosen]

def draw_battle_layout(screen, player_team, enemy_team):
    a_frame = ActionFrame((config.ACTION_X, config.ACTION_Y, config.ACTION_WIDTH, config.ACTION_HEIGHT), config.ACTIONS, screen, enemy_team)
    screen.fill((0, 0, 0))
    battle_cards = draw_battle_cards(screen, player_team)
    a_frame.update()
    enemies = draw_enemies(screen, enemy_team)
    return a_frame, battle_cards, enemies


def draw_battle_cards(screen, team = None):
    cards_margin = (config.CARDS_AREA_WIDTH - len(team.members) * config.CARD_WIDTH) // (len(team.members) + 1)
    cards = pygame.sprite.Group()
    y = config.HEIGHT * config.ACTION_SHIFT - config.CARD_HEIGHT
    for i, char in enumerate(team.members):
        x = i * (config.CARD_WIDTH + cards_margin) + cards_margin
        card = CharacterFrame((x, y, config.CARD_WIDTH, config.CARD_HEIGHT), char, screen)
        card.rect.x = card.offset_X + 5
        card.rect.y = card.offset_Y + 25
        card.update()
        cards.add(card)
        team.members[i].battle_card = card
    return cards

def draw_enemies(screen, team = None):
    enemies_sprite_group = pygame.sprite.Group()
    enemy_margin = config.EN_FRAME_WIDTH // (len(team.members) * 2 + 2)
    x = enemy_margin
    for member in team.members:
        member.rect.x = x
        member.rect.y = config.EN_START_Y - member.rect.height
        enemies_sprite_group.add(member)
        x += 2 * enemy_margin
    enemies_sprite_group.draw(screen)
    return enemies_sprite_group
