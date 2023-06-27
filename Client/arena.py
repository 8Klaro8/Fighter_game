import sys, random



class Map:
    """ Prints out the map in the terminal and processes
    & dispalys new status of the map"""
    def __init__(self) -> None:
        self.coordinates = None
        self.map_size = {"x": 6, "y": 6}
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
        for i in range(len(self.map_array)):
            for j in range(len(self.map_array[i])):
                if j == (len(self.map_array[i]) - 1):
                    print("\n_______________")
                else:
                    print(self.map_array[i][j], end="")

    def _place_fighter(self, fighters):
        # for fighter in fighters:
        #     name = fighter[0]
        #     x_pos = fighter[1]
        #     y_pos = fighter[2]
            # print("FIGHTERS: ", fighters, x_pos, y_pos)

        column_array = []
        for row in range(self.map_size["y"]):
            for column in range(self.map_size["x"]):
                for fighter in fighters:
                    name = fighter[0]
                    x_pos = fighter[1]
                    y_pos = fighter[2]
                    
                    if row == y_pos and column == x_pos:
                        column_array.append(f" {name[:1]}|")
                    else:
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