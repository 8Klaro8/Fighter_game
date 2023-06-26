



class ChooseStrategy:
    def __init__(self) -> None:
        self.actions = ["Fight", "Defend", "Run"]
        self.events = ["Fighter nearby", "2 fighters nearby", "In corner"]
        self.strategies = []
        self.options = {1: ["Choose strategy", self.show_strategies],
                        2: ["Go to Fight!", self._fight]}

    def choose_option(self):
        print("\n------------------------\n"
              "Options:")
        for i in range(len(self.options)):
            print(f"{i+1}.) {self.options[i+1][0]}")

        chosen_option = int(input("Choose an option..."))
        # calling chosed option
        self.options[chosen_option][1]()

    def _fight(self):
        if len(self.strategies) <= 0:
            self._print_prompt("Can't fight without choosing stategy!")
            return
        self._print_prompt("FIGHT")

    def show_strategies(self):
        print("\n------------------------\nActions")
        action = self.actions[self._print_strategy(self.actions)]
        print("\n------------------------\nEvents")
        event = self.events[self._print_strategy(self.events)]

        # save chosen strategy
        strategy = {"Action": None, "Event": None}
        strategy["Action"] = action
        strategy["Event"] = event

        if not self._strategy_added(strategy):
            self._print_prompt(f"Your chosen strategy\nDo: {action}\nWhen: {event}")
            self.strategies.append(strategy)

        else:
            self._print_prompt("Your chosen strategy already exists.")
            
        print(self.strategies)

    def _print_prompt(self, text):
        print("\n------------------------\n"
                f"{text}"
                "\n------------------------\n")
            

    def _strategy_added(self, strategy) -> bool:
        """ Checks if strategy -action, event pair
        has been already added """
        current_action = strategy["Action"]
        current_event = strategy["Event"]
        for strat in self.strategies:
            if strat["Action"] == current_action and \
                strat["Event"] == current_event:
                return True
        return False

    def _print_strategy(self, strategy: list) -> int:
        """ Prints avaialble action & events """
        print()
        for i in range(len(strategy)):
            print(f"{i+1}.) {strategy[i]}")
        if strategy == self.actions:
            return (int(input("Choose action...")) - 1)
        elif strategy == self.events:
            return (int(input("Choose event...")) - 1)
        
if __name__ == '__main__':
    chs = ChooseStrategy()
    while True:
        chs.choose_option()