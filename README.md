[![Deploy](https://github.com/Dutch-Raptor/nebula/actions/workflows/deploy.yml/badge.svg)](https://github.com/Dutch-Raptor/nebula/actions/workflows/deploy.yml)

# Nebula

[![Continuous Integration and Deployment](https://github.com/Sirius-A-Astronomy/Nebula/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sirius-A-Astronomy/Nebula/actions/workflows/ci-cd.yml)

This is the Nebula Database by the Kapteyn Learning Community.
It is a repository of user-submitted practice questions.

TODO: Add a screenshot of the website

TODO: replace docs link to nebula docs once they are up

**To check out the full documentation, go to [nebula.pieterhuizenga.com](https://nebula.pieterhuizenga.com)**

# Getting Started

This guide will help you get Nebula up and running on your local machine.


> This guide assumes you're using linux or [wsl](https://docs.microsoft.com/en-us/windows/wsl/install)

## Step 1. Clone or pull the project

```bash
git clone https://gitlab.astro.rug.nl/sirius-a/nebula.git
```



> To learn more about contributing to Nebula, see [Contributing](docs/developer/contributing.md)

Checkout to the `branch` you want to work on. For example, if you want to work on the `dev` branch:

```bash
git checkout dev
```

## Step 2. Create a virtual environment

This makes sure you do not 'contaminate' your global Python dependencies with the dependencies for Nebula and vice versa.

-   Go to the nebula directory

```bash
cd nebula
```

-   Create the python virtual environment

```bash
python3 -m venv venv
```


> In this command the second `venv` is the name of the virtual environment. You can name it whatever you want, but it is recommended to keep it as `venv` for consistency.

- Activate your virtual environment

```bash
. venv/bin/activate
```


> To deactivate the virtual environment, run `deactivate`


## Step 3. Install dependencies

```bash
make deps-dev
```

## Step 4. Database creation and seeding

Initialize the database and seed it with some data.

```bash
export FLASK_APP=nebula

flask db init

flask db seed
```

> For more information on the database CLI commands, see [here](docs/developer/cli/database-cli.md)

## Step 5. Run the development servers

Run both the `flask` and `Vite` development servers in separate terminals.

To run the `flask` development server:
```bash
make dev-server
```

This will run the flask development server on [localhost:5000](localhost:5000) which will serve the web pages and the API.

---

To run the `Vite` development server:
```bash
npm run dev
```

This will run the Vite development server on [localhost:5173](localhost:5173) which will serve the frontend assets.

> To close either of the webservers: ctrl+c

The development server should now be running on [localhost:5000](localhost:5000)

## Building for production

```bash
make build
```

This will build all the assets and put them in the `nebula/static` directory and build the documentation.


