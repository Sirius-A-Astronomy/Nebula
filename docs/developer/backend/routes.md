# Routes

Routes are defined in the `routes` directory. The `routes` directory is located in the `nebula` directory. The `routes` directory contains a two subdirectories: `web` and `api`. The `web` directory contains all the routes for the web application. The `api` directory contains all the routes for the API.

The `web` and `api` directories contain a `__init__.py` file. The `__init__.py` file contains a Flask [`blueprint`](https://flask.palletsprojects.com/en/2.2.x/blueprints/). This blueprint can either be imported in the `<route>.py` file or can be extended with another blueprint. The `<route>.py` file contains the route logic.

The `__init__.py` file handles registering the blueprint with the Flask application.


```
📂nebula
 ┣ 📂routes // [!code focus:7]
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜api_route.py
 ┃ ┗ 📂web
 ┃ ┃ ┣ 📜__init__.py 
 ┃ ┃ ┣ 📜web_route.py
 ┣ 📂src
```

## Using Routes

The `web` and `api` blueprints can be imported and used directly or extended with another blueprint. Extending the `web` and `api` blueprints is useful for creating routes that are specific to a module. For example, the `user` module has a `user` blueprint that extends the `web` blueprint. This allows the `user` module to have its own routes that are prefixed with `/user`.

The API Blueprint automatically prefixes all routes with `/api`


### Using a blueprint directly

```python {4,7}
# your_route.py

# import the web blueprint
from nebula.routes.web import bp as web_bp

# Add your routes
@web_bp.route('/your_route')
def your_route():
    # available at /your_route
    return 'Hello World'

@web_bp.route('/another_route')
def another_route():
    # available at /another_route
    return 'Hello World'
```

### Extending a blueprint

```python {4,7,10}
# your_route.py

# import the web blueprint
from nebula.routes.web import bp as web_bp

# Create a new blueprint that will contain the routes for your route
bp = Blueprint('your_route', __name__, url_prefix='/your_route')

# Extend the web blueprint with your blueprint
web_bp.register_blueprint(bp)

# Add your routes
@bp.route('/')
def your_route():
    # available at /your_route/
    return 'Hello World'

@bp.route('/another_route')
def another_route():
    # available at /your_route/another_route
    return 'Hello World'
```