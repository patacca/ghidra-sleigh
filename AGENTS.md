- Always run the command from a python venv
- **In the CI** Never run python commands inside a venv


## Development

Install development tooling:

```bash
python -m venv venv
. venv/bin/activate
pip install -e ".[dev]"
```

Run checks via `tox`:

```bash
# Run all environments
tox

# Run one environment
tox -e lint
tox -e format
tox -e py
```

The configured `tox` environments are:

- `lint`: lint checks
- `format`: formatting checks
- `py`: tests (active interpreter)