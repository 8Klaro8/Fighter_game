


import time, json

class Authentication:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        # self.login_if = {"Type": "Login", "Payload": []}
        # self.register_if = {"Type": "Register", "Payload": []}
        self.auth_if = {"Type": None, "Payload": []}
        self.options = {1: ["Login", self._login],
                        2: ["Register", self._register]}

    def _show_logic_if(self):
        """ Displays authentication options"""
        print("------------------------\nOptions:")
        for option_num, option in self.options.items():
            print(f"{option_num}.) {option[0]}")

    def _receive_user_input(self) -> dict:
        """ Start chosen functionality """
        choice = int(input("\nChoose... "))
        self.options[choice][1]() # calling choosed function/ option
        return self.auth_if

    def _login(self) -> dict:
        """ Asks for login credentials & returns it """
        credentials = {"Username": None, "Password": None}

        username = input("Type your username... ")
        password = input("Type your password...")

        # setup login if.
        credentials["Username"] = username
        credentials["Password"] = password
        # self.login_if['Payload'].append(credentials)
        self.auth_if['Payload'].append(credentials)
        self.auth_if["Type"] = "Login"

         # sending login if. to server
        print("Sending credentials to server...")
        print(f"Payload: ", self.auth_if)
        # return self.login_if

    def _register(self):
        """ Returns register if. """
        credentials = {"Username": None, "Password": None}

        username = input("\nChoose a username... ")
        password = input("Choose a password...")
        rep_password = input("Repeat password...")

        if not self._control_password(password, rep_password):
            print("Password doesn't match!")
            time.sleep(0.5)
            self._register()
        else:
            # setup credentials
            credentials["Username"] = username
            credentials["Password"] = password
            self.auth_if['Payload'].append(credentials)
            self.auth_if["Type"] = "Register"
            # self.register_if['Payload'].append(credentials)

            print("Sending register credentials to server...")
            print(f"Payload: ", self.auth_if)

    def _control_password(self, password_1: str, password_2: str) -> bool:
        """ Checks if passwords match """
        if password_1 != password_2:
            return False
        return True
    
    def _auth_logging_user(self, username: str, password: str) -> bool:
        content = self._read_users_json()
        for user in content["Users"]:
            if user["Username"] == username:
                if user["Password"] == password:
                    return True
        return False

    def _read_users_json(self):
        with open("users.json", "r") as file:
            try:
                content = json.load(file)
            except json.JSONDecodeError:
                print("Users file is empty.")
                return None
        return content

if __name__ == '__main__':
    auth = Authentication()
    auth._show_logic_if()
    auth._receive_user_input()