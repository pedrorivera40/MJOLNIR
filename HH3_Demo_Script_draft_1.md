# HH3 Demo

This is an overview of the main capabilities to showcase during the Oral Exam's presentation for MJölrnir's system. The main capabilities to showcase will be Authorization, User Management, Event Management, Team Management, Athlete Management, and Play by Play Management .  The Authentication module must be able to authenticate users, and provide a token that allows the authenticated user to access protected resources. The User Management module must be able to perform CRUD operations on Dashboard Users. The Event Management Module must be able to perform CRUD operations on Events. The Team and Athlete Modules must be able to perform CRUD operations on Team and Athletes respectively. Finally the PBP module must be able to perform CRUD operations on Volleball PBP events.

## Authentication Module

For the Authentication module we want to showcase the login process and the token creation as well as token verification.

1. Login with valid credentials **[SW-R: 5a Sec-R: 2a, 2b, 2c, 2d, 3a, 3b, 3c, 3d]**.
2. Try login in to an inactive account **[Sec-R: 2f, 3f]**.
3. Verify the token is created and the user is added to the vuex store **[Sec-R: 2c]**.
4. Verify requests contain the token for the user.
5. Verify the token successfully passes the API's token check.
6. Logout from the session **[SW-R: 5b, 6a, Sec-R: 3g, 3h]**
7. Lock a User's account with 3 erroneous logins **[SW-R: 1h, Sec-R: 2e, 3e]**.
8. Try to login to the deactivated user account **[Sec-R: 2f, 3f]**
9. Activate a user's account using the temp password **[SW-R: 1c, 1i, 1j, 1k, Sec-R: 2g, 2i, 2j]**.
10. Login again **[Sec-R: 3i]**.

## User Management Module

For the user management module we want to showcase we are able to perform CRUD operations on dashboard users. And that these operations are propagated to the Database.

1. Go to 'Manejo de Usuarios' to see all users **[SW-R: 1d]**.
2. Create a new user from the user management page with a compliant password **[SW-R: 1a, 1b ]**.
3. Edit a user's information **[SW-R: 1e]**.
4. Edit a User's Permissions **[SW-R: 1g]**.
5. Delete a user **[SW-R: 1f]**.
6. Reset a User's Password Using the User Management Page **[SW-R: 1j, 1k, Sec-R: 2h]**.

## Sports Module

This module is divided in two components: View and API Routes. Demonstration for this module will take place as part of the other modules that are integrated with it (Team and Athlete modules). The following segment briefly describes each component of the Sports module.

1. Its view allows users to navigate to the team profile of interest (both Freya and Loki). Presents the user with a list of sport cards which are filtered by the sport branch. When clicked, these redirect to the latest team profile for the desired sport.

2. Its API routes expose information regarding the sports covered by the system such as: list of sports by branch, sport entry given its id or sport name, list categories of a sport given its id, and a list of sport detail entries.

## Athlete Module

For the Athlete module we want to showcase the creation of at least
two athletes(one for a sport with positions and another one for a 
sport with categories) and to show the athle profile viewer page
where they can see an athletes info including their season stats.

1. Create an athlete that participates in a sport with positions
assigning the positions to the athlete from the athlete 
management page.**[SOFTWARE REQUIREMENTS 4D,4E]**

2. Create an athlete that participates in a sport with categories
assigning the categories to the athlete. from the athlete
management page.**[SOFTWARE REQUIREMENTS 4F]**

3. Edit an athlete profiles information.**[SOFTWARE REQUIREMENTS 4G]**

4. Delete an existing athlete.**[SOFTWARE REQUIREMENTS 4H]**

## Team Management Module

For the Team Management module we want to showcase we are able to perform CRUD operations on Team Profiles, and that these operations are propagated to the Database (seen in both dashboard and website views).

1. Create a Team (Select Sport, Select Create Team Option) **[Software Requirement 4A]**
2. Edit the information of the created team. (Select Edit Team Button) **[Software Requirement 4B]**
3. Add Team Members to the Created Team (Add Team Members Button) **[Software Requirement 4I]**
4. Remove the Added Athletes from the Team
5. Delete the Created Team (Remove Team Button) **[Software Requirement 4C]**
6. Select a previously existing team, show team members, team statistics and team event history.
7. Select a previously existing team from different sport, show difference in team statistics fields.

## Event Module

For the Event module we want to showcase the creation of an event,
the event viewer page and the results page for an event that has 
statistics recorded.

1. Go to events management page to see a list of created events.**[SOFTWARE REQUIREMENTS 2B]**

2. Create an event from the event management page.**[SOFTWARE REQUIREMENTS 2A]**

3. Edit the information of an existing event.**[SOFTWARE REQUIREMENTS 2C]**

4. Delete an event.**[SOFTWARE REQUIREMENTS 2E]**

5. Select an event with statistics to view and then click on 
the "see results button" to be redirected to the results page.**[SOFTWARE REQUIREMENTS 2D]**

## PBP Management Module
This module allows dashboard users to control the PBP sequence as a Volleyball game takes place. Note that this information is also displayed on the Freya website for general fanbase to view. As for this demonstration, the objective is to create a new PBP sequence for an existing Volleyball game, and modify the game sequence by adding the athletes that participate, adding game actions, updating opponent team color, adjusting game score, and changing the current set value. Finally the game will be marked as ended.

1. Go to events management page to see a list of created events. (similar as in the previous demonstration).

2. Find an event in the list that shows the button "Crear PBP" to create a PBP sequence (use pagination if needed) **[SOFTWARE REQUIREMENTS 3K]**.

3. Validate it corresponds to a Volleyball event and press the "Crear PBP" button. **[SOFTWARE REQUIREMENTS 3A]**

4. Move to the "Acciones Generales" section within the PBP page and click in the "Color de Oponente" button.

5. Choose the desired color for opponent game action cards and press "Guardar". **[SOFTWARE REQUIREMENTS 3B]**

6. Move to the "Administrador de Jugadas" section, and on the left side press the button for choosing UPRM athletes who will participate on the event.

7. Click on the checkbox of those athletes that will participate, and then press "Salir" to exit the modal. **[SOFTWARE REQUIREMENTS 3C, 3E]**

8. Move back to the "Administrador de Jugadas" section, and on the right side press the button for managing opponent athletes who will participate on the event.

9. Here we can add, edit, and delete the opponent team participants. **[SOFTWARE REQUIREMENTS 3D, 3F]**

10. At this point we are ready to add, edit, and remove game actions. **[SOFTWARE REQUIREMENTS 3G, 3H, 3I]**

11. Move to the "Acciones Generales" section, and press the "Finalizar" button.

12. Validate the cloud function was triggered and the statistics were synchronized. **[SOFTWARE REQUIREMENTS 3J]**

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

## Error Handling Athlete & Events

For the error handling portion we want to showcase the system's resilience to erroneous inputs. In the front end this can be seen by the UI setting restrictions when erroneous input is entered, and notifications when erroneous actions are performed in the system. In terms of the back end this can be seen by running the tests, outlined in the testing sheet, for the back end's athlete & event management capabilities.

1. Trying to create an athlete without the required fields.

2. Trying to create an athlete with information that does not conform to the
athlete profile field formats.

3. Trying to edit an athlete with information that does not conform to the
athlete profile field formats.

4. Trying to create an event without the required fields.

5. Trying to create an event with information that does not conform to the
athlete profile field formats.

6. Trying to edit an event with information that does not conform to the
athlete profile field formkats.
