



class DuelManager:
    def __init__(self, fighters: list) -> None:
        self.actions = ["Fight", "Defend", "Run"]
        self.events = ["Fighter nearby", "2 fighters nearby", "In corner"]
        self.fighters = fighters
        self.extra_defense = 1
        self.miss_chance = 50

    def process_fight(self):
        self._process_actions()
        self._process_duel()

    def _process_actions(self):
        """ If defense or run is chosen as action,
        then updats these attributes """
        for fighter in self.fighters:
            strategy_payload = fighter.strategy
            for strategy in strategy_payload["Action"]:
                for action in strategy:
                    if action == "Run":
                        print("Raise chance of not getting hit")
                        fighter.miss_chance = self.miss_chance
                    elif action == "Defend":
                        fighter.defense = fighter.defense + self.extra_defense
            action = strategy_payload[0]["Action"]

    def _process_duel(self):
        """ If the fighters meet then process their duel """
        for fighter in self.fighters:
            for fighter_2 in self.fighters:
                if fighter != fighter_2:
                    fighter._attack(fighter_2)
                    fighter_2._attack(fighter)
                    print("Duel's Done!")

# FIGHTER 1:  [{'Action': 'Fight', 'Event': 'Fighter nearby'}]  
# FIGHTER 2:  [{'Action': 'Defend', 'Event': 'Fighter nearby'}]