
import keyboard


class ChooseStrategy:
    def __init__(self) -> None:
        self.actions = ["Aggressive", "Defend", "Run"]
        # self.events = ["Fighter nearby", "2 fighters nearby", "In corner"]
        self.events = ["1on2", "In corner", "below 50% Hp"]
        self.strategies = []
        self.options = {1: ["Choose strategy", self.show_strategies],
                        2: ["Go to Fight!", self._fight]}
        self.is_fight = False

    def _go_back_function(self, input:str):
        """ Calls the corresponding fucntion where to go back """
        if input.lower() == 'back':
            return True
        return False
    
    def _logout_function(self, input:str):
        """ Calls the corresponding fucntion where to go back """
        if input.lower() == 'logout':
            return True
        return False

    def _control_user_input(self, input):
        """ Controls if user choosed a valid option
        on the validation screen """
        try:
            input = int(input)
            try:
                self.options[input][1]()
            except:
                self._print_prompt("Invalid number...")
                self.choose_option()
                # self._receive_user_auth_choice()
        except:
            self._print_prompt("Please give a valid choice...")
            self.choose_option()
            # self._receive_user_auth_choice()
        
    def choose_option(self) -> list:
        print("\nType 'logout' to log out\n--------------------")
        print("\n------------------------\n"
              "Options:")
        for i in range(len(self.options)):
            print(f"{i+1}.) {self.options[i+1][0]}")

        chosen_option = input("Choose an option...")
        if self._logout_function(chosen_option):
            self._print_prompt("Logging out...")
            return "Logout"

        self._control_user_input(chosen_option)

        # calling chosed option
        # self.options[chosen_option][1]()

        # if already pressed fight then return staregies
        if self.is_fight:
            return self.strategies
        
        # return "Logout"

    def _fight(self):
        if len(self.strategies) <= 0:
            self._print_prompt("Can't fight without choosing stategy!")
            self.choose_option()
        if not self.is_fight:
            self._print_prompt("FIGHT")
            self.is_fight = True

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
            self.choose_option()

        else:
            self._print_prompt("Your chosen strategy already exists.")
            self.choose_option()
            
        # print(self.strategies)
        # self.choose_option()

    def _print_prompt(self, text):
        print("\n------------------------\n"
                f"{text}"
                "\n------------------------\n")

    def _strategy_added(self, strategy) -> bool:
        """ Checks if strategy action, event pair
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