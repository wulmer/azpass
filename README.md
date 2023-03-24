# azpass

A cli tool to use azure keyvaults as a secret store.

## Pre-requisites

- Python 3 (tested with 3.9)
- azure cli (tested with 2.46.9)
- run `az login` and follow the instructions before using this tool

## Installation

```bash
pip3 install -r requirements.lock
pip3 install .
```

To update the `requirements.lock` file, run `pip3 freeze -r requirements.txt > requirements.lock`.

## Building a distributable pex file

If you have the Python package `pex` installed, run

```bash
python setup.py bdist_pex
```

and find the pex file in the `dist/` folder. You can directly execute the pex
file or copy/link it to your `~/bin/` folder:

```bash
cp dist/azpass-*.pex ~/bin/azpass
# or
ln -sf $(pwd)/dist/azpass-*.pex ~/bin/azpass
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
azpass secret list
```

or if you want to filter the secrets

```bash
azpass secret list pat
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
