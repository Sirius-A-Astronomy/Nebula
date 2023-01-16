# Importing assets

Nebula uses [Vite](https://vitejs.dev/) to import assets into the frontend. Vite is a frontend build tool that is used to build the frontend assets. Vite is also used to serve the frontend assets during development.

## Project structure

The frontend assets are located in the `nebula/src` directory. The `nebula/src` directory is structured as follows:

```
📦nebula/src
 ┣ 📂js
 ┣ 📂public
 ┃ ┣ 📂images
 ┃ ┗ 📂js
 ┣ 📂scss
```

The `nebula/src/js` directory contains `TypeScript` and `Vue` files that are used to build the frontend. 

The `nebula/src/public` directory contains assets that are used directly by the frontend.

The `nebula/src/scss` directory contains `SCSS` files that are used to build the frontend styling.

::: info Note
The `nebula/src/public` directory is copied as is to the `nebula/static` directory during production.
:::

## Importing assets in `html` and `jinja`

Assets in `html` and `jinja` files need to import from different directories depending on the environment. During development, the assets are served by the `Vite webserver`. During production, the assets are built by `Vite` and are located in the `nebula/static` directory.

To help with this difference, the `vite` template is used to import assets. The `vite` template is located at `nebula/templates/utilities/vite.html`.

### Usage

The `vite` template provides the following functions:

#### `vite_script`

Imports a script. If the script imports any other assets, they will be imported as well.

param: `source` - The path to the script relative to the `nebula/src` directory.

Input:
```html
{{ vite_script('js/main.ts') }}
```

Output:
::: code-group
```html [Development]
<script type="module" src="http://localhost:5173/js/main.ts"></script>
```

```html [Production]
<script type="module" src="/static/js/main.js"></script>
<link rel="stylesheet" href="/static/main.css"></link>
```
:::

#### `vite_style`

Imports a style.

param: `source` - The path to the style relative to the `nebula/src` directory.

Input:
```html
{{ vite_style('scss/main.scss') }}
```

Output:
::: code-group
```html [Development]
<link rel="stylesheet" href="http://localhost:5173/scss/main.scss">
```

```html [Production]
<link rel="stylesheet" href="/static/main.css"></link>
```
:::

#### `vite_asset`

Imports an asset. The asset will be imported as is.

param: `source` - The path to the asset relative to the `nebula/src` directory.

Input:
```html
{{ vite_asset('js/main.js') }}
```

Output:
::: code-group
```html [Development]
http://localhost:5173/js/main.js
```

```html [Production]
/static/js/main.js
```
:::
#### `vite_public_asset`

Imports a public asset. The asset will be imported as is.
When importing a public asset, this function should be used instead of `vite_asset`. This is because vite serves plublic assets from the root directory.

param: `source` - The path to the asset relative to the `nebula/src/public` directory.

Input:
```html
{{ vite_public_asset('images/logo.svg') }}
```

Output:
::: code-group
```html [Development]
http://localhost:5173/images/logo.svg
```

```html [Production]
/static/images/logo.svg
```
:::


::: details utilities/vite.html
<<< @/../nebula/templates/utilities/vite.html
:::

## Importing assets in `TypeScript` and `Vue`

Assets in `TypeScript` and `Vue` files can just be imported the same way as in any other `TypeScript` or `Vue` project. Vite will handle the import depending on the environment.

```ts
// Import a script
import { createApp } from 'vue';

// Import a style
import '@scss/main.scss';

// Import an asset
import logo from '@public/images/logo.svg';
```


### Aliases

A few aliases are available to make it easier to import assets. The aliases are defined in `nebula/src/js/vite.config.ts`.

Creating a new alias is as simple as adding a new entry to the `resolve.alias` object in `vite.config.ts` and adding it to `"compilerOptions"."paths"` in `tsconfig.json`.

Adding the alias to `vite.config.ts` ensures that the alias will work in `TypeScript` and `Vue` files.

Adding the alias to `tsconfig.json` will allow editors to resolve the alias.

```ts
// vite.config.ts // [!code focus:4]
export default defineConfig({
  resolve: {
    alias: {
      // ...
      '@': path.resolve(__dirname, 'js'), // [!code focus:3]
      '@public': path.resolve(__dirname, 'public'),
      '@scss': path.resolve(__dirname, 'scss'),
      // ...
    },
  },
});
```

```json
// tsconfig.json // [!code focus:1]
{
  "compilerOptions": { // [!code focus]
    // ...
    "paths": { // [!code focus]
      // ...
      "@/*": ["js/*"], // [!code focus:3]
      "@public/*": ["public/*"],
      "@scss/*": ["scss/*"],
      // ...
    },
    // ...
  }
}
```
