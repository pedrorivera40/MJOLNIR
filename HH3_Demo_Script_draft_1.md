# HH3 Demo

This is an overview of the main capabilities to showcase during the Oral Exam's presentation for MJölrnir's system. The main capabilities to showcase will be Authorization, User Management, Event Management, Team Management, Athlete Management, and Play by Play Management .  The Authentication module must be able to authenticate users, and provide a token that allows the authenticated user to access protected resources. The User Management module must be able to perform CRUD operations on Dashboard Users. The Event Management Module must be able to perform CRUD operations on Events. The Team and Athlete Modules must be able to perform CRUD operations on Team and Athletes respectively. Finally the PBP module must be able to perform CRUD operations on Volleball PBP events.

## Authentication Module

For the Authentication module we want to showcase the login process and the token creation as well as token verification.

1. Login with valid credentials [SW-R: 5a Sec-R: 2a, 2b, 2c, 2d, 3a, 3b, 3c, 3d].
2. Try login in to an inactive account [Sec-R: 2f, 3f].
3. Verify the token is created and the user is added to the vuex store [Sec-R: 2c].
4. Verify requests contain the token for the user.
5. Verify the token successfully passes the API's token check.
6. Logout from the session [SW-R: 5b, Sec-R: 3g, 3h]
7. Lock a User's account with 3 erroneous logins [SW-R: 1h, Sec-R: 2e, 3e].
8. Try to login to the deactivated user account [Sec-R: 2f, 3f]
9. Activate a user's account using the temp password [SW-R: 1c, 1i, 1j, 1k, Sec-R: 2g, 2i, 2j].
10. Login again [Sec-R: 3i].

## User Management Module

For the user management module we want to showcase we are able to perform CRUD operations on dashboard users. And that these operations are propagated to the Database.

1. Go to 'Manejo de Usuarios' to see all users [SW-R: 1d].
2. Create a new user from the user management page with a compliant password [SW-R: 1a, 1b ].
3. Edit a user's information [SW-R: 1e].
4. Edit a User's Permissions [SW-R: 1g].
5. Delete a user [SW-R: 1f].
6. Reset a User's Password Using the User Management Page [SW-R: 1j, 1k, Sec-R: 2h].

## Team Management Module

For the Team Management module we want to showcase we are able to perform CRUD operations on Team Profiles, and that these operations are propagated to the Database (seen in both dashboard and website views).

1. Create a Team (Select Sport, Select Create Team Option) **[Software Requirement 4A]**
2. Edit the information of the created team. (Select Edit Team Button) **[Software Requirement 4B]**
3. Add Team Members to the Created Team (Add Team Members Button) **[Software Requirement 4I]**
4. Remove the Added Athletes from the Team
5. Delete the Created Team (Remove Team Button) **[Software Requirement 4C]**
6. Select a previously existing team, show team members, team statistics and team event history.
7. Select a previously existing team from different sport, show difference in team statistics fields.


## Results Management Module

For the Results Management module we want to showcase we are able to perform CRUD operations on Results, and that these operations are propagated to the Database (seen in both dashboard and website views).

1. Go to a Basketball Event's Results (32), show Individual and Team Stats
2. Go to a Volleybal Event's Results (7), show Individual and Team Stats
3. Go to a Soccer Event's Results (10), show Individual and Team Stats
4. Go to a Baseball Event's Results (24), show Individual and Team Stats
5. Go to a Medal-Based Event's Results (36), show Individual and Team Stats
6. Go to a Match-Based Event's Results (19), show Individual and Team Stats 
7. Go to an existing even't results, Add Athlete Statistics for that Event, show how page updates both Individual and Team Stats **[Software Requirement 2D]**
8. Add Final Score for the Event **[Software Requirement 2D]**
9. Edit Final Score for the Event **[Software Requirement 2C (partially)]**
10. Edit one of the Athlete Statistics Records for the Event, show how page updates both Individual and Team Stats **[Software Requirement 2C (partially)]**
11. Delete one of the Athlete Statistics Record for the Event, show how page updates both Individual and Team Stats **[Software Requirement 2C (partially)]**

## Error Handling 

For the error handling portion we want to showcase the system's resilience to erroneous inputs. In the front end this can be seen by the UI setting restrictions when erroneous input is entered, and notifications when erroneous actions are performed in the system. In terms of the back end this can be seen by running the suit of tests for the back end's user management capabilities.

1. Trying to log in with an erroneous password.
2. Trying to create passwords that do not conform to the Password's Determined format.
3. Trying to log in with invalid usernames.
4. Try invalid email when adding a new user or editing a user.
5. Try modifying/deleting logged in user.
6. Try adding user with existing email.
7. Try adding user with existing username.
8. Try changing a user's username to an existing username.
9. Try changing a user's email to an existing email.

