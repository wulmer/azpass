# azpass

A cli tool to use azure keyvaults as a secret store.

## Pre-requisites

- Python 3 (tested with 3.9)
- azure cli (tested with 2.46.9)
- run `az login` and follow the instructions before using this tool

## Installation

```bash
pip install -r requirements.txt
pip install .
```

## Usage

### Create a environment

Environments store you keyvault references that will be used to retrieve secrets.

```bash
azpass init
```
### Add a keyvault reference

```bash
azpass vault add my-resource-group/my-keyvault-name
```

### List secrets of the added keyvaults

```bash
azpass secrets list
```

or if you want to filter the secrets

```bash
azpass secrets list pat
```

### More commands

```bash
azpass --help
```

## Performance increase

If you suffer from slow performance, you may need to disable telemetry of the azure cli.

```bash
az config set core.collect_telemetry=False
```