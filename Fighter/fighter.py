import random

class Fighter:
    def __init__(self, name, strategy, client) -> None:
        self.health = 16 # must be even
        self.moving_range = 1
        self.name = name
        self.attack = 3
        self.attack_deduct_by_def = 1
        self.defense = 1
        self.extra_def = 1
        self.miss_chance = 1 # represent %
        self.extra_miss_chance = 8
        self.strategy = strategy
        self.pos = ()
        self.move_updated = False
        self._defense_boosted = False
        self._miss_chance_boosted = False
        self.matching_client = client
        self.bonus_attack_range = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
        self._random_pos()

    def _get_rand_bonus_dmg(self) -> int:
        """ Selects a random number as bonus dmg """
        return random.choice(self.bonus_attack_range)

    def _add_bonus_dmg(self, bonus_dmg):
        self.attack = self.attack + bonus_dmg

    def _add_agressive_behaviour(self):
        """ Adds bonus dmg randomly and deducts the same value from defense """
        aggressive_random_num = self._get_rand_bonus_dmg()
        new_defense = (self.defense - aggressive_random_num)
        if new_defense >= 0:
            self.defense = new_defense
            self.attack = self.attack + aggressive_random_num
            print("---aggressive behaviour---")
        else:
            # if new_defense is negative then deduct it from health
            self.defense = 0
            self.attack = self.attack + aggressive_random_num
            self.health = self.health - abs(new_defense)
            print("---aggressive behaviour minus health---")


    def _boost_defense(self):
        """ Boosts defense and deducts from attack """
        self.defense += self.extra_def # boost defense
        self.attack -= self.attack_deduct_by_def # deduct from attack becase of def
        self._defense_boosted = True

    def _boost_miss_chance(self):
        """ Boosts the chance to perry dmg """
        self.miss_chance += self.extra_miss_chance
        self.attack = random.randint(0,1)
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
                print(f"\n---DIED---'{self.name}'")
        else:
            # perried but still gets dmg if defnded_dmg is greater than 0
            self.defense = (self.defense + 1) # if perried attack then +1 defense
            defended_dmg = dmg - self.defense # defend dmg
            if defended_dmg > 0:
                self.health = self.health - defended_dmg
                print(f"\n---Perried---'{self.name}'")
            else:
                print("---NO DMG: defens greater than dmg---")

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
        """ Returns true if fighter is on edge """
        if self.pos[0] >= self.moving_range:
            return True
        return False
    
    def _is_on_edge_x_min(self) -> bool:
        """ Returns true if fighter is on edge """
        if self.pos[0] <= 0:
            return True
        return False
    
    def _is_on_edge_y_max(self) -> bool:
        """ Returns true if fighter is on edge """
        if self.pos[1] >= self.moving_range:
            return True
        return False
    
    def _is_on_edge_y_min(self) -> bool:
        """ Returns true if fighter is on edge """
        if self.pos[1] <= 0:
            return True
        return False

    def _random_pos(self) -> list:
        """ Initializes a random position for a fighter """
        x_pos = random.randint(0,self.moving_range)
        y_pos = random.randint(0,self.moving_range)
        self.pos = [x_pos, y_pos]