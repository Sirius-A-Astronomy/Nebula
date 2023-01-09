# Models

Models are defined in the `models` directory. Each model is defined in its own file. For example, the `User` model is defined in `models/user.py`.

The `__init__.py` file in the `models` directory is used to import all of the models. This file is imported in `nebula/__init__.py` and is used to create the database tables.

```
📂instance // [!code focus:2]
 ┣ 📜site.db
📂nebula
 ┣ 📂models // [!code focus:3]
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜user.py
 ┃ ...
 ┣ 📜__init__.py // [!code focus]
 ...
📜config.py // [!code focus]
 ```

## Database

The database is defined in `nebula/__init__.py`. The database is defined using [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) and [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).

### Configuration

The database configuration is defined in `/config.py`. The current database is an sqlite database stored in `instance/site.db`.

## Base Model

The base model is defined in `nebula/models/__init__.py`. The base model is used to define the default fields for all models. It adds the following fields to all models:

- `id`: The primary key for the model
- `uuid`: A unique identifier for the model
- `created_at`: The date and time the model was created
- `updated_at`: The date and time the model was last updated

## Creating a Model

To create a new model, create a new file in the `models` directory. The file name should be the name of the model in snake case. For example, the `User` model is defined in `models/user.py`.

The model should extend the base model. For example, the `User` model extends the base model:

```python {2,5}
# nebula/models/user.py // [!code focus:5]
from nebula.models import Base 
from nebula import db

class User(Base):
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    ...
```