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

-   Loading the configuration from `config.py`
-   Authentication via [Flask Login](https://flask-login.readthedocs.io/en/latest/)
-   Database via [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
-   csrf protection via [Flask WTF](https://flask-wtf.readthedocs.io/en/0.15.x/)
-   Context processors for global functions in templates via `nebula/helpers/global_functions.py`
-   Error handlers for 4xx and 5xx errors via `nebula/routes/web/errors.py`

### Routes

The routes are split into two categories: API and Web. The API routes are used for communicating with the database and the Web routes are used for rendering the frontend.

```
📂nebula
 ┣ 📂routes
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜api_route.py
 ┃ ┗ 📂web
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜web_route.py
 ┣ ...
```

::: tip More Information
For more information on the routes, see the [Routes](/developer/backend/routes) section.
:::

### Models

The models are used to define the database schema. The models are defined using [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) and [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).

Models are defined in the `models` directory. Each model is defined in its own file. For example, the `User` model is defined in `models/user.py`.

```
📂nebula
 ┣ 📂models
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜user.py
```

::: tip More Information
For more information on the models, see the [Models](/developer/backend/models) section.
:::

## Frontend

The frontend of nebula is created with the Javascript Framework [Vue](https://vuejs.org/).

Any assets that are imported in the frontend are located in the `nebula/src` directory.

```
📦nebula/src
 ┣ 📂js
 ┣ 📂public
 ┃ ┣ 📂images
 ┃ ┗ 📂js
 ┣ 📂scss
```

::: tip More Information
Learn more about how assets are imported in nebula in the [Importing Assets](/developer/frontend/importing-assets) section.
:::

### `Vue`

The frontend is written with [Vue](https://vuejs.org/). Vue is a frontend framework that is used to create reactive components. The frontend is responsible for rendering the pages and handling user interactions.

All of the Vue rendering in contained within the `nebula/src/js` directory.

Nebula uses `Vue`\'s [`Composition API`](https://vuejs.org/guide/extras/composition-api-faq.html) to create components. The `Composition API` is a new way to create components in `Vue` that is more flexible and allows for better code organization.

```
📦nebula/src/js
 ┣ 📂components
 ┣ 📂views
 ┣ 📂stores
 ┣ 📂vue-services
 ┣ 📂lib
 ┣ 📂http
 ┣ 📜router.ts
 ┣ 📜App.ts
 ┣ 📜App.vue
 ┣ 📜BaseLayout.vue
 ┣ 📜DashBoardLayout.vue
```

::: tip Learn more about `Vue`
Learn more about `Vue` using their [documentation](https://vuejs.org/guide/).

They provide an excellent documentation that will help you get started with `Vue`.
:::

#### `App.ts`

This is the main entry point for the frontend. This file is responsible for creating the Vue instance and mounting the application to the DOM.
This is the file that is loaded by the `nebula/templates/index.html` file which is the response the server sends for any webpage request.

#### `router.ts`

This file is responsible for creating the Vue router. The Vue router is responsible for handling the frontend routing. The frontend routing is used to determine which page to render based on the URL.

#### `App.vue`

This is the root Vue component. This component is responsible for rendering the layout of the application. The layout is determined by the URL. The layout is either the `BaseLayout.vue` or the `DashBoardLayout.vue` component.

It also contains common components that are used across all pages such notifications and modals.

#### `BaseLayout.vue`

This is the base layout for the application. This layout is used for all pages except the dashboard. This layout contains the navigation bar and the footer.

#### `DashBoardLayout.vue`

This is the dashboard layout for the application. This layout is used for the dashboard page. This layout contains the navigation bar and the footer.

#### Components

The `components` directory contains the individual components for the frontend.

#### Views

The `views` directory contains the individual views for the frontend. These views will then be places in the `RouterView` component in their respective layouts.

#### Stores

Stores are used to store the state of the frontend. The stores are located at `nebula/src/js/stores`.

The stores directory contains a storeFactory.ts file. The storeFactory.ts file is used to create most of the stores. The storeFactory.ts file is located at `nebula/src/js/stores/factory/storeFactory.ts`.

#### Vue Services

Vue services are used to define reusable functions for the frontend. The vue services are located at `nebula/src/js/vue-services`.

#### lib

The `lib` directory contains various reusable functions and classes that are used across the frontend. For example, the `lib` directory contains `mathjax.ts` which is used to load and instantiate MathJax.

#### http

The `http` directory contains an api service that is used to make api calls to the backend. The api service is located at `nebula/src/js/http/api.ts`.

It provides `get`, `post`, `put`, and `delete` methods to make api calls.
