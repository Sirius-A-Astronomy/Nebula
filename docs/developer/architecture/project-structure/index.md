# Project Structure

Nebula uses a [Flask](https://flask.palletsprojects.com/en/2.0.x/) backend and a [Vite](https://vitejs.dev/) + [Vue](https://vuejs.org/) frontend. The project structure is as follows:



```
📂docs
📂nebula
 ┣ 📂cli
 ┣ 📂models
 ┣ 📂routes
 ┣ 📂src
 ┣ 📂static
 ┣ 📂templates
 ┣ 📂helpers
 ┣ 📜__init__.py
📜config.py
...
```

## Backend

The backend is written in Python and uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework. The backend is responsible for handling requests from the frontend and communicating with the database.

### `__init__.py`

This file is the entry point for the backend. This is where the Flask app is created and the database is initialized. The routes are also registered in this file.

It sets up the following:
- Loading the configuration from `config.py`
- Authentication via [Flask Login](https://flask-login.readthedocs.io/en/latest/)
- Database via [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- csrf protection via [Flask WTF](https://flask-wtf.readthedocs.io/en/0.15.x/)
- Context processors for global functions in templates via `nebula/helpers/global_functions.py`
- Error handlers for 4xx and 5xx errors via `nebula/routes/web/errors.py`

### Routes

The routes are split into two categories: API and Web. The API routes are used for communicating with the database and the Web routes are used for rendering the frontend.


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

::: tip More Information
For more information on the routes, see the [Routes](/developer/backend/routes) section.
:::

### Models

The models are used to define the database schema. The models are defined using [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) and [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).



Models are defined in the `models` directory. Each model is defined in its own file. For example, the `User` model is defined in `models/user.py`.

```
📂nebula
 ┣ 📂models // [!code focus:3]
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜user.py
 ```

::: tip More Information
For more information on the models, see the [Models](/developer/backend/models) section.
:::

## Frontend

::: warning Migration in Progress 
Nebula is currently in the process of migrating from `Flask` and `Jinja` templates to `Vite` and `Vue`.

The documentation is subject to change as the migration progresses.
:::

### `Flask` and `Jinja`

The frontend is written with templates using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/). The frontend is responsible for rendering the pages and handling user interactions.

The html templates are located in the `nebula/templates` directory. The `templates` directory is split into several subdirectories:

```
📂nebula
 ┣ 📂templates // [!code focus:10]
 ┃ ┣ 📂errors
 ┃ ┣ 📂layouts
 ┃ ┃ ┗ 📜base.html
 ┃ ┣ 📂main
 ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┗ 📜login.html
 ┃ ┗ 📂utilities
 ┃ ┃ ┣ 📜macros.html
 ┃ ┃ ┗ 📜vite.html
```

#### Layouts

The `layouts` directory contains the base template for the frontend. Individual pages can extend the base template to inherit the base layout. The base template is located at `nebula/templates/layouts/base.html`. To learn more about extending templates, see the [Jinja documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance).

#### Main

The `main` directory contains the individual pages for the frontend. The pages are usually rendered using the base template. The pages are located at `nebula/templates/main`.

#### Utilities

The `utilities` directory contains the macros and vite template. The macros are used to define reusable blocks of code. The macros are located at `nebula/templates/utilities/macros.html`. 

The vite template is used to load vite assets. The vite template is located at `nebula/templates/utilities/vite.html`.


### Serving frontend assets with `Vite`

Currently `Vite` is used to build the frontend assets. `Vite` is a build tool that uses [ESM](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) imports to bundle the frontend assets. `Vite` is similar to [Webpack](https://webpack.js.org/) but is much faster.


```
📦nebula/src
 ┣ 📂js
 ┣ 📂public
 ┃ ┣ 📂images
 ┃ ┗ 📂js
 ┣ 📂scss
 ```

Any assets that are imported in the frontend are located in the `nebula/src` directory.

During development, `Vite` is used to serve the frontend assets with their web server. Vite will watch for changes in the frontend assets and automatically reload the page. 

During production, `Vite` is used to build the frontend assets. The frontend assets are built into the `nebula/static` directory. Vite will create a manifest file that maps the asset names to their hashed names. The manifest file is located at `nebula/static/manifest.json`.

::: tip More Information
Learn more about how assets are imported in nebula in the [Importing Assets](/developer/frontend/importing-assets) section.
:::

### `Vue`

::: warning Migration in Progress
Nebula is currently in the process of migrating from `Flask` and `Jinja` templates to `Vite` and `Vue`.

The documentation is subject to change as the migration progresses.
:::

The frontend is written with [Vue](https://vuejs.org/). Vue is a frontend framework that is used to create reactive components. The frontend is responsible for rendering the pages and handling user interactions.

The frontend is located in the `nebula/src/js` directory. The frontend is split into several subdirectories:

```
📦nebula/src/js
 ┣ 📂components
 ┣ 📂views
 ┣ 📂stores
 ┣ 📂vue-services
 ┣ 📂add_question
 ┣ 📂dashboard
 ┣ 📜router.ts
```

Since Nebula is still migrating there is no single frontend entry point. Currently these are the frontend entry points:

- `nebula/templates/main/dashboard/index.html`
  - Which imports `nebula/src/js/dashboard/dashboardMain.ts`
- `nebula/templates/main/add_question.html`
  - Which imports `nebula/src/js/add_question/add_question.ts`

These entry ts files import their respective Vue apps and mount them to the DOM.

#### Components

The `components` directory contains the individual components for the frontend. The components are located at `nebula/src/js/components`.

#### Views

The `views` directory contains the individual views for the frontend. The views are located at `nebula/src/js/views`.

#### Stores

Stores are used to store the state of the frontend. The stores are located at `nebula/src/js/stores`.

The stores directory contains a storeFactory.ts file. The storeFactory.ts file is used to create most of the stores. The storeFactory.ts file is located at `nebula/src/js/stores/factory/storeFactory.ts`.

#### Vue Services

Vue services are used to define reusable functions for the frontend. The vue services are located at `nebula/src/js/vue-services`.

#### `router.ts`

The `router.ts` file is used to define the routes for the frontend. The routes are located at `nebula/src/js/router.ts`.

