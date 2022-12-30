# How are routes defined?

Routes are defined in the `routes` directory. The `routes` directory is located in the `nebula` directory. The `routes` directory contains a two subdirectories: `web` and `api`. The `web` directory contains all the routes for the web application. The `api` directory contains all the routes for the API.

The `web` and `api` directories contain a `__init__.py` file. The `__init__.py` file contains a Flask `blueprint`. This blueprint can either be imported in the `<route>.py` file or can be extended with another blueprint. The `<route>.py` file contains the route logic.

The `__init__.py` file handles registering the blueprint with the Flask application.



# Usage

## Web Routes

```python {4,7,10}
# your_route.py

# import the web blueprint
from nebula.routes.web import bp as web_bp

# Create a new blueprint that will contain the routes for your route
bp = Blueprint('your_route', __name__)

# Extend the web blueprint with your blueprint
web_bp.register_blueprint(bp)

# Add your routes
@bp.route('/your_route')
def your_route():
    return 'Hello World'

@bp.route('/your_route/<id>')
def your_route_with_id(id):
    return 'Hello World with id: ' + id

# These routes can be linked to with the url_for function
# url_for('web.your_route.your_route')
# url_for('web.your_route.your_route_with_id', id=1)
```

## API Routes
```python {4,7,10}
# your_route.py

# import the api blueprint
from nebula.routes.api import bp as api_bp

# Create a new blueprint that will contain the routes for your route
bp = Blueprint('your_route', __name__, url_prefix='/your_route')

# Extend the api blueprint with your blueprint
api_bp.register_blueprint(bp)

# Add your routes
@bp.route('/')
def your_route():
    return 'Hello World'

@bp.route('/<id>')
def your_route_with_id(id):
    return 'Hello World with id: ' + id

# These routes can be linked to with the url_for function
# url_for('api.your_route.your_route')
# url_for('api.your_route.your_route_with_id', id=1)
```

For api routes it is not always necessary to extend the api blueprint. 
Routes can be directly added to the blueprint of the API. This is useful if a route does not need to be prefixed with the name of the blueprint.

```python {4}
# your_route.py

# import the api blueprint
from nebula.routes.api import bp

# Add your routes
@bp.route('/your_route')
def your_route():
    return 'Hello World'

@bp.route('/your_route/<id>')
def your_route_with_id(id):
    return 'Hello World with id: ' + id

# These routes can be linked to with the url_for function
# url_for('api.your_route')
# url_for('api.your_route_with_id', id=1)
```