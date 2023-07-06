



class DuelManager:
    def __init__(self, fighters: list) -> None:
        self.actions = ["Fight", "Defend", "Run"]
        self.events = ["Fighter nearby", "2 fighters nearby", "In corner"]
        self.fighters = fighters
        self.extra_defense = 1
        self.attack_deduct_by_def = 1
        self.miss_chance = 8

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
                        print(f"Fighter '{fighter.name}' - health: {fighter.health}, "
                                f"attack: {fighter.attack}, "
                                f"defense: {fighter.defense}, "
                                f"miss chance: {fighter.miss_chance}")
                        print(f"Fighter '{fighter_2.name}' health: {fighter_2.health}, "
                                f"attack: {fighter_2.attack}, "
                                f"defense: {fighter_2.defense}, "
                                f"miss chance: {fighter_2.miss_chance}")
                        if is_duel_done:
                            break
                break
            break

# FIGHTER 1:  [{'Action': 'Fight', 'Event': 'Fighter nearby'}]  
# FIGHTER 2:  [{'Action': 'Defend', 'Event': 'Fighter nearby'}]