


import time

class Authentication:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.login_if = {"Type": "Login", "Payload": []}
        self.register_if = {"Type": "Register", "Payload": []}
        self.options = {1: ["Login", self._login],
                        2: ["Register", self._register]}

    def _show_logic_if(self):
        """ Displays authentication options"""
        print("------------------------\nOptions:")
        for option_num, option in self.options.items():
            print(f"{option_num}.) {option[0]}")

    def _receive_user_input(self):
        """ Start chosen functionality """
        choice = int(input("\nChoose... "))
        self.options[choice][1]() # calling choosed function/ option

    def _login(self) -> dict:
        """ Asks for login credentials & returns it """
        credentials = {"Username": None, "Password": None}

        username = input("\nChoose a username... ")
        password = input("Choose a password...")

        # setup login if.
        credentials["Username"] = username
        credentials["Password"] = password
        self.login_if['Payload'].append(credentials)

         # sending login if. to server
        print("Sending credentials to server...")
        print(f"Payload: ", self.login_if)
        return self.login_if

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
            self.register_if['Payload'].append(credentials)

            print("Sending register credentials to server...")
            print(f"Payload: ", self.register_if)
            return self.register_if

    def _control_password(self, password_1: str, password_2: str) -> bool:
        """ Checks if passwords match """
        if password_1 != password_2:
            return False
        return True
    

if __name__ == '__main__':
    auth = Authentication()
    auth._show_logic_if()
    auth._receive_user_input()