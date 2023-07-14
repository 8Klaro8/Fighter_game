import random



class DuelManager:
    def __init__(self, fighters: list) -> None:
        self.actions = ["Aggressive", "Defend", "Run"]
        self.events = ["1on2", "In corner", "below 50% Hp"]
        self.fighters = fighters
        self.extra_defense = 1
        self.attack_deduct_by_def = 1
        self.miss_chance = 8
        self.fighter_orig_health = 14
        self.is_duel_done = False
        self.bonus_dmg_added = False
        self.fought_this_round = False
        self.corners = None
        self._set_corner_attribute()

    def _set_corner_attribute(self) -> dict | str:
        """ Checks the number of fighters
        and based on that it gets the map's size
        and from there it sets the corner attributes(pos) """
        corners = {
            "corner_1": None,
            "corner_2": None,
            "corner_3": None,
            "corner_4": None
            }
        fighters_num = len(self.fighters)
        if fighters_num <= 2:
            # self.corners = "---Map is too small---"
            corners["corner_1"] = [0,0]
            corners["corner_2"] = [1,0]
            corners["corner_3"] = [0,1]
            corners["corner_4"] = [1,1]
            self.corners = corners

        elif fighters_num <= 3:
            corners["corner_1"] = [0,0]
            corners["corner_2"] = [3,0]
            corners["corner_3"] = [0,3]
            corners["corner_4"] = [3,3]
            self.corners = corners

        elif fighters_num <= 5:
            corners["corner_1"] = [0,0]
            corners["corner_2"] = [4,0]
            corners["corner_3"] = [0,4]
            corners["corner_4"] = [4,4]
            self.corners = corners

    def _check_fighters_corner_pos(self, fighter) -> bool:
        """ Checks if the current fighter is in a corner """
        if type(self.corners) is dict: # checking if corners is a dict of pos datas
            if self.corners["corner_1"][0] == fighter.pos[0] and \
                self.corners["corner_1"][1] == fighter.pos[1]:
                return True
            elif self.corners["corner_2"][0] == fighter.pos[0] and \
                self.corners["corner_2"][1] == fighter.pos[1]:
                return True
            elif self.corners["corner_3"][0] == fighter.pos[0] and \
                self.corners["corner_3"][1] == fighter.pos[1]:
                return True
            elif self.corners["corner_4"][0] == fighter.pos[0] and \
                self.corners["corner_4"][1] == fighter.pos[1]:
                return True
        elif type(self.corners) is str:
            print("CORNER IS STR")
        return False

    def process_fight(self):
        """ Starts to process all necessary functions for fight """
        if len(self.fighters) > 1:
            self._process_all_strategies()
            self._add_bonus_dmg_once()
            self._process_duel()

    def _process_actions(self):
        """ If defense or run is chosen as action,
        then updats these attributes """
        for fighter in self.fighters:
            fighter._reset_defaults()
            strategy_payload = fighter.strategy
            for strategy in strategy_payload:
                action = strategy["Action"]
                if action == "Run":
                    if not fighter._miss_chance_boosted:
                        print("Raise chance of not getting hit")
                        fighter._boost_miss_chance(self.miss_chance)
                        break
                elif action == "Defend":
                    if not fighter._defense_boosted:
                        fighter._boost_defense(self.extra_defense, self.attack_deduct_by_def)
                        break

    def _process_fighters_strategies(self, fighter):
        """ Processes each strategy for the given fighter """
        fighter._reset_defaults() # reset default values before modify again
        for strat in fighter.strategy:
            if strat["Action"] == "Run" and \
                    strat["Event"] == "1on2":
                if len(self.fighters) > 2:
                    print(f"---1ON2---{fighter.name}")
                    fighter._boost_miss_chance(self.miss_chance)

            elif strat["Action"] == "Run" and \
                strat["Event"] == "In corner":
                if self._check_fighters_corner_pos(fighter):
                    fighter._boost_miss_chance(self.miss_chance)
                    self._print_prompt(f"'{fighter.name}' BELOW 50% - health: {fighter.health} - CORNER")

                    
            elif strat["Action"] == "Run" and \
                strat["Event"] == "below 50% Hp":
                if fighter.health <= self.fighter_orig_health / 2:
                    fighter._boost_miss_chance(self.miss_chance)
                    self._print_prompt(f"'{fighter.name}' BELOW 50% - health: {fighter.health}")

            elif strat["Action"] == "Defend" and \
                    strat["Event"] == "1on2":
                if len(self.fighters) > 2:
                    print(f"---DEFEND 1ON2---{fighter.name}")
                    fighter._boost_defense(self.extra_defense,
                                        self.attack_deduct_by_def)
                    
            elif strat["Action"] == "Defend" and \
                    strat["Event"] == "In corner":
                if self._check_fighters_corner_pos(fighter):
                    fighter._boost_miss_chance(self.miss_chance)
                    fighter._boost_defense(self.extra_defense,
                                        self.attack_deduct_by_def)
                    self._print_prompt(f"'{fighter.name}' DEFEND CORNER")
                    
            elif strat["Action"] == "Defend" and \
                    strat["Event"] == "below 50% Hp":
                if fighter.health <= self.fighter_orig_health / 2:
                    print(f"---DEFEND 50% HP---{fighter.name}")
                    fighter._boost_defense(self.extra_defense,
                                        self.attack_deduct_by_def)

            elif strat["Action"] == "Aggressive" and \
                    strat["Event"] == "1on2":
                if len(self.fighters) >= 3:
                    fighter._add_agressive_behaviour()
                    self._print_prompt("AGGRESSIVE")

            elif strat["Action"] == "Aggressive" and \
                    strat["Event"] == "In corner":
                if self._check_fighters_corner_pos(fighter):
                    fighter._boost_miss_chance(self.miss_chance)
                    fighter._add_agressive_behaviour()
                    self._print_prompt(f"'{fighter.name}' AGGRESSIVE CORNER")

            elif strat["Action"] == "Aggressive" and \
                    strat["Event"] == "below 50% Hp":
                fighter._add_agressive_behaviour()
                self._print_prompt("AGGRESSIVE")

    def _print_prompt(self, text):
        print("\n------------------------\n"
                f"{text}"
                "\n------------------------\n")

    def _process_all_strategies(self):
        """ Processes all fighters strategy """
        for fighter in self.fighters:
            self._process_fighters_strategies(fighter)

    def _add_bonus_dmg_once(self):
        """ Adds and prints bonus dmg per round for each fighter """
        for fighter in self.fighters:
            bonus_dmg_1 = fighter._get_rand_bonus_dmg()
            fighter._add_bonus_dmg(bonus_dmg_1)
            print(f"'{fighter.name}' bonus dmg is: {bonus_dmg_1}")
        
    def _process_duel(self):
        """ If the fighters meet then process their duel """
        # self.bonus_dmg_added = False # reset bonus dmg
        self.fought_this_round = False # reset fight round
        print("\nNew Fight\n----------------")
        for fighter in self.fighters:
            for fighter_2 in self.fighters:
                if fighter.name != fighter_2.name:
                    if not self.fought_this_round:
                        fighter._attack(fighter_2)
                        fighter_2._attack(fighter)
            self.fought_this_round = True

        self._print_involed_fighters()

    def _print_involed_fighters(self):
        """ Prints out the invloved fighters """
        print("\n---Fight Result---")
        for fighter in self.fighters:
            print(f"'{fighter.name}', health: {fighter.health}")
        print("----------------\n")
