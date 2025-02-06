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
    team = party.PlayerParty([characters.MainCharacter('Joker', 125, c1), characters.Ally('Skull', 150, c), characters.Ally('Panther', 95, c1), characters.Ally('Queen', 100, c1)])
    fight = battle.Battle(team, team)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        fight.fight_process(screen)
        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == '__main__':
    main()