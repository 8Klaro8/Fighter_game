

import socket, json, threading


class ClientSocket:
    def __init__(self, port, host) -> None:
        self.PORT = port
        self.HOST = host
        self.client_socket = None

    def _create_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

    def _receive_data(self):
        received_data = self.client_socket.recv(1024).decode('utf-8')
        print("DATA: ", received_data)

    def _send_data(self):
        test_messag = {"Type": "Action", "Strategy": "YOYO"}
        self.client_socket.send(self._jsonify_data(test_messag).encode('utf-8'))

    def _jsonify_data(self, data: dict) -> json:
        return json.dumps(data)


if __name__ == '__main__':
    client_socket = ClientSocket(port=6060, host="localhost")
    client_socket._create_socket()
    
    receive_thread = threading.Thread(target=client_socket._receive_data)
    receive_thread.start()
    send_thread = threading.Thread(target=client_socket._send_data)
    send_thread.start()