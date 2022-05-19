# Nebula
This is the Nebula Database by the Kapteyn Learning Community.
It is a repository of user-submitted practice questions.

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

_Note: in this guide the branch 'flask-redevelopment' was used as it was the most recently used._

```bash
git checkout flask-redevelopment
```
</details>
<details><summary>3. Create a virtual environment for the project inside the project directory. </summary>
This makes sure you do not 'contaminate' your global Python dependencies with the dependencies for Nebula and vice versa.

* Go to the nebula directory

```bash
cd nebula
```

* Create the directory for the virtual environment

```bash
mkdir venv
```

* Create the python virtual environment

```bash
python3 -m venv venv 
```

</details>
<details><summary>4. Activate your virtual environment</summary>

```bash
. venv/bin/activate
```

_Note: to deactivate the virtual environment symply run ```deactivate```_
</details>

<details><summary>5. Install dependencies</summary>

* While in the virtual environment run:

```bash
python3 -m pip install -r requirements.txt
```

* You will also need to install nodejs and sass to be able to compile the scss files to valid css
* [installing nodejs](https://nodejs.org/en/download/package-manager/)

* Now nodejs is installed, you can install sass with:

```bash
npm install -g sass
```

_Note: omit the -g flag if you don't wish to install sass globally_


</details>


<details><summary>6. Create the nebula database</summary>

1. To create the database you'll first need to install nebula as a package. (still within the virtual environment)

    ```bash
    python3 -m pip install -e .
    ```
2. Now initialise the database:

    ```bash
    python3 database-setup/init_db.py
    ```

3. The database is still empty, though. Let's fill it with some sample data.

    ```bash
    python3 database-setup/database_test_data.py
    ```

</details>


7. It should be possible to run Nebula via the following command:

```bash
env FLASK_APP=nebula FLASK_ENV=development flask run
```

_Note: to close the flask local webserver: ctrl+c_

8. It should be available at [localhost:5000](localhost:5000/) in your browser, or via a link in the command prompt.

Now you should be good to go!

## Nebula uses SASS

[SASS, or Synthactically Awesome Style Sheets](https://sass-lang.com/), is a superset of CSS. Since nebula uses the SCSS syntax any css written in the .scss files is valid

When Nebula builds it will automatically compile all sass files in the static/scss folder into css files on startup. For this it uses sass via a subprocess on the local machine. This needs to be installed (step 5 of installation and setup). 

To also have nebula detect changes and automatically reload while you are editing scss files you can start nebula with an extra environment variable.

```bash
export FLASK_RUN_EXTRA_FILES="path/to/file:/path/to/other/file"
```

Since every file needs to be added individually this can of course get really tedious. By adding the following code to your ~/.bashrc or ~/.bash_profile you can start nebula with one simple command that automatically finds all scss files and tell nebula to watch them for changes.

```bash
function nebrunner () {
    echo "Running nebula"
    export FLASK_APP=nebula
    export FLASK_ENV=development

    # find all scss files and add them to the extra files that flask will watch
    export search_dir="./nebula/static/scss"/*
    export FLASK_RUN_EXTRA_FILES=""

    for i in $(find $search_dir -name '*.scss');
    do
        export FLASK_RUN_EXTRA_FILES="$FLASK_RUN_EXTRA_FILES$i:"
        
    done;
    export FLASK_RUN_EXTRA_FILES=${FLASK_RUN_EXTRA_FILES%?} # remove last colon

    # run flask
    python3 -m flask run
}
```
_Note: this will only watch files that exist when nebula starts. To also watch a new file, restart nebula._

Now starting nebula is as simple as running ```nebularun``` in your command line.


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
