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

def battle_screen(team1 = 0, team2 = 0):
    c = equipment.Crystal()
    c1 = equipment.Crystal()
    agi = abt.AttackAbility('Agi', 30, 'Ma', 'Слабая атака огнём', 'fire', 10)
    bufu = abt.AttackAbility('Bufu', 4, 'Ma', 'Слабая атака льдом', 'ice', 15)
    garu = abt.AttackAbility('Garu', 4, 'Ma', 'Слабая атака ветром', 'wind', 15)
    dia = abt.HealAbility("Dia", 5, 'Ma', 50, 'Исцеление небольшого количества здоровья союзнику')
    abilities = [agi, bufu, dia, agi, agi, garu]
    c1.abilities = abilities
    c.weak_resist['ice'] = -1
    c.weak_resist['fire'] = 1
    wp = equipment.Weapon(50, 90)
    team = party.PlayerParty([characters.MainCharacter('Joker', 125, 75, c1, wp), characters.Ally('Skull', 150, 50, c1, wp), characters.Ally('Panther', 95, 100, c1, wp), characters.Ally('Queen', 100, 95, c1, wp)])
    en_team = party.EnemyParty([characters.Enemy('Jack Frost', 100, 5, 70, c1, wp), characters.Enemy('Pyro Jack', 75, 5, 70, c1, wp), characters.Enemy('King Frost', 150, 5, 20, c1, wp), characters.Enemy('Shit eater', 10, 5, 15, c1, wp)])
    

    BATTLE_FINISHED = False
    sequence = create_sequence(team, en_team)
    active_id = 0
    enemies_sprites = pygame.sprite.Group()
    battle_cards = pygame.sprite.Group()
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
        result = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            
            elif event.type == pygame.KEYDOWN and type(sequence[active_id]) != characters.Enemy:
                result = action_frame.key_events(event.key)
                print(result)

        if type(sequence[active_id]) == characters.Enemy:
            if randchek(sequence[active_id].attack_odds):
                result = sequence[active_id].attack_character(team.members)
            else:
                result = sequence[active_id].support_ally(en_team.members)

        if result == 'next':
            sequence[active_id].isActive = False
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
                
        screen.fill(pygame.Color("black"))
        battle_cards.draw(screen)
        battle_cards.update()
        enemies_sprites.draw(screen)
        if action_frame.CHOOSING_ENEMY:
            service_group.draw(screen)
        service_group.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    battle_screen()