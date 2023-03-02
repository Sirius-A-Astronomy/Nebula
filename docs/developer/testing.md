
# Testing

## Unit tests

If you want to run tests, you first need to install Nebula as a package. Again in a virtual environment, run in the root directory:

```bash
pip install -e .
```

Then, simply run:

```bash
pytest
```

or for coverage:

```bash
coverage run -m pytest
```

## End to end testing with cypress

0. [If you haven't yet, install nodejs and npm (still all in the virtual environment)](https://nodejs.org/en/download/package-manager/)
1. [Install cypress](https://docs.cypress.io/guides/getting-started/installing-cypress)

2. [Install cypress real events](https://github.com/dmtrKovalenko/cypress-real-events#installation)

3. With the webserver running, start cypress

    ```bash
    ./node_modules/.bin/cypress open
    ```

    or

    ```bash
    npx cypress start
    ```

    To run all of the tests without a GUI run:

    ```bash
    npx cypress run
    ```

4. In the UI click on one of the tests to start it.

To learn more check out: [Writing your first test](https://docs.cypress.io/guides/getting-started/writing-your-first-test)
