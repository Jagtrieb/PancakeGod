import pygame
import characters
import party
import equipment
import additonals
import visuals
import battle
import abilities
import config
import sys

def terminate():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    size = width, height = config.WIDTH, config.HEIGHT
    screen = pygame.display.set_mode(size)
    c = equipment.Crystal(50)
    c1 = equipment.Crystal(75)
    wp = equipment.Weapon(50, 90)
    team = party.PlayerParty([characters.MainCharacter('Joker', 125, c1, wp), characters.Ally('Skull', 150, c), characters.Ally('Panther', 95, c1), characters.Ally('Queen', 100, c1)])
    en_team = party.EnemyParty([characters.Enemy('Jack Frost', 100), characters.Enemy('Pyro Jack', 75), characters.Enemy('King Frost', 150)])
    

    clock = pygame.time.Clock()
    fight = battle.Battle(team, en_team, screen, clock)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        fight.fight_process()
        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == '__main__':
    main()