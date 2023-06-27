import sys, random



class Map:
    """ Prints out the map in the terminal and processes
    & dispalys new status of the map"""
    def __init__(self) -> None:
        self.coordinates = None
        self.map_size = {"x": 7, "y": 7}
        self.map_array = []

    def _update_map(self):
        """ Updates the status of the map """
        pass

    def _create_map(self):
        """ Prints the map to the terminal """
        column_array = []
        for row in range(self.map_size["y"]):
            for column in range(self.map_size["x"]):
                column_array.append("  |")
            self.map_array.append(column_array)
            column_array = []

    def _print_map(self):
        """ Prints out the map """
        print()
        for i in range(len(self.map_array)):
            for j in range(len(self.map_array[i])):
                if j == (len(self.map_array[i]) - 1):
                    print("\n______________________")
                else:
                    print(self.map_array[i][j], end="")
        self.map_array = []

    def _place_fighter(self, fighters):

        column_array = []
        added_this_round = False
        added_in_a_fighters_round = False
        for row in range(self.map_size["y"]):
            for column in range(self.map_size["x"]):
                added_in_a_fighters_round = False
                added_this_round = False

                for fighter in fighters:
                    if fighter[1] == column and fighter[2] == row:
                        column_array.append(f" {fighter[0][:1]}|")
                        added_this_round = True

                if not added_this_round and not added_in_a_fighters_round:
                    column_array.append("  |")
                    added_in_a_fighters_round = True

            if column == 7:
                column_array.append("  |")

            self.map_array.append(column_array)
            column_array = []

    def _place_fighter1(self, fighters):
        # TODO fix map!
        # fighter_data = []
        # for fighter in fighters:
        #     name = fighter[0]
        #     x_pos = fighter[1]
        #     y_pos = fighter[2]

            # fighter_data.append([name, x_pos, y_pos])
            # print("FIGHTERS: ", fighters, x_pos, y_pos)

        # fighters = [['a', 0, 0]]
        # fighters = [['a', 0, 0], ['b', 0, 1], ['c', 1, 1]]

        column_array = []
        _name_added = False
        for row in range(self.map_size["y"]):
            for column in range(self.map_size["x"]):
                _name_added = False
                if len(fighters) == 0:
                    if not _name_added and len(column_array) <= 7:
                        column_array.append("  |")
                        _name_added = False

                    if len(fighters) == 1 and column == 6:
                        column_array.append("  |")

                for fig in fighters:
                    _added_this_round = False
                    _name_added = False
                    if row == fig[2] and column == fig[1] and len(column_array) <= 7:
                        column_array.append(f" {fig[0][:1]}|")
                        fighters.remove(fig)
                        _name_added = True
                    # else:
                    if not _name_added and len(column_array) <= 7:
                        column_array.append("  |")
                        _name_added = False
                        _added_this_round = True

                    if len(fighters) == 1 and column == 6 and len(column_array) <= 7 and not _added_this_round:
                        column_array.append("  |")

            self.map_array.append(column_array)
            column_array = []

    # def _random_pos(self) -> tuple:
    #     """ Returns a random position for a fighter """
    #     x_pos = random.randint(0,5)
    #     y_pos = random.randint(0,5)
    #     return (x_pos, y_pos)


if __name__ == '__main__':
    map = Map()
    map._create_map()
    map._print_map()