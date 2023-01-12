# How does Nebula work?


## User Roles and Permissions

Nebula has 5 user roles:

| Role        	| Access Level 	| Description                                                                                  	|
|-------------	|--------------	|----------------------------------------------------------------------------------------------	|
| Not Logged In 	| n/a            	| A user that is not logged in. They can only view questions and comments.                      	|
| Guest       	| 0            	| A guest is an unverified logged in user. They can only view questions and comments.            	|
| Student     	| 1            	| A student is a verified user. They can post comments.                   	|
| Moderator   	| 2            	| A moderator (most likely a member from KLC) moderates Nebula. They can post/edit/delete questions and comments. 	|
| Admin       	| 3            	| An admin manages the site. They can post/edit/delete questions and comments, and change courses. 	|
| Maintainer  	| 4            	| A maintainer is a developer. They can do everything.                                        	|

Any user that has access to the dashboard can update the access_level of any user with a lower access level. This means that a moderator can update the access level of a student, but not an admin. They can change the access level of a student to any level below their own. For example, a moderator can change a student's access level to guest, but not admin.

The following table shows the permissions of each role:

|              | Post/edit/delete Questions | Edit/delete all questions | Post/Edit/Delete comments | Edit/Delete all comments | Nebula Dashboard | Change Courses |
|--------------|----------------------------|---------------------------|---------------------------|--------------------------|------------------|----------------|
| 0 Guest      | 0                          | 0                         | 0                         | 0                        | 0                | 0              |
| 1 Student    | 0                          | 0                         | 1                         | 0                        | 0                | 0              |
| 2 Moderator  | 1                          | 0                         | 1                         | 1                        | 1                | 0              |
| 3 Admin      | 1                          | 1                         | 1                         | 1                        | 1                | 1              |
| 4 Maintainer | 1                          | 1                         | 1                         | 1                        | 1                | 1              |
