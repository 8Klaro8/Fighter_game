import json


class Database:
    def __init__(self) -> None:
        pass

    def _save_user(self, register_payload: dict):
        """ Manages user's save into users.json """
        username = register_payload["Payload"][0]["Username"]
        password = register_payload["Payload"][0]["Password"]
        new_user_if = {"Username": username,
                       "Password": password}
        
        content = self._read_users_json(username, password)
        if content == None or content == False:
            # save new user
            first_if = {"Users": register_payload["Payload"]}
            self._save_to_file(first_if)
        else:
            content["Users"].append(new_user_if)
            self._save_to_file(content)

    def _save_to_file(self, content):
        """ Saves data to users.json"""
        with open('users.json', 'w') as file:
            dumped_data = json.dumps(content)
            file.write(dumped_data)

    def _read_users_json(self, username, password):
        """ Reads users.json file if exists otherwise returs false"""
        try:
            return self._read_file(username, password)
        except:
            return False
        
    def _read_file(self, username, password) -> None | dict:
        """ Reads users.json. If file is emt returns None,
        otherwise returns the loaded content"""
        with open("users.json", "r") as file:
            try:
                content = json.load(file)
            except json.JSONDecodeError:
                print("Users file is empty.")
                return None
        return content
            
    def _user_exists(self, userame) -> bool:
        """ Returns True if user exists in db,
        otherwise False"""
        content = None
        with open("users.json", "r") as file:
            content = json.load(file)

        for user in content["Users"]:
            if user["Username"] == userame:
                return True
        return False