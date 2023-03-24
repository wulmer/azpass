# Authenticate with azure-identity and return a credential object

import click
from pathlib import Path
from environment import Environment
from vault import Vault

env_path = Path.home() / ".azpass"

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
def azpass():
    """A cli tool to use azure keyvaults as a secret store."""
    pass

@azpass.group()
def vault():
    """Manage key vaults"""

@vault.command()
@click.argument("path", required=True)
def add(path):
    """Add a keyvault.

    path: <resource-group>/<vault-name>
    """
    resource_group, name = parse_secret_path(path, True)
    print(resource_group, name)
    Environment(env_path).add_vault(Vault(name, resource_group))

@vault.command()
@click.argument("name", required=True)
def get(name):
    """Get a key vault.
    
    name: vault name    
    """
    vaults = Environment(env_path).get_vaults()
    for vault in vaults:
        if name == vault.name:
            print(str(vault))

@vault.command()
def list():
    """List all key vaults"""
    print(Environment(env_path).get_vaults())

@azpass.group()
def secret():
    """Manage secrets"""
    pass

@secret.command("get")
@click.argument("path", required=True)
def get_s(path):
    """Get secrets from a vault.
    path: secret path in the format <vault-name>/<resource-group>
    """
    vault_name, secret_name = parse_secret_path(path, True)
    if not vault_name:
        vaults = Environment(env_path).get_vaults()
        secrets = [vault.get_secret(secret_name) for vault in vaults]
        for secret in secrets:
            print(secret)
    else:
        vault = Environment(env_path).get_vault(vault_name)
        if not vault:
            print("Vault not found")
            return
        print(vault.get_secret(secret_name))

@secret.command("list")
@click.argument("find", required=False)
def list_s(find):
    """List all secrets
    find: Filter secrets by string
    """
    res = []
    if find:
        res = Environment(env_path).list_secret_names(find)
    else:
        res = Environment(env_path).list_secret_names()
    for r in res:
        print(r)

@secret.command()
@click.argument("path", required=True)
@click.argument("secret-value", required=True)
def set(path, secret_value):
    """Set a secret in a vault.
    
    path: secret path in the format <vault-name>/<resource-group>

    secret-value: Value of the secret
    """
    vault_name, secret_name = parse_secret_path(path, False)
    vault = Environment(env_path).get_vault(vault_name)
    if not vault:
        print("Vault not found")
        return
    vault.set_secret(secret_name, secret_value)

@azpass.command()
def init():
    """Initialize a environment"""
    Environment(env_path)

def parse_secret_path(path: str, rg_name_optional: bool):
    elems = path.split("/")
    if rg_name_optional:
        switch = len(elems)
        if switch == 1:
            return "", elems[0]
        elif switch == 2:
            return elems[0], elems[1]
        else:
            raise ValueError("Invalid secret path, expected format: <vault-name>/<secret-name>")

    else:
        if len(elems) != 2:
            raise ValueError("Invalid secret path, expected format: <vault-name>/<secret-name>")
        return elems[0], elems[1]
    

def main():
    azpass()

if __name__ == "__main__":
    main()