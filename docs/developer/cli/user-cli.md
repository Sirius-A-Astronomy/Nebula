# This is the user CLI documentation.

Nebula has a few commands that can be used to manage users.

To start using the cli, navigate to the repository root and set the `FLASK_APP` environment variable to nebula

```bash
export FLASK_APP=nebula
```

Now you can use the cli commands.

## Create a user

To create a user, you can use the `flask user create` command. 

```bash
flask user create <username?> <password?> <access_level?> <create_instantly?>
```

### arguments
- `username`: String (optional): The username of the user. This is the name that will be used to log in. If not provided, the user will be prompted to enter a username.
- `password`: String (optional): The password of the user. This is the password that will be used to log in. If not provided, the user will be prompted to enter a password.
- `access_level`: String (optional) | Number (optional): The access level of the user. This is the level of access that the user will have. If not provided, the user will be prompted to enter an access level. To learn more about access levels, see [this page](/how-does-nebula-work.md#user-roles-and-permissions).
- `create_instantly`: ('y' | 'n') (optional): Whether or not the user should be created instantly. If 'y' the user will not be prompted to confirm any details, nor will they be prompted for additional details. 
## Delete a user

To delete a user, you can use the `flask user delete` command.

```bash
flask user delete <username?>
```

### arguments
- `username`: String (optional): The username of the user. If not provided, the user will be prompted to enter a username.

## List users

To list users, you can use the `flask user list` command. It will list all users in the database.

```bash
flask user list
```

## Edit a user

To edit a user, you can use the `flask user edit` command. It will ask for the username of the user to edit, and then prompt for the details to edit.

```bash
flask user edit <username?>
```

### arguments
- `username`: String (optional): The username of the user. If not provided, the user will be prompted to enter a username.

## Reset Password

To reset a user's password, you can use the `flask user reset-password` command. It will ask for the username of the user to reset the password of, and generate a new password for the user. The new password will be printed to the console.

```bash
flask user reset-password <username?>
```

### arguments

- `username`: String (optional): The username of the user. If not provided, the user will be prompted to enter a username.