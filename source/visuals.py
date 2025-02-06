import pygame
import config
import characters
from additonals import load_image

class UniversalFrame:
    def __init__(self, rect_value):
        self.frame = pygame.Rect((rect_value[0], rect_value[1], rect_value[2], rect_value[3]))
    
    def draw(self):
        pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)

class CharacterFrame(UniversalFrame):
    def __init__(self, rect_value, character=None, screen = None):
        super().__init__(rect_value)
        self.character = character
        self.screen = screen
        self.offset_X = self.frame.left
        self.offset_Y = self.frame.top
    
    def draw(self):
        pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)

        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 12)
        text = font.render(self.character.name, True, ('white'))
        self.screen.blit(text, (self.offset_X + 5, self.offset_Y + 10))

        self.screen.blit(self.character.icon, (self.offset_X + 5, self.offset_Y + 25))

        string_y = self.offset_Y + config.STATUS_STRING_Y
        text = font.render(f'HP {self.character.HP}/{self.character.MaxHP}', True, (116, 250, 161))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.HP / self.character.MaxHP * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (16, 150, 61), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (116, 250, 161), (self.offset_X + 10, string_y, hp_len, 15))

        string_y += 25
        text = font.render(f'SP {self.character.crystal.max_charge}/{self.character.crystal.charge}', True, (196, 99, 175))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.crystal.max_charge / self.character.crystal.charge * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (96, 0, 175), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (196, 99, 175), (self.offset_X + 10, string_y, hp_len, 15))

    def active(self):
        pygame.draw.rect(self.screen, pygame.Color('yellow'), self.frame, 5)
    
    def inactive(self):
        pygame.draw.rect(self.screen, pygame.Color('white'), self.frame, 5)

    def update(self):
        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 12)
        string_y = self.offset_Y + config.STATUS_STRING_Y
        text = font.render(f'HP {self.character.HP}/{self.character.MaxHP}', True, (116, 250, 161))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.HP / self.character.MaxHP * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (16, 150, 61), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (116, 250, 161), (self.offset_X + 10, string_y, hp_len, 15))

        string_y += 25
        text = font.render(f'SP {self.character.crystal.max_charge}/{self.character.crystal.charge}', True, (196, 99, 175))
        self.screen.blit(text, (self.offset_X + 10, string_y))
        string_y += 20
        hp_len = round(self.character.crystal.max_charge / self.character.crystal.charge * config.CARD_WIDTH * 0.85)
        pygame.draw.rect(self.screen, (96, 0, 175), (self.offset_X + 10, string_y, config.CARD_WIDTH * 0.85, 15))
        pygame.draw.rect(self.screen, (196, 99, 175), (self.offset_X + 10, string_y, hp_len, 15))

class ActionFrame(UniversalFrame):
    def __init__(self, rect_value, actions = [], screen = None):
        super().__init__(rect_value)
        self.actions = actions
        self.chosen_ind = 0
        self.screen = screen
        self.chosen = 0

        self.indent = 30
        self.margin = (config.ACTION_HEIGHT - self.indent) // (len(self.actions) * 2 - 1)
        
    def change_chosen(self, value):
        if (self.chosen + value) < len(self.actions) and (self.chosen + value) >= 0:
            self.chosen += value
            self.update()

    def draw(self):
        pygame.draw.rect(self.screen, pygame.Color((255, 255, 255)), self.frame, 5)
        self.update()
        # self.group.draw(self.screen)

    def update(self):
        x = config.ACTION_X + 15
        y = config.ACTION_Y + self.indent
        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 18)
        for i, action in enumerate(self.actions):
            text = font.render(action, True, ('white') if self.chosen != i else ('yellow'))
            self.screen.blit(text, (x, y))
            y += 2 * self.margin
    
    def return_value(self):
        return self.actions[self.chosen]


def draw_battle_layout(screen, team):
    a_frame = ActionFrame((config.ACTION_X, config.ACTION_Y, config.ACTION_WIDTH, config.ACTION_HEIGHT), config.ACTIONS, screen)
    screen.fill((0, 0, 0))
    battle_cards = draw_battle_cards(screen, team)
    a_frame.draw()
    return a_frame, battle_cards


def draw_battle_cards(screen, team = None):
    cards_margin = (config.WIDTH - len(team.members) * config.CARD_WIDTH) // (len(team.members) + 1)
    cards = []
    for i, char in enumerate(team.members):
        x = i * (config.CARD_WIDTH + cards_margin) + cards_margin
        card = CharacterFrame((x, config.HEIGHT - config.CARD_HEIGHT, config.CARD_WIDTH, config.CARD_HEIGHT), char, screen)
        card.draw()
        cards.append(card)
        team.members[i].battle_card = card
    return cards

def draw_enemies(screen, team = None):
    pass
