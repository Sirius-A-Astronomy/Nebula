
[Back to the main page](/README.md)

# This is the database CLI Documentation.

Nebula has a few commands that can be used to manage the database.

To start using the cli, navigate to the repository root and set the `FLASK_APP` environment variable to nebula

```bash
export FLASK_APP=nebula
```

Now you can use the cli commands.

## Init

To init the database, you can use the `flask db init` command. This will create the database and all tables.

```bash
flask db init
```

## Drop

To drop the database, you can use the `flask db drop` command. This will drop the database and all tables.

```bash
flask db drop
```

## Reset

To reset the database, you can use the `flask db reset` command. This will drop the database and all tables, and then recreate them.

```bash
flask db reset
```

## Seed

To seed the database, you can use the `flask db seed` command. This will seed the database with some default data.

```bash
flask db seed
```

The seed data comes from JSON files in the `nebula/seed_data` directory.

