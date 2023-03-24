# Implement a class to store the state of the application

import json
import pathlib
from typing import Generator, List, Optional

import azure.core.exceptions

from .vault import Vault


class Environment:
    vaults: List[Vault]

    def __init__(self, path: pathlib.Path):
        self.path = path
        self.vaults = []
        if not pathlib.Path(self.path).is_file():
            self.save()
        self.load()

    def save(self) -> None:
        state = {"vaults": []}
        for vault in self.vaults:
            state["vaults"].append(
                {"name": vault.name, "resource_group": vault.resource_group}
            )
        state_json = json.dumps(state, indent=2)
        print(state_json)
        self.path.write_text(state_json)

    def load(self) -> None:
        state = json.loads(self.path.read_text())
        for vault in state["vaults"]:
            self.vaults.append(Vault(vault["name"], vault["resource_group"]))

    def add_vault(self, vault: Vault) -> None:
        self.vaults.append(vault)
        self.save()

    def get_vault(self, name: str) -> Optional[Vault]:
        for vault in self.vaults:
            if vault.name == name:
                return vault

    def get_vaults(self) -> List[Vault]:
        return self.vaults

    def list_secret_names(self, find: str = "") -> Generator[str, None, None]:
        for vault in self.vaults:
            try:
                for name in vault.list_secret_names():
                    if find in name:
                        yield f"{vault.name}/{name}"
            except azure.core.exceptions.ResourceNotFoundError:
                pass
