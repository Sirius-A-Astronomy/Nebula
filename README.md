# Nebula

This is the Nebula Database by the Kapteyn Learning Community.
It is a repository of user-submitted practice questions.

## Table of Contents
[[_TOC_]]

_Other documentation:_
- [CLI Documentation](docs/cli/index.md)
- [How does Nebula work?](docs/how-does-nebula-work.md)

## Installation & Setup

_Note: This guide assumes you're using linux or [wsl.](https://docs.microsoft.com/en-us/windows/wsl/install)_

Setting up the project should be possible via the following: (all from the project root directory).

<details> 
<summary>1. Clone or pull the project (expand for more info)</summary>

```bash
git clone https://gitlab.astro.rug.nl/sirius-a/nebula.git
```

</details>
<details><summary>2. Git checkout to the correct branch</summary>

_Note: in this guide the branch 'dev' was used as it was the most recently used._

```bash
git checkout dev
```

</details>
<details><summary>3. Create a virtual environment for the project inside the project directory. </summary>
This makes sure you do not 'contaminate' your global Python dependencies with the dependencies for Nebula and vice versa.

-   Go to the nebula directory

```bash
cd nebula
```

-   Create the directory for the virtual environment

```bash
mkdir venv
```

-   Create the python virtual environment

```bash
python3 -m venv venv
```

</details>
<details><summary>4. Activate your virtual environment</summary>

```bash
. venv/bin/activate
```

_Note: to deactivate the virtual environment symply run `deactivate`_

</details>

<details><summary>5. Install dependencies</summary>

-   While in the virtual environment run:

```bash
python3 -m pip install -r requirements.txt
```

-   You will also need to install nodejs and sass to be able to compile the scss files to valid css
-   [installing nodejs](https://nodejs.org/en/download/package-manager/)

-   Now nodejs is installed, you can install sass with:

```bash
npm install
```

_Note: omit the -g flag if you don't wish to install sass globally_

</details>

<details><summary>6. Create the nebula database</summary>
- The following command will create the database and seed it with test data

```bash
make db-migrate-fresh-seed
```

</details>

7. It should be possible to run Nebula via the following command:

```bash
make dev-server
```

_Note: to close the flask local webserver: ctrl+c_

8. It should be available at [localhost:5000](localhost:5000/) in your browser, or via a link in the command prompt.

Now you should be good to go!




## Testing

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

### Testing with cypress

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

## To-do

1. Move original website over to Flask
    - [ ] Implement updated database structure
    - [ ] PHP code -> Flask
2. Ensure the current database gets moved over properly
3. Implement accounts (Just Kapteyn intranet, or external accounts with linkage?)
    - [ ] Superusers
    - [ ] KLC members (Referees)
    - [ ] Professors/staff
    - [ ] Regular users
    - [ ] Limited guest accounts (pre-prognum)?
4. Implement stretch goaals
    - [ ] NebuLaTeX + Markdown
    - [ ] Like
    - [ ] Comment (issue reporting, changelog, but single author)
    - [ ] Subscribe?
    - [ ] Difficult-o-meter
    - [ ] Aeaesthetics
