# azpass

A cli tool to use azure keyvaults as a secret store.

## Installation

```bash
pip install -r requirements.txt
pip install .
```

## Usage

```bash
azpass --help
```

## Performance increase

If you suffer from slow performance, you may need to disable telemetry of the azure cli.

```bash
az config set core.collect_telemetry=False
```