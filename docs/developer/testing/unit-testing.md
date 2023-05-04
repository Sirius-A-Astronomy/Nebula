# Unit Testing

To make sure Nebula works as intended we have a suite of unit tests that can be run with the following command:

```bash
make test
```

This will run `pytest` to test the python backend and `vitest` to test the javascript frontend.

## Python Backend

The python backend tests are located in the `nebula/tests/py` directory.

To only run the python backend tests run the following command:

```bash
make test-py
```

To learn how to write pytest tests see the [pytest documentation](https://docs.pytest.org/en/latest/).

Fixtures for pytest can be found in the `nebula/tests/py/conftest.py` file. This includes fixures for the database, flask app, and flask client as well as a client that has a logged in user or admin.

## Javascript Frontend

The javascript frontend tests are located in the `nebula/tests/js` directory.

To only run the javascript frontend tests run the following command:

```bash
make test-js
```
