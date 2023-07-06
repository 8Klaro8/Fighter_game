



class DuelManager:
    def __init__(self, fighters: list) -> None:
        self.actions = ["Fight", "Defend", "Run"]
        self.events = ["Fighter nearby", "2 fighters nearby", "In corner"]
        self.fighters = fighters
        self.extra_defense = 1
        self.miss_chance = 5

    def process_fight(self):
        """ Applies run and defense action and
        proceses fight """
        self._process_actions()
        self._process_duel()

    def _process_actions(self):
        """ If defense or run is chosen as action,
        then updats these attributes """
        for fighter in self.fighters:
            fighter._reset_defaults()
            strategy_payload = fighter.strategy
            print(strategy_payload)
            for strategy in strategy_payload:
                action = strategy["Action"]
                if action == "Run":
                    if not fighter._boost_miss_chance:
                        print("Raise chance of not getting hit")
                        fighter._boost_miss_chance(self.miss_chance)
                        break
                elif action == "Defend":
                    if not fighter._defense_boosted:
                        fighter._boost_defense(self.extra_defense)
                        break

    def _process_duel(self):
        """ If the fighters meet then process their duel """
        is_duel_done = False
        while not is_duel_done:
            for fighter in self.fighters:
                for fighter_2 in self.fighters:
                    if fighter != fighter_2:
                        fighter._attack(fighter_2)
                        fighter_2._attack(fighter)
                        is_duel_done = True
                        print("Duel's Done!")
                        print("Fighter 1 health: ", fighter.health)
                        print("Fighter 2 health: ", fighter_2.health)
                        break
                break
            break

# FIGHTER 1:  [{'Action': 'Fight', 'Event': 'Fighter nearby'}]  
# FIGHTER 2:  [{'Action': 'Defend', 'Event': 'Fighter nearby'}]