

import json


class Database:
    def __init__(self) -> None:
        pass

    def _save_user(self, register_payload: dict):
        username = register_payload["Payload"][0]["Username"]
        password = register_payload["Payload"][0]["Password"]
        new_user_if = {"Username": username,
                       "Password": password}
        
        content = self._read_users_json()
        if content == None:
            # save new user
            first_if = {"Users": register_payload["Payload"]}
            self._save_to_file(first_if)
        else:
            content["Users"].append(new_user_if)
            self._save_to_file(content)

    def _save_to_file(self, content):
        with open('users.json', 'w') as file:
            dumped_data = json.dumps(content)
            file.write(dumped_data)

    # def _save_first_data(self, content):
    #     with open('users.json', 'w') as file:
    #         dumped_data = json.dumps(content)
    #         file.write(dumped_data)

    def _read_users_json(self):
        with open("users.json", "r") as file:
            try:
                content = json.load(file)
            except json.JSONDecodeError:
                print("Users file is empty.")
                return None
        return content
            
