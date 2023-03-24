from typing import Generator

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError


class Vault:
    """Vault class"""

    def __init__(self, name: str, resource_group: str):
        self.name = name
        self.resource_group = resource_group
        self.client = SecretClient(
            vault_url=f"https://{self.name.lower()}.vault.azure.net",
            credential=DefaultAzureCredential(),
        )

    def __str__(self):
        return f"Vault(name={self.name}, resource_group={self.resource_group})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_secret(self, secret_name) -> str | None:
        """Get a secret from the vault"""
        try:
            secret = self.client.get_secret(secret_name).value
            return secret
        except ResourceNotFoundError:
            return None

    def set_secret(self, secret_name: str, secret_value: str) -> None:
        """Set a secret in the vault"""
        self.client.set_secret(secret_name, secret_value)

    def delete_secret(self, secret_name: str) -> None:
        """Delete a secret from the vault"""
        self.client.begin_delete_secret(secret_name)
        self.client.purge_deleted_secret(secret_name)

    def list_secret_names(self) -> Generator[str, None, None]:
        """List all secrets names in the vault"""
        secrets_p = self.client.list_properties_of_secrets()
        for secret_p in secrets_p:
            # skip a secret if it has no name
            if secret_p.name:
                yield secret_p.name
