import pygame
import characters
import party
import equipment
import additonals
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
    agi = abt.AttackAbility('Agi', 3, 'Ma', 'fire', 10)
    bufu = abt.AttackAbility('Bufu', 4, 'Ma', 'ice', 15)
    garu = abt.AttackAbility('Garu', 4, 'Ma', 'wind', 15)
    abilities = [agi, bufu, bufu, agi, agi, garu]
    c1.abilities = abilities
    c1.weak_resist['phys'] = -1
    c.weak_resist['ice'] = -1
    c.weak_resist['fire'] = 1
    wp = equipment.Weapon(50, 90)
    team = party.PlayerParty([characters.MainCharacter('Joker', 125, 75, c1, wp), characters.Ally('Skull', 150, 50, c, wp), characters.Ally('Panther', 95, 100, c1, wp), characters.Ally('Queen', 100, 95, c1, wp)])
    en_team = party.EnemyParty([characters.Enemy('Jack Frost', 100, 5, c1), characters.Enemy('Pyro Jack', 75, 5, c), characters.Enemy('King Frost', 150), characters.Enemy('Shit eater', 10)])
    
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
    
    while not BATTLE_FINISHED:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            
            elif event.type == pygame.KEYDOWN and type(sequence[active_id]) != characters.Enemy:
                result = action_frame.key_events(event.key)
                print(result)
                if result == 'next':
                    sequence[active_id].isActive = False
                    active_id += 1
                    sequence[active_id].isActive = True
                    action_frame.set_active_char(sequence[active_id])
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