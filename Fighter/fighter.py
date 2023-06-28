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

    def _random_moving(self):
        """ Sets the next randomic movemnt/ pos. """
        current_x = self.pos[0]
        current_y = self.pos[1]

        random_choice_zero = [0, -1]
        random_choice_one = [1, -1]

        next_move_x = None
        next_move_y = None

        if self._is_on_edge_x():
            next_move_x = random.choice(random_choice_zero)
            self.pos[0] = next_move_x
        else:
            new_x = random.choice(random_choice_one)
            self.pos[0] = new_x

        if self._is_on_edge_y():
            next_move_y = random.choice(random_choice_zero)
            self.pos[1] = next_move_y
        else:
            new_y = random.choice(random_choice_one)
            self.pos[1] = new_y

    def _is_on_edge_x(self) -> bool:
        if self.pos[0] == 6:
            return True
        return False
    
    def _is_on_edge_y(self) -> bool:
        if self.pos[1] == 6:
            return True
        return False

    def _random_pos(self) -> list:
        """ Saves a random position for a fighter """
        x_pos = random.randint(0,6)
        y_pos = random.randint(0,6)
        self.pos = [x_pos, y_pos]