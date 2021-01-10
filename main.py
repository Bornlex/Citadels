# coding: utf-8

import sys
import uuid
import random
import logging

from src import player as ply

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

NAMES = [
    "Jean",
    "Charles",
    "Francois",
    "Julien",
    "Antoine",
    "Christine",
    "Pierre",
    "Mariel",
    "Jerome",
    "Thomas",
    "Didier"
]

ASSASSIN = 0
THIEF = 1
MAGICIAN = 2
KING = 3
BISHOP = 4
SALESMAN = 5
ARCHITECT = 6
CONDOTTIERE = 7
CHARACTERS_ORDER = {
    0: "Assassin",
    1: "Voleur",
    2: "Magicien",
    3: "Roi",
    4: "Eveque",
    5: "Marchand",
    6: "Architecte",
    7: "Condottiere"
}
CHARACTERS = list(CHARACTERS_ORDER.values())


def count_points(players):
    max_points = 0
    winner = None
    for player in players:
        points = player.count_points()
        if points > max_points:
            winner = player
            max_points = points
    return winner


def pop_character(characters):
    selected = random.choice(characters)
    characters.remove(selected)
    return selected, characters


def play(players):
    logger.info(f"[game][*] starting...")
    turn = 1
    while True:
        logger.info(f"[{turn}] new turn...")
        over = False
        available_characters = CHARACTERS.copy()
        logger.info(f"[{turn}][*] players choosing characters")
        characters_to_players = {}
        players_to_characters = {}
        if len(players) == 4:
            selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] first character removed: {selected}")
            selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] second character removed: {selected}")
            invisibly_selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] invisibly character removed: {invisibly_selected}")
        elif len(players) == 5:
            selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] second character removed: {selected}")
            invisibly_selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] invisibly character removed: {invisibly_selected}")
        elif len(players) == 6:
            invisibly_selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] invisibly character removed: {invisibly_selected}")
        else:
            invisibly_selected, available_characters = pop_character(available_characters)
            logger.info(f"[{turn}][?] invisibly character removed: {invisibly_selected}")
        for player in players:
            chosen = player.choose_characters(available_characters)
            characters_to_players[chosen] = player
            players_to_characters[player.name] = chosen
            available_characters.remove(chosen)
        for character in CHARACTERS:
            logger.info(f"[{turn}][?] {character} is called!")
            if character not in characters_to_players:
                logger.info(f"[{turn}][?] {character} either not in list or dead")
                continue
            to_play = characters_to_players[character]
            to_play.play_turn()
            if len(to_play.buildings) == 7:
                logger.info(f"[{turn}] a player achieved building 7 buildings")
                over = True
        if over:
            break
        logger.info(f"[{turn}][?] end of turn")
        for player in players:
            player.reset()
    winner = count_points(players)
    logger.info(f"[game] the winner is: {winner.name}")


if __name__ == "__main__":
    players_number = 6
    players = [ply.Player(str(uuid.uuid4())) for i in range(players_number)]
    play(players)
