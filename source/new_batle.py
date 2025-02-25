import pygame
import party
import characters
from equipment import Crystal, Weapon, Armor
from additonals import randchek, load_image
from visuals import draw_battle_layout
import config
import sys


class Battle:
    def __init__(self, team1 = None, team2 = None):
        pass

def create_sequence(team1, team2):
    if randchek(75):
        print('Player Andvantage!')
        current_team = team1
        target_team = team2
    else:
        print('Enemy Andvantage!')
        current_team = team2
        target_team = team1
    return [*current_team.members, *target_team.members]

