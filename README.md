# Nebula
This is the Nebula Database by the Kapteyn Learning Community.
It is a repository of user-submitted practice questions.

## Installation & Setup
Setting up the project should be possible via the following: (all from the project root directory).
<details> 
<summary>1. Clone or pull the project (expand for more info)</summary>
```bash
git clone https://gitlab.astro.rug.nl/sirius-a/nebula.git
```

</details>
2. Create a virtual environment for the project. This makes sure you do not 'contaminate' your global Python dependencies with the dependencies for Nebula and vice versa.
3. Activate your virtual environment
4. It should be possible to run Nebula via the following command:
```bash
env FLASK_APP=nebula FLASK_ENV=development flask run
```
5. It should be available at [localhost:5000](localhost:5000/) in your browser, or via the command line.


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
