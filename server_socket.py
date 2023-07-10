import socket, json, threading, time, queue, random
from Database.database import Database
from Authentication.auth import Authentication
from Fighter.fighter import Fighter
from Fighter.duel_manager import DuelManager 


class ServerSocket:
    def __init__(self, port, host) -> None:
        self.PORT = port
        self.HOST = host
        self.server_socket = None
        self.connected_users = [] # [{"Client": client, "Username": "yxc"}]
        self.database = Database()
        self.outgoing_queue = queue.Queue(10)
        self.auth = Authentication()
        self.fighters = []
        self.sent_strategy_by_client = []
        self.tick_counter = 0
        self.same_pos = []
        self.same_pos_added = False
        self.round_time = 1.5
        self.last_fighters_pos_data = []

    def _create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print("Server is listening...")
        self._accept_new_connections()

    def _accept_new_connections(self):
        while True:
            client, addr = self.server_socket.accept()
            if client not in self.connected_users:
                print("Adding new client...")
                self.connected_users.append({"Client": client}) # saving client
            print(f"{addr} has connected.")

            receive_data_thread = threading.Thread(target=self._receive_data,
                                                   args=(client, ))
            receive_data_thread.start()

            send_data_thread = threading.Thread(target=self._tick_data)
            send_data_thread.start()

    def _receive_data(self, client):
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                data = self._read_json(data.decode('utf-8'))
                print("RECEIVED DATA: ", data)

                self._process_incoming_data(data, client)

            except WindowsError as e:
                try:
                    i = self._get_user_by_client(client)
                    left_username = self.connected_users[i]["Username"]
                    # delete fighter
                    for fighter in self.fighters:
                        if fighter.name == left_username:
                            self.fighters.remove(fighter)
                    print(f"'{left_username}' has left.")
                    # remove client
                    self.connected_users.pop(i)
                except Exception as ex:
                    print(f"{client} has left before login.")
                    print(ex)
                    # remove client
                    self.connected_users.pop(i)
                    print("USERS: ", self.connected_users)
                break

    def _process_incoming_data(self, data, client):
        if data["Type"] == "Register":
                print("Register request...")
                self._register_user(data, client)

        elif data["Type"] == "Login":
            print("Login request...")
            username = data["Payload"][0]["Username"]
            password = data["Payload"][0]["Password"]
            if not self.auth._auth_logging_user(username, password):
                print("Wrong password...")
                wrong_password_if = {"Type": "Fail",
                                        "Payload": ["Wrong password."]}
                self.outgoing_queue.put(wrong_password_if)
                client.send(self._jsonify_data(self.outgoing_queue.get())
                            .encode('utf-8'))
            else:
                loggedin_if = {"Type": "Logged",
                                "Payload": ["Successfuly logged in!"]}
                self.outgoing_queue.put(loggedin_if)
                client.send(self._jsonify_data(self.outgoing_queue.get())
                            .encode('utf-8'))
                self.outgoing_queue.task_done()
                print(f"'{username}' Logged in!")
                # saved logged in users
                i = self._get_user_by_client(client)
                self.connected_users[i]["Username"] = username

        elif data["Type"] == "Action":
            print("Action request...")

        elif data["Type"] == "Strategy":
            strategy = data["Payload"]
            print("RECEIEVING STRATEGY: ", strategy)
            # save strategy with clint to identify users who sent it already
            self.sent_strategy_by_client.append(client)
            # creating fighter
            i = self._get_user_by_client(client)
            fighter_name = self.connected_users[i]["Username"]
            fighter = Fighter(fighter_name, strategy, client)
            self.fighters.append(fighter) # append created fighter to all fighter

    def _broadcast_fighters_pos(self, client):
        """ Sends all fighters pos to clients """
        fighter_details_if = {"Type": "Fighters", "Payload": []}
        for fighter in self.fighters:
            fighter_details = {"Name": None, "Pos": None}
            pos = fighter.pos
            name = fighter.name
            fighter_details["Name"] = name
            fighter_details["Pos"] = pos
            fighter_details_if["Payload"].append(fighter_details)

        for i in range(len(self.connected_users)):
            if client in self.sent_strategy_by_client:
                self.connected_users[i]["Client"].send(self._jsonify_data(fighter_details_if)
                                                .encode('utf-8'))

    def _get_user_by_client(self, client) -> int:
        """ Returns the int that represents the corresponding user """
        for i in range(len(self.connected_users)):
            if self.connected_users[i]["Client"] == client:
                return i

    def _register_user(self, test_register_payload, client):
        """ Processes registering user. Either registers if not exists
        or sends user exists message. """
        user_exists_if = {"Type": "Fail", "Payload": ["User already exists."]}
        successful_reg_if = {"Type": "Successful", "Payload": ["Successful registration!"]}
        
        if not self._user_exists(test_register_payload):
            print("Saving new user...")
            self.database._save_user(test_register_payload)
            self.outgoing_queue.put(successful_reg_if)
            client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))
        else:
            self.outgoing_queue.put(user_exists_if)
            print("User already exists...")
            client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))

    def _tick_data(self):
        while True:
            # shuffle fighters to select fighters evenly
            random.shuffle(self.fighters)
            # set fighters move range depending on how much fighters are there
            self._set_moving_range_by_player_num()

            wait_list = []
            fighters_pos_data = {"Type": "FighterUpdatePos",
                                "Payload": [],
                                "PlayerNum": len(self.fighters)}
            self.same_pos_added = False

            # move fighters every 3rd tick
            if self.tick_counter >= 4:
                self._move_fighters()
                self._fighter_same_pos()
                duel_manager = DuelManager(self.same_pos)
                duel_manager.process_fight()
                self._process_fighter_payload(fighters_pos_data)
                self._check_liveness_of_fighters()

            self.tick_counter += 1 # add to tick counter 

            # for fighter in self.fighters:
            #     if fighter not in self.same_pos: # append new pos data if not in same pos
            #         current_fighter = [fighter.name, fighter.pos[0], fighter.pos[1]]
            #         fighters_pos_data["Payload"].append(current_fighter)
            #     else: # if two or more fighters meet then displays 'x' once! 
            #         if not self.same_pos_added:
            #             current_fighter = ["x", fighter.pos[0], fighter.pos[1]]
            #             fighters_pos_data["Payload"] = []
            #             fighters_pos_data["Payload"].append(current_fighter)
            #             self.same_pos_added = True

            self.same_pos = [] # reset same pos
            # set last fighter_pos_data to current to control if there was any change
            if self.tick_counter >= 2:
                self.last_fighters_pos_data = fighters_pos_data
            wait_list.append(fighters_pos_data) # add data to temp. holder
            if len(wait_list[0]["Payload"]) > 0: # checks if payload is not empty
                if not self._check_if_same_pos_but_diff_symbol(fighters_pos_data):
                    if not self._check_if_playload_has_x_only(fighters_pos_data):
                        try:
                            # if client in self.sent_strategy_by_client:
                            if fighters_pos_data["PlayerNum"] > 1:
                                if self.last_fighters_pos_data != fighters_pos_data:
                                    print("MOVING RANGE", self.fighters[0].moving_range)
                                    for cli in self.sent_strategy_by_client:
                                        cli.send(self._jsonify_data(wait_list[0]).encode('utf-8'))
                            elif fighters_pos_data["PlayerNum"] == 1:
                                # for cli in self.sent_strategy_by_client:
                                self.sent_strategy_by_client[0].send(self._jsonify_data(wait_list[0]).encode('utf-8'))
                                    # cli.send(self._jsonify_data(wait_list[0]).encode('utf-8'))
                        except:
                            pass
            time.sleep(self.round_time)

    def _process_fighter_payload(self, fighters_pos_data):
        for fighter in self.fighters:
            if fighter not in self.same_pos: # append new pos data if not in same pos
                current_fighter = [fighter.name, fighter.pos[0], fighter.pos[1]]
                fighters_pos_data["Payload"].append(current_fighter)
            else: # if two or more fighters meet then displays 'x' once! 
                if not self.same_pos_added:
                    current_fighter = ["x", fighter.pos[0], fighter.pos[1]]
                    fighters_pos_data["Payload"] = []
                    fighters_pos_data["Payload"].append(current_fighter)
                    self.same_pos_added = True

    def _check_if_playload_has_x_only(self, fighters_pos_data):
        """ Returns true if payload contains only an 'x' """
        if fighters_pos_data["PlayerNum"] == 1 and \
            fighters_pos_data["Payload"][0][0] == "x":
            return True
        return False


    def _set_moving_range_by_player_num(self):
        if len(self.fighters) <= 2:
            for fighter in self.fighters:
                fighter.moving_range = 1
        elif len(self.fighters) <= 3:
            for fighter in self.fighters:
                fighter.moving_range = 3
        elif len(self.fighters) <= 5:
            for fighter in self.fighters:
                fighter.moving_range = 4

    def _check_if_same_pos_but_diff_symbol(self, fighters_pos_data) -> bool:
        """ If there are more fighters in the payload
        with the same postion, then return True"""
        if len(fighters_pos_data["Payload"]) > 1:
            for data_1 in fighters_pos_data["Payload"]:
                for data_2 in fighters_pos_data["Payload"]:
                    if data_1 != data_2 and \
                        data_1[1] == data_2[1] and \
                            data_1[2] == data_2[2]:
                        return True
        return False

    def _move_fighters(self):
        """ Moves all fighters to a random position
        (one step to a close field) and resets tick counter """
        for fighter in self.fighters:
                fighter._random_moving()
        self.tick_counter = 0 # 'reset' tick counter
        # TODO put tick_counter outside

    def _set_same_post_to_all_fighter(self):
        for fighter in self.fighters:
            fighter.pos = [0,0]

    def _fighter_same_pos(self):
        """ Puts fighters in a list if they are at the same position """
        # self._set_same_post_to_all_fighter()
        for fighter in self.fighters:
            for fighter_2 in self.fighters:
                if fighter.pos == fighter_2.pos and fighter != fighter_2:
                    if not self._fighter_in_same_pos(fighter):
                        self.same_pos.append(fighter)
                    if not self._fighter_in_same_pos(fighter_2):
                        self.same_pos.append(fighter_2)

        # duel_manager = DuelManager(self.same_pos)
        # duel_manager.process_fight()
        # self._check_liveness_of_fighters()

    def _check_liveness_of_fighters(self):
        """ Removes fighter if health is <= 0 """
        death_if = {"Type": "Died", "Payload": ["Your fighter died."]}
        wait_list = []
        wait_list.append(death_if)

        for fighter in self.fighters:
            if fighter.health <= 0:
                # sending death signal to user
                dead_user = fighter.matching_client
                dead_user.send(self._jsonify_data(wait_list[0])
                            .encode('utf-8'))
                self.fighters.remove(fighter)
                self.sent_strategy_by_client.remove(dead_user)
                print()

    def _fighter_in_same_pos(self, fighter) -> bool:
        """ Checks if fighter is already appended in self.same_pos"""
        fighter_name = fighter.name
        for fighter in self.same_pos:
            same_pos_fighter_name = fighter.name
            if fighter_name == same_pos_fighter_name:
                return True
        return False

    def _user_exists(self, register_payload) -> bool:
        """ Checks if user already exists """
        content = None
        content = self.database._read_users_json()
        if content == None:
            return False
        username = register_payload['Payload'][0]['Username']
        for user in content['Users']:
            if user['Username'] == username:
                return True
        return False

    def _jsonify_data(self, data: dict) -> json:
        return json.dumps(data)
    
    def _read_json(self, data) -> bool:
        return json.loads(data)


test_data = {"Type": "Register",
             "Payload": [{"Username": "Kakao", "Password": "123"}]}
if __name__ == '__main__':
    server_socket = ServerSocket(6060, "localhost")
    server_socket._create_socket()
    # server_socket._accept_new_connections()
    # server_socket._register_user(test_data)

    
