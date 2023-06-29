import random

class Fighter:
    def __init__(self, name, strategy) -> None:
        self.health = 10
        self.name = name
        self.attack = 3
        self.defense = 1
        self.strategy = strategy
        self.pos = ()
        self.move_updated = False
        self._random_pos()

    def _attack(self, opponent):
        """ Attacks other fighter """
        opponent._get_damage(self.attack)

    def _get_damage(self, dmg: int):
        """ Receives dmg by other fighter """
        self.health = self.health - dmg
        if self.health <= 0:
            print("---DEAD---")

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
        random_choice_plus = [0, 1]

        next_move_x = None
        next_move_y = None

        if self._is_on_edge_x_max():
            next_move_x = random.choice(random_choice_zero)
            self.pos[0] = current_x + next_move_x

        elif self._is_on_edge_x_min():
            next_move_x = random.choice(random_choice_plus)
            self.pos[0] = current_x + next_move_x
        else:
            new_x = random.choice(random_choice_one)
            self.pos[0] = current_x + new_x

        if self._is_on_edge_y_max():
            next_move_y = random.choice(random_choice_zero)
            self.pos[1] = current_y + next_move_y

        elif self._is_on_edge_y_min():
            next_move_y = random.choice(random_choice_plus)
            self.pos[1] = current_y + next_move_y
        else:
            new_y = random.choice(random_choice_one)
            self.pos[1] = current_y + new_y

    def _is_on_edge_x_max(self) -> bool:
        if self.pos[0] >= 6:
            return True
        return False
    
    def _is_on_edge_x_min(self) -> bool:
        if self.pos[0] <= 0:
            return True
        return False
    
    def _is_on_edge_y_max(self) -> bool:
        if self.pos[1] >= 6:
            return True
        return False
    
    def _is_on_edge_y_min(self) -> bool:
        if self.pos[1] <= 0:
            return True
        return False

    def _random_pos(self) -> list:
        """ Saves a random position for a fighter """
        x_pos = random.randint(0,6)
        y_pos = random.randint(0,6)
        self.pos = [x_pos, y_pos]