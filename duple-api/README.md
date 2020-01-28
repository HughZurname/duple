# Duple API

## Available Scripts

In the project directory, you can run:

- `pip install -e .`

  - Installs the app and it's dependencies.
  - _Required for the scripts below to work._

- `python -m duple -s`

  - Runs the app in server mode.

- `python -m duple -c -f <filename>`

  - Runs the app in console mode.

- `tox`

  - Installs test dependencies and runs tests

---

## Testing

Testing is done with [pytest](https://docs.pytest.org/en/latest/) for unit testing with coverage by [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/), static security analysis is performed by [bandit](https://bandit.readthedocs.io/en/latest/) and linting is provided by [flake8](http://flake8.pycqa.org/en/latest/).

- All of this can be run with the `tox` command from this folder.
- Coverage and testing Reports can be found in `./reports`

## Logging

Logging has been set to `INFO`, if you would like to see full debug logging (it gives you some interesting insight in to how `deduper` selectes it's predicates) you can change it in `duple/__init__.py`

## Swagger

Swagger docs can be found at `localhost:8080/api/doc` and should cover the important parts of interacting with the `duple` api.
