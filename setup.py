"""
Temporary file copied from the Flask Tutorial.
Section: 'Make the project installable'
https://flask.palletsprojects.com/en/1.1.x/tutorial/install/
"""
from setuptools import find_packages, setup

setup(
    name="nebula",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "Flask-SQLAlchemy", "Flask-WTF"],
)
