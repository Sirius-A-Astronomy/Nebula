import glob
from os.path import basename, dirname, isfile, join

from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]


from . import *  # import all the modules in the api folder
