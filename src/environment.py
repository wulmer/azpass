# Implement a class to store the state of the application

import pathlib
from vault import Vault
from os import path
import json

class Environment():
    vaults: list[Vault] = []

    def __init__(self, path: pathlib.Path):
        self.path = path
        if not pathlib.Path(self.path).is_file():
            self.save()
        else:
            self.load()

    def save(self):
        f = open(self.path, "w")
        state = {"vaults": []}
        for vault in self.vaults:
            state["vaults"].append({"name": vault.name, "resource_group": vault.resource_group})
        print(state)
        state_json = json.dumps(state)
        f.write(state_json)
        f.close()    

    def load(self):
        f = open(self.path, "r")
        state_json = f.read()
        state = json.loads(state_json)
        for vault in state["vaults"]:
            self.vaults.append(Vault(vault["name"], vault["resource_group"]))
        f.close()

    def add_vault(self, vault: Vault):
        self.vaults.append(vault)
        self.save()

    def get_vault(self, name: str):
        for vault in self.vaults:
            if vault.name == name:
                return vault
    
    def get_vaults(self):
        return self.vaults
    
    def list_secret_names(self, find: str = "") -> list[str]:
        names: list[str] = []
        for vault in self.vaults:
            for name in vault.list_secret_names():
                if find in name:
                    names.append(f"{vault.name}/{name}")
        return names

        
    

