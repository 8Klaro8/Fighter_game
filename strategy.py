class Strategy:
    def __init__(self) -> None:
        self.actions = [{"Action": "Attack", "Points": 3},
                        {"Action":"Defense", "Points": 2},
                        {"Action":"Run", "Points": 1}] 
        
        self.events = [{"Event": "Fight nearby", "Points": 2},
                       {"Event": "Low Hp", "Points": 1},
                       {"Event": "In corner", "Points": 1}] 
        
        self.strategies = []
        self.points_sum = 0
        self.max_points = 8
        self.options = [{"OptionName": "Choose Strategy", "Function": self._ask_user_for_strategy},
                        {"OptionName": "Fight", "Function": self._fight},
                        {"OptionName": "Check points", "Function": self._check_points},
                        {"OptionName": "Quit", "Function": quit}]

    def main_stategy(self):
        while True:
            self._show_options()
            # self._ask_user_for_strategy()

    def _fight(self):
        print("FIGHT")

    def _check_points(self):
        print(f"\n------------------------\n"
              f"Your total points: {self.points_sum}"
              "\n------------------------")

    def _show_options(self):
        print("\n------------------------\nOptions\n")
        for i in range(len(self.options)):
            print(f"{i+1}.) {self.options[i]['OptionName']}")
        
        chosen_option = int(input("Choose an option...")) - 1
        chosen_function = self.options[chosen_option]['Function']
        chosen_function()

    def _ask_user_for_strategy(self):
        """ Asks user for input """
        strategy = {}
        temp_point_sum = 0

        self._display_actions()
        action = int(input("\nChoose an action... ")) - 1
        self._display_events()
        event = int(input("\nChoose an event... ")) - 1

        # select actions
        chosen_action = self.actions[action]["Action"]
        chosen_event = self.events[event]["Event"]
        # calculate action points
        temp_point_sum += self.actions[action]["Points"]
        temp_point_sum += self.events[event]["Points"]

        strategy["Action"] = chosen_action
        strategy["Event"] = chosen_event
        strategy["Points"] = temp_point_sum


        if not self._is_strategy_added(strategy):
            # save strategy
            self.strategies.append(strategy)
            # save point sum
            self.points_sum += temp_point_sum

            print(f"\n------------------------\nChosen strategy -- Do: {strategy['Action']} |"
                                        f" When: {strategy['Event']} |"
                                        f" Costs: {strategy['Points']}")
            print(f"Total cost: {self.points_sum}")
            # checks if points exceeds max
            if not self._check_points_sum():
                print("Your action points exceeds the max...")
                print("Your total points: ", self.points_sum)
                print("Max available points: ", self.max_points)
                self._delete_strategy()

        else:
            print("Strategy already added...")

    def _display_actions(self):
        """ Dispalys avaialble actions """
        print("\n------------------------\nActions")
        for i in range(len(self.actions)):
            if i == (len(self.actions) - 1):
                print(f"{i + 1}.) {self.actions[i]['Action']}, costs: {self.actions[i]['Points']}")
            else:
                print(f"{i + 1}.) {self.actions[i]['Action']}, costs: {self.actions[i]['Points']}\n", end="")

    def _display_events(self):
        """ Dispalys avaialble events """
        print("\nEvents")
        for i in range(len(self.events)):
            if i == (len(self.events) - 1):
                print(f"{i + 1}.) {self.events[i]['Event']}, costs: {self.events[i]['Points']}")
            else:
                print(f"{i + 1}.) {self.events[i]['Event']}, costs: {self.events[i]['Points']}\n", end="")

    def _check_points_sum(self) -> bool:
        """ checks if the collected points reaches max points """
        if self.points_sum >= self.max_points:
            return False
        return True
    
    def _delete_strategy(self):
        """ Deletes the chosen strategy """
        print("\nYour strategy...")
        for i in range(len(self.strategies)):
            print(f"{i + 1}.) Action: {self.strategies[i]['Action']}\t"
                    f"Event: {self.strategies[i]['Event']}\t"
                    f"Cost: {self.strategies[i]['Points']}")
        
        to_delete = int(input("\nDelete strategy...")) - 1
        # delete points from total
        points_to_delete = self.strategies[to_delete]['Points']
        self.points_sum -= points_to_delete
        # print and remove strategy
        print(f"{to_delete + 1} Action: {self.strategies[to_delete]['Action']} {self.strategies[to_delete]['Event']} has been removed...")
        self.strategies.pop(to_delete)

    def _is_strategy_added(self, strategy: dict) -> bool:
        if strategy in self.strategies:
            return True
        return False
            
        



if __name__ == '__main__':
    strategy = Strategy()
    strategy.main_stategy()