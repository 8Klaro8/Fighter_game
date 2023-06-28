import socket, json, threading, time, queue
from Database.database import Database
from Authentication.auth import Authentication
from Fighter.fighter import Fighter

# class OutgoingQueue:
#     def __init__(self) -> None:
#         self.outgoing_queue = queue.Queue()

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

    def _create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print("Server is listening...")

        self._accept_new_connections()
        # self._register_user()

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

            send_data_thread = threading.Thread(target=self._tick_data,
                                                args=(client, ))
            send_data_thread.start()

            # move_fighter_thread = threading.Thread(target=self._move_fighter)
            # move_fighter_thread.start()

    def _receive_data(self, client):
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                data = self._read_json(data.decode('utf-8'))
                print("RECEIVED DATA: ", data)

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
                        print("Logged in!")
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
                    fighter = Fighter(fighter_name, strategy)
                    self.fighters.append(fighter) # append created fihter to all fighter
                    # send all client all fighter pos
                    self._broadcast_fighters_pos(client)

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
                    print("USERRS: ", self.connected_users)
                break
                # else:
                #     print(f"{client} has left...")
                #     for user in self.connected_users:
                #         if client == user["Client"]:
                #             self.connected_users.remove(user)

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
        # self.outgoing_queue.put(fighter_details_if)

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
        user_exists_if = {"Type": "Fail", "Payload": ["User already exists."]}
        successful_reg_if = {"Type": "Successful", "Payload": ["Successful registration!"]}
        # test_register_payload = {"Type": "Register",
        #                          "Payload": [{"Username": "Kakao", "Password": "123"}]}
        
        if not self._user_exists(test_register_payload):
            print("Saving new user...")
            self.database._save_user(test_register_payload)
            self.outgoing_queue.put(successful_reg_if)
            client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))
        else:
            self.outgoing_queue.put(user_exists_if)
            print("User already exists...")
            client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))


    def _tick_data(self, client):

        while True:
            time.sleep(2)
            fighters_pos_data = {"Type": "FighterUpdatePos", "Payload": []}
            
            for fighter in self.fighters:
                current_fighter = [fighter.name, fighter.pos[0], fighter.pos[1]]
                fighters_pos_data["Payload"].append(current_fighter)
            self.outgoing_queue.put(fighters_pos_data)

            try:
                # TODO send for only logged in uers
                if client in self.sent_strategy_by_client:
                    client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))
                    self.outgoing_queue.task_done()

            except:
                for user in self.connected_users:
                    if user["Client"] == client:
                        self.connected_users.remove(user)

            finally:
                self.outgoing_queue.get()
                self.outgoing_queue.task_done()

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
    
    # def _read_users_json(self) -> dict | None:
    #     with open("users.json", "r") as file:
    #         try:
    #             content = json.load(file)
    #         except json.JSONDecodeError:
    #             print("Users file is empty.")
    #             return None
    #     return content


test_data = {"Type": "Register",
             "Payload": [{"Username": "Kakao", "Password": "123"}]}
if __name__ == '__main__':
    server_socket = ServerSocket(6060, "localhost")
    server_socket._create_socket()
    # server_socket._accept_new_connections()
    # server_socket._register_user(test_data)

    
