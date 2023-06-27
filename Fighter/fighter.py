import random

class Fighter:
    def __init__(self, name, strategy) -> None:
        self.health = 10
        self.name = name
        self.attack = 3
        self.defense = 1
        self.strategy = strategy
        self.pos = ()
        self._random_pos()

    def _attack(self):
        """ Attacks other fighter """
        pass

    def _can_attack(self):
        pass

    def _resurrect_fighter(self):
        pass

    def _random_pos(self):
        """ Saves a random position for a fighter """
        x_pos = random.randint(0,5)
        y_pos = random.randint(0,5)
        self.pos = (x_pos, y_pos)