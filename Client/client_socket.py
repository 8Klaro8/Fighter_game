

import socket, json, threading, random
from Authentication.auth import Authentication
from Client.strategy import ChooseStrategy
from Client.arena import Map


class ClientSocket:
    def __init__(self, port, host) -> None:
        self.PORT = port
        self.HOST = host
        self.client_socket = None
        self.auth = Authentication()
        self.choose_strategy = ChooseStrategy()
        self.map = Map()
        self.fighters_details = []

    def _create_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

    def _receive_data(self):
        while True:
            received_data = self.client_socket.recv(1024)
            if not received_data:
                break
            
            received_data = self._read_json(received_data.decode('utf-8'))
            if received_data["Type"] == "FighterUpdatePos":
                self.fighters_details = []
                # check how much fighters are there
                self._set_map_size_by_player_num(received_data)
                
                for fighter in received_data["Payload"]:
                    name = fighter[0]
                    x_pos = fighter[1]
                    y_pos = fighter[2]
                    fighter_list = [name, x_pos, y_pos]
                    print("FIGHT_LIST: ", fighter_list)
                    if fighter_list not in self.fighters_details:
                        self.fighters_details.append(fighter_list)
                # print map with fighters on it
                self.map._place_fighter(self.fighters_details)
                self.map._print_map()

            elif received_data["Type"] == "Fail":
                print("\n---------------------------\n"
                      f"{received_data['Payload'][0]}"
                      "\n---------------------------")
                self._send_data()

            elif received_data["Type"] == "Logged":
                print(received_data["Payload"][0])
                # calling strategy
                strategy_if = {"Type": "Strategy", "Payload": []}
                strategy = self.choose_strategy.choose_option()
                print("SENDING STRATEGY: ", strategy)
                # send strategy to server
                # append each chosen strategy to if.
                for strat in strategy:
                    strategy_if["Payload"].append(strat)
                print(strategy_if)
                # strategy_if["Payload"].append(strategy[0])
                self.client_socket.send(self._jsonify_data(strategy_if).encode('utf-8'))                

            elif received_data["Type"] == "Fighters":
                print(f"\n{received_data['Payload']}")
                # save fighters
                self.fighters_details = []
                # get out name, and positions from each fighter to draw the map
                for fighter in received_data["Payload"]:
                    name = fighter["Name"]
                    x_pos = fighter["Pos"][0]
                    y_pos = fighter["Pos"][1]
                    fighter_list = [name, x_pos, y_pos]
                    if fighter_list not in self.fighters_details:
                        self.fighters_details.append(fighter_list)
                # print map with fighters on it
                self.map._place_fighter(self.fighters_details)
                self.map._print_map()

            elif received_data["Type"] == "Successful":
                print(f"\n{received_data['Payload']}")
                self._send_data()

            elif received_data["Type"] == "Died":
                print("You Died!")
                strategy_if = {"Type": "Strategy", "Payload": []}
                strategy = self.choose_strategy.choose_option()
                print("SENDING STRATEGY: ", strategy)
                # send strategy to server
                strategy_if["Payload"].append(strategy[0])
                self.client_socket.send(self._jsonify_data(strategy_if).encode('utf-8'))     

            else:
                print("DATA: ", received_data)

    def _set_map_size_by_player_num(self, received_data):
        if len(received_data["Payload"]) <= 2:
            self.map.map_size['x'] = 2
            self.map.map_size['y'] = 2
            print("MAP SIZE 2: ", self.map.table_size)
        elif len(received_data["Payload"]) <= 3:
            self.map.map_size['x'] = 4
            self.map.map_size['y'] = 4
        elif len(received_data["Payload"]) <= 5:
            self.map.map_size['x'] = 5
            self.map.map_size['y'] = 5

    def _send_data(self):
        # data = {"Type": "Action", "Strategy": "YOYO"}
        # self.client_socket.send(self._jsonify_data(data).encode('utf-8'))

        # register req.
        self.auth._show_logic_if()
        credentials_payoad = self.auth._receive_user_input()
        self.client_socket.send(self._jsonify_data(credentials_payoad).encode('utf-8'))
        credentials_payoad["Payload"] = []

    def _jsonify_data(self, data: dict) -> json:
        return json.dumps(data)
    
    def _read_json(self, data) -> bool:
        # TODO dont send data if fighter is dead
        return json.loads(data)


if __name__ == '__main__':
    client_socket = ClientSocket(port=6060, host="localhost")
    client_socket._create_socket()
    
    receive_thread = threading.Thread(target=client_socket._receive_data)
    receive_thread.start()
    send_thread = threading.Thread(target=client_socket._send_data)
    send_thread.start()