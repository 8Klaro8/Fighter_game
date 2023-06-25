import socket, json, threading, time, queue
from Database.database import Database
from Authentication.auth import Authentication

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
                                       "Payload": ["Logged in!."]}
                        self.outgoing_queue.put(loggedin_if)
                        client.send(self._jsonify_data(self.outgoing_queue.get())
                                    .encode('utf-8'))
                        print("Logged in!")

                elif data["Type"] == "Action":
                    print("Action request...")
            except WindowsError:
                if len(self.connected_users) <= 0:
                    pass
                # else:
                #     print(f"{client} has left...")
                #     for user in self.connected_users:
                #         if client == user["Client"]:
                #             self.connected_users.remove(user)

    def _register_user(self, test_register_payload, client):
        user_exists_if = {"Type": "Fail", "Payload": ["User already exists."]}
        # test_register_payload = {"Type": "Register",
        #                          "Payload": [{"Username": "Kakao", "Password": "123"}]}
        
        if not self._user_exists(test_register_payload):
            print("Saving new user...")
            self.database._save_user(test_register_payload)
        else:
            self.outgoing_queue.put(user_exists_if)
            print("User already exists...")
            client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))


    def _tick_data(self, client):
        tick_data_if = {"Type": "Tick", "Payload": ["EMPTY"]}
        self.outgoing_queue.put(tick_data_if)
        while True:
            time.sleep(2)
            # self.server_socket.sendall(json.dumps(tick_data_if).encode('utf-8'))
            try:
                client.send(self._jsonify_data(self.outgoing_queue.get()).encode('utf-8'))
            except:
                for user in self.connected_users:
                    if user["Client"] == client:
                        self.connected_users.remove(user)

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

    
