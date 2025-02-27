import pygame
import characters
import party
import equipment
from additonals import randchek
import visuals
import abilities as abt
from new_batle import create_sequence
import config
import sys

size = width, height = config.WIDTH, config.HEIGHT
FPS = config.FPS
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()

def update_team_state(got_team):
        for i in got_team.members:
            if i.state != 'dead':
                return 0
        return 1

def battle_screen(team1 = 0, team2 = 0):
    c = equipment.Crystal()
    c1 = equipment.Crystal()
    agi = abt.AttackAbility('Agi', 30, 'Ma', 'Слабая атака огнём', 'fire', 30)
    bufu = abt.AttackAbility('Bufu', 4, 'Ma', 'Слабая атака льдом', 'ice', 30)
    garu = abt.AttackAbility('Garu', 4, 'Ma', 'Слабая атака ветром', 'wind', 25)
    dia = abt.HealAbility("Dia", 5, 'Ma', 50, 'Исцеление небольшого количества здоровья союзнику')
    abilities = [agi, bufu, dia, garu]
    c1.abilities = abilities
    c.weak_resist['ice'] = -1
    c.weak_resist['fire'] = 1
    abilities = [agi, dia, garu]
    c.abilities = abilities
    wp = equipment.Weapon(50, 90)
    team = party.PlayerParty([characters.MainCharacter('Joker', 125, 75, c1, wp), characters.Ally('Skull', 150, 50, c1, wp), characters.Ally('Panther', 95, 100, c1, wp), characters.Ally('Queen', 100, 95, c1, wp)])
    en_team = party.EnemyParty([characters.Enemy('Jack Frost', 10, 5, 95, c, wp), characters.Enemy('Pyro Jack', 15, 5, 70, c, wp)])
    

    BATTLE_FINISHED = False
    sequence = create_sequence(team, en_team)
    active_id = 0
    service_group = pygame.sprite.Group()

    action_frame, battle_cards, enemies_sprites = visuals.draw_battle_layout(screen, team, en_team)
    sequence[active_id].isActive = True
    action_frame.set_active_char(sequence[active_id])
    service_group.add(action_frame)
    
    if type(sequence[active_id]) != characters.Enemy:
        action_frame.default_state()
    else:
        action_frame.awaiting_state()

    while not BATTLE_FINISHED:
        result = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            
            elif event.type == pygame.KEYDOWN and type(sequence[active_id]) != characters.Enemy:
                result = action_frame.key_events(event.key)
                #print(result)

        if type(sequence[active_id]) == characters.Enemy:
            if randchek(sequence[active_id].attack_odds):
                result = sequence[active_id].attack_character(team.members)
            else:
                result = sequence[active_id].support_ally(en_team.members)

        
        if result == 'died':
            if update_team_state(en_team):
                return 'Victory'



        if result == 'next':
            sequence[active_id].isActive = False
            # while sequence[active_id].state == 'dead':
            active_id += 1
            if active_id == len(sequence):
                active_id = 0
            sequence[active_id].isActive = True
            action_frame.default_state()
            action_frame.set_active_char(sequence[active_id])
            if type(sequence[active_id]) != characters.Enemy:
                action_frame.default_state()
            else:
                action_frame.awaiting_state()
        
        if result == 'player_victory':
            return 'Victory'

        screen.fill(pygame.Color("black"))
        battle_cards.draw(screen)
        battle_cards.update()
        enemies_sprites.draw(screen)
        if action_frame.CHOOSING_ENEMY:
            service_group.draw(screen)
        service_group.update()
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(text_to_render):
    screen.fill('black')
    while True:
        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 35)
        text = font.render(text_to_render, True, ('white'))
        screen.blit(text, (config.WIDTH // 2 - font.size(f'{text}')[0] // 2, config.WIDTH // 2 - font.size(f'{text}')[1] // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    screen.fill('black')
    while True:
        font = pygame.font.Font('data/fonts/PressStart2P-Regular.ttf', 25)
        text = font.render('The legend of unfinished JRPG', True, ('white'))
        screen.blit(text, (150, 250))
        text = font.render('Press any button to start', True, ('yellow'))
        screen.blit(text, (200, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return 1
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    start_screen()
    battle_result = battle_screen()
    end_screen(f'{battle_result}')
