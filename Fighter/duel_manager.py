import random



class DuelManager:
    def __init__(self, fighters: list) -> None:
        self.actions = ["Fight", "Defend", "Run"]
        self.events = ["1on1", "1on2", "In corner", "below 50% Hp"]
        self.fighters = fighters
        self.extra_defense = 1
        self.attack_deduct_by_def = 1
        self.miss_chance = 8
        self.fighter_orig_health = 14
        self.bonus_attack_range = [1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
        self.is_duel_done = False
        self.bonus_dmg_added = False
        self.fought_this_round = False

    def _get_rand_bonus_dmg(self) -> int:
        """ Selects a random number as bonus dmg """
        return random.choice(self.bonus_attack_range)

    def process_fight(self):
        """ Applies run and defense action and
        proceses fight """
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
                strat["Event"] == "below 50% Hp":
                if fighter.health <= self.fighter_orig_health / 2:
                    fighter._boost_miss_chance(self.miss_chance)
                    self._print_prompt(f"'{fighter.name}' BELOW 50% - health: {fighter.health}")
                    
            elif strat["Action"] == "Defend" and \
                    strat["Event"] == "In corner":
                if fighter.pos == (0,0) or \
                    fighter.pos == (3,0) or \
                    fighter.pos == (0,3) or \
                    fighter.pos == (3,3):
                        fighter._boost_defense(self.extra_defense,
                                            self.attack_deduct_by_def)
                        self._print_prompt("IN CORNER")
                            
            elif strat["Action"] == "Run" and \
                    strat["Event"] == "1on2":
                if len(self.fighters) > 2:
                    print(f"---1ON2---{fighter.name}")
                    fighter._boost_miss_chance(self.miss_chance)

    def _print_prompt(self, text):
        print("\n------------------------\n"
                f"{text}"
                "\n------------------------\n")

    def _process_all_strategies(self):
        """ Processes all fighters strategy """
        for fighter in self.fighters:
            self._process_fighters_strategies(fighter)

    def _add_bonus_dmg_once(self):
        """ Adds and prints bonus dmg per round """
        for fighter in self.fighters:
            bonus_dmg_1 = self._get_rand_bonus_dmg()
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

    def _add_bonus_dmg(self, fighter, fighter_2):
        """ Adds and prints bonus dmg per round """
        bonus_dmg_1 = self._get_rand_bonus_dmg()
        fighter._add_bonus_dmg(bonus_dmg_1)
        print(f"'{fighter.name}' bonus dmg is: {bonus_dmg_1}")

        bonus_dmg_2 = self._get_rand_bonus_dmg()
        fighter_2._add_bonus_dmg(bonus_dmg_2)
        print(f"'{fighter_2.name}' bonus dmg is: {bonus_dmg_2}")

        self.bonus_dmg_added = True

    def _print_involed_fighters(self):
        """ Prints out the invloved fighters """
        print("\n---Fight Result---")
        for fighter in self.fighters:
            print(f"'{fighter.name}', health: {fighter.health}")
        print("----------------\n")

# FIGHTER 1:  [{'Action': 'Fight', 'Event': 'Fighter nearby'}]  
# FIGHTER 2:  [{'Action': 'Defend', 'Event': 'Fighter nearby'}]