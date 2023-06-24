import socket, json, threading
from Database.database import Database

class ServerSocket:
    def __init__(self, port, host) -> None:
        self.PORT = port
        self.HOST = host
        self.server_socket = None
        self.connected_users = [] # [{"Client": client, "Username": "yxc"}]
        self.database = Database()

    def _create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
        print("Server is listening...")

        self._register_user()

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

    def _receive_data(self, client):
        while True:
            data = client.recv(1024)
            print("RECEIVED DATA: ", data)

    def _register_user(self):
        test_register_payload = {"Type": "Register",
                                 "Payload": [{"Username": "Kakao", "Password": "123"}]}
        
        if not self._user_exists(test_register_payload):
            print("Saving new user...")
            self.database._save_user(test_register_payload)
        else:
            print("User already exists...")
        
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

    # def _read_users_json(self) -> dict | None:
    #     with open("users.json", "r") as file:
    #         try:
    #             content = json.load(file)
    #         except json.JSONDecodeError:
    #             print("Users file is empty.")
    #             return None
    #     return content


if __name__ == '__main__':
    server_socket = ServerSocket(6060, "localhost")
    server_socket._create_socket()
    server_socket._accept_new_connections()
    server_socket._register_user()
