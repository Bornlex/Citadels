# coding: utf-8

import random


class Player:
    def __init__(self, name, strategy, environment):
        self._name = name
        self._gold = 2
        self._buildings = []
        self._character = None
        self._strategy = strategy
        self._environment = environment
        super(Player, self).__init__()

    def count_points(self):
        points = 0
        colors = []
        for building in self.buildings:
            points += building.value
            colors.append(building.color)
        if list(set(colors)) == 5:
            points += 3
        return points

    def choose_characters(self, available_characters):
        chosen = random.choice(available_characters)
        self._character = chosen
        return chosen

    def reset(self):
        self._character = None

    def play_turn(self):
        """
        Either:
        - takes 2 gold
        - draws 2 cards, keep 1

        Then can:
        - build
        - use special skill
        """
        state = self._environment.get_state()
        self._strategy.act(state)

    @property
    def buildings(self):
        return self._buildings

    @property
    def name(self):
        return self._name
