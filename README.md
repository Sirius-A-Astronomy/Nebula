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
</details>


6. It should be possible to run Nebula via the following command:

```bash
env FLASK_APP=nebula FLASK_ENV=development flask run
```
_Note: to close the flask local webserver: ctrl+c_

7. It should be available at [localhost:5000](localhost:5000/) in your browser, or via the command line.

<details><summary>8. Most likely you'll not be able to access the website just yet as the database needs to be created locally as well.</summary>

1. To create the database you'll first need to install nebula as a package. (still within the virtual environment)

    ```bash
    python3 -m pip install -e .
    ```
2. Enter python:
   
   ```bash
   python3
   ```
3. Create the database:

    ```python
    from nebula import create_app, db

    app = create_app()

    app.app_context().push()

    db.create_all()

    exit()
    ```

You can now run Nebula as shown above, however you'll find that there are no courses or anything on the site as the database we just created is completely empty. To fix that run (in the virtual environment):
```bash
python3 database-setup/database_setup.py
```
</details>
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
1. install cypress in venv
* prerequisites:

    ```bash
    apt-get install libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb 
    ```

    ```bash
    apt-get install cypress --save-dev
    ```

2. install cypress real events
   
    ```bash
    npm install cypress-real-events
    yard add cypress-real-events
    ```

3. With the webserver running start cypress
   
   ```bash
   ./node_modules/.bin/cypress open
   ```

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
