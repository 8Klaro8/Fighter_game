


import time, json
from Database.database import Database

class Authentication:
    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.database = Database()
        self._go_back = False
        # self.login_if = {"Type": "Login", "Payload": []}
        # self.register_if = {"Type": "Register", "Payload": []}
        self.auth_if = {"Type": None, "Payload": []}
        self.options = {1: ["Login", self._login],
                        2: ["Register", self._register]}
        
    def _display_auth_options(self):
        """ Displays authentication options"""
        print("------------------------\nOptions:")
        for option_num, option in self.options.items():
            print(f"{option_num}.) {option[0]}")

    def _receive_user_auth_choice(self) -> dict:
        """ Start chosen functionality (login or register)
        and returns the given credentials """
        choice = input("\nChoose... ")
        self._control_user_input(choice)
        return self.auth_if
    
    def _control_user_input(self, input):
        """ Controls if user choosed a valid option
        on the validation screen """
        try:
            input = int(input)
            try:
                self.options[input][1]()
            except:
                print("Invalid number...")
                self._receive_user_auth_choice()
        except:
            print("Please give a valid choice...")
            self._receive_user_auth_choice()

    def _login(self) -> dict:
        """ Asks for login credentials & returns it """
        credentials = {"Username": None, "Password": None}
        is_go_back = False
        print("\nType 'back' to go back\n--------------------")

        while True:
            username = input("Type your username... ")
            if self._go_back_function(username):
                is_go_back = True
                break
            password = input("Type your password...")
            if self._go_back_function(password):
                is_go_back = True
                break

            # setup login if.
            credentials["Username"] = username
            credentials["Password"] = password
            # self.login_if['Payload'].append(credentials)
            self.auth_if['Payload'].append(credentials)
            self.auth_if["Type"] = "Login"

            # sending login if. to server
            print("Sending credentials to server...")
            print(f"Payload: ", self.auth_if)
            break

        # Goes back to auth screen if 'b' was pressed
        print("IS_GO_BACK: ", is_go_back)
        if is_go_back:
            self._display_auth_options()
            self._receive_user_auth_choice()

    def _register(self):
        """ Saves register if. """
        credentials = {"Username": None, "Password": None}
        print("\nType 'back' to go back\n--------------------")

        while True:
            username = input("\nChoose a username... ")
            if self._go_back_function(username):
                self._go_back = True
                break
            password = input("Choose a password...")
            if self._go_back_function(password):
                self._go_back = True
                break
            rep_password = input("Repeat password...")
            if self._go_back_function(rep_password):
                self._go_back = True
                break
            
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

                print("Sending register credentials to server...")
                print(f"Payload: ", self.auth_if)
                break

        if self._go_back:
            self._go_back = False
            # Goes back to auth screen if 'back' was typed
            self._display_auth_options()
            self._receive_user_auth_choice()

    def _control_password(self, password_1: str, password_2: str) -> bool:
        """ Checks if passwords match """
        if password_1 != password_2:
            return False
        return True
    
    def _auth_logging_user(self, username: str, password: str) -> bool:
        """ If username and password match then returns True """
        content = self.database._read_users_json(username, password)
        # content = self._read_users_json(username, password)

        if not content:
            return "FileNotFound"
        
        for user in content["Users"]:
            if user["Username"] == username:
                if user["Password"] == password:
                    return True
        return False
    
    def _go_back_function(self, input:str):
        """ Calls the corresponding fucntion where to go back """
        if input.lower() == 'back':
            return True
        return False