# Getting Started

## Installation & Setup

::: info
 This guide assumes you're using linux or [wsl](https://docs.microsoft.com/en-us/windows/wsl/install)
:::

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

5. Install dependencies

```bash
make deps-dev
```

<details><summary>6. Create and seed the database</summary>

```bash
export FLASK_APP=nebula

flask db init

flask db seed

# or `flask db seed_dev`
```

:::tip Learn More
For more information on the database CLI commands, see [here](/developer/cli/database-cli.md)
:::

</details>

1. It should be possible to run Nebula via the following command:

```bash
make dev-server
```

::: info
To close the flask local webserver: ctrl+c
:::

8. It should be available at [localhost:5000](localhost:5000/) in your browser, or via a link in the command prompt.

Now you should be good to go!