# Writing documentation

Nebula uses [VitePress](https://vitepress.vuejs.org/) to generate the documentation. VitePress is a documentation generator that uses [Vue](https://vuejs.org/) and [Vite](https://vitejs.dev/) to create a single page application (SPA) documentation website.

VitePress takes markdown files and generates a static website from them. The markdown files are located in the `docs` directory.

## Getting started

To get started with the documentation, you need to install the dependencies and start the development server.

### Install dependencies

To install the dependencies, run the following command:

```bash
npm install
```

### Start development server

To start the development server, run the following command:

```bash
npm run docs:dev
```

This will start the development server on port `5173` (If you already have the vite devserver running it will start on port `5174`).

Now you can start working on the documentation.

### Building the documentation

After you have made changes to the documentation, you need to build the documentation to be able to see them in the local nebula website.

```bash
npm run docs:build
```

This will build the documentation and place it in the `docs/.vitepress/dist` directory.

Now you should be able to go to `/docs` on the local nebula website and see the changes.

## Writing documentation

The documentation is written in markdown files. The markdown files are located in the `docs` directory.

::: tip Learn more about markdown
To learn more about markdown, see the [documentation](https://www.markdownguide.org/).
:::

::: tip Learn more about VitePress
To learn more about VitePress, see the [documentation](https://vitepress.vuejs.org/).
:::

