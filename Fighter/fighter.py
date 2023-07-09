import random

class Fighter:
    def __init__(self, name, strategy, client) -> None:
        self.health = 14
        self.moving_range = 3
        self.name = name
        self.attack = 3
        self.defense = 1
        self.miss_chance = 1 # represent %
        self.strategy = strategy
        self.pos = ()
        self.move_updated = False
        self._defense_boosted = False
        self._miss_chance_boosted = False
        self.matching_client = client
        self._random_pos()

    def _add_bonus_dmg(self, bonus_dmg):
        self.attack = self.attack + bonus_dmg

    def _boost_defense(self, extra_def: int, attack_deduct_by_def: int):
        """ Boosts defense and deducts from attack """
        self.defense += extra_def # boost defense
        self.attack -= attack_deduct_by_def # deduct from attack becase of def
        self._defense_boosted = True

    def _boost_miss_chance(self, extra_miss_chance):
        """ Boosts the chance to perry dmg """
        self.miss_chance += extra_miss_chance
        self.attack = 0 # set attack to 0 because of running
        self._miss_chance_boosted = True

    def _reset_defaults(self):
        """ resets all attributes to default """
        self.attack = 3
        self.miss_chance = 1
        self.defense = 1
        self._defense_boosted = False
        self._miss_chance_boosted = False

    def _perried_attack(self) -> bool:
        """ Returns True if missed """
        chance_of_getting_hit = random.randint(1,10)
        if chance_of_getting_hit <= self.miss_chance:
            return True
        return False
        # for num in range(1, (self.miss_chance + 1)):
        #     if num == chance_of_getting_hit:
        #         return True
        # return False

    def _attack(self, opponent):
        """ Attacks other fighter """
        opponent._get_damage(self.attack)

    def _get_damage(self, dmg: int):
        """ Receives dmg by other fighter """
        if not self._perried_attack():
            if self.defense > dmg:
                print(f"\n'{self.name}' DEFENDED ALL")
            else:
                defended_dmg = dmg - self.defense
                self.health = self.health - defended_dmg
            if self.health <= 0:
                print(f"\n'{self.name}' is ---DEAD---")
        else:
            print(f"\n'{self.name}' Perried!")

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
        if self.pos[0] >= self.moving_range:
            return True
        return False
    
    def _is_on_edge_x_min(self) -> bool:
        if self.pos[0] <= 0:
            return True
        return False
    
    def _is_on_edge_y_max(self) -> bool:
        if self.pos[1] >= self.moving_range:
            return True
        return False
    
    def _is_on_edge_y_min(self) -> bool:
        if self.pos[1] <= 0:
            return True
        return False

    def _random_pos(self) -> list:
        """ Saves a random position for a fighter """
        x_pos = random.randint(0,self.moving_range)
        y_pos = random.randint(0,self.moving_range)
        self.pos = [x_pos, y_pos]