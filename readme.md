# CAPSTONE - A Casting Agency Application

## Specifications

The application aims in providing backend apis for the crew members to create and manage movies along with its cast.


## Motivation
This is the final project in the FSND Udacity, which asses the knowledge of the candidate in building apis's using python, Flask, SqlAlchemy, Auth0 and Heroku.

## Pre-Requirements
### Dependencies
The techstack that this application use are python, Heroku and postgresql.

The following dependencies should be installed prior running the application
1. python (3.7 or higher)
2. pip (preinstalled with python)
3. postgresql (optional - if you use remote server)
4. Heroku CLI (tested with 7.53.0)

## Running in Local (Optional)

###### Note: This is information section to run application in local, skip to "Access API's in Heroku" section for testing this application live in heroku

### Backend

Clone source from the below repo
https://github.com/dvinodbabu/capstone.git

1. setup a virtual environment
```
cd ${PROJECT_PATH}\backend
python3 -m venv myenv
dev\Scripts\activate.bat
```
2. Install the python dependencies
```
cd ${PROJECT_PATH}\backend
pip install -r requirements.txt
```

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. 

```bash
cd ${PROJECT_PATH}\backend
createdb casting
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py seed
```
## Roles 
1. Create a application and api "casting" in Auth0
2. Create 3 users with below permissions for API's
 Ex-:
    * executive_producer@outlook.com
    * casting_assitant@outlook.com
    * casting_director@outlook.com
```
PERMISSION          ASSISTANT           DIRECTOR            PRODUCER 
----------------------------------------------------------------------   
get:artist              *                   *                   *
get:movies              *                   *                   *
post:artist                                 *                   *
post:movies                                                     *
delete:artist                               *                   *
delete:movies                                                   *
patch:artist                                *                   * 
```

### Environment Variables

Configure setup.bat/setup.sh according to your configurations you have created in Auth) and Postgres.

Note: The below are required only for running testcases.
* export ASSISTANT_TOKEN=
* export DIRECTOR_TOKEN=
* export PRODUCER_TOKEN= 

### Run (Local)
Start the python app
```
cd ${PROJECT_PATH}\backend
python3 -m venv myenv
dev\Scripts\activate.bat
setup.bat (or sh setup.sh for linux)
flask run
```
Access the below url in browser
https://dev-j5-9ahca.us.auth0.com/authorize?audience=casting&response_type=token&client_id=vlViuA63Vez7RG7Yzz3MG9dxYgEliiZ7&redirect_uri=https://localhost:5000/

You will be greeted with a login page. Enter anyone of the credentials you have created in Auth0 page.
After successful login you will be redirected with a access token in the redirection url.
Use that token in postman to set the request header to access the permitted end points for the user.
Access http://localhost:5000/logout to test the application for other user as the session in Auth0 defaultly return token to the first user that have logged in to the system

### Access API's in Heroku


## API Documentation

* Base URL: The backend is hosted at `https://capstoneprojectbyvinod.herokuapp.com/`
* Authentication: Auth0

Below is the username and password configured in Auth0 (Refer to the "Roles" section on the permission)
* executive_producer@outlook.com/ExecutiveProducer@123
* casting_assitant@outlook.com/CastingAssistant@123
* casting_director@outlook.com/CastingDirector@123

Use the below url to login and generate token for the user.
https://dev-j5-9ahca.us.auth0.com/authorize?audience=casting&response_type=token&client_id=vlViuA63Vez7RG7Yzz3MG9dxYgEliiZ7&redirect_uri=https://capstoneprojectbyvinod.herokuapp.com/

Note: Use https://capstoneprojectbyvinod.herokuapp.com/logout endpoint to initiate the login sequence again for a different user.

### Error Handling

Errors are returned in the below JSON format:
```
    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }
```
The API will return the following types of errors:

* 500 - Server Error
* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 401 - Authorization Error

## API end-points

#### GET /artists
* Definition: fetches list of artists from the database
* Sample: `curl --location --request GET "https://capstoneprojectbyvinod.herokuapp.com/artists" --header "Authorization: Bearer {access_token}"`<br>


#### POST /artists
* Definition: creates a new artist in the database
* Sample: `curl --location --request POST "https://capstoneprojectbyvinod.herokuapp.com/artists" --header "Authorization: Bearer {access_token}" --header "Content-Type: application/json" --data-raw "{\"name\": \"Will Smith\", \"age\": \"45\", \"gender\": \"male\", \"phone\": \"871869523\"}"`<br>


#### PATCH /artists/{artist.id}
* Definition: updates a existing artist information in the database
* Sample: `curl --location --request PATCH "https://capstoneprojectbyvinod.herokuapp.com/artists/{artist.id}" --header "Authorization: Bearer {access_token}" --header "Content-Type: application/json" --data-raw "{\"name\": \"Will Smith\", \"age\": \"45\", \"gender\": \"male\", \"phone\": \"871869523\"}"`<br>


#### DELETE /artists/{artist.id}
* Definition: delete a existing artist information from the database
* Sample: `curl --location --request DELETE "https://capstoneprojectbyvinod.herokuapp.com/artists/{artist.id}" --header "Authorization: Bearer {access_token}"`<br>


#### GET /movies
* Definition: fetches list of movies from the database
* Sample: `curl --location --request GET "https://capstoneprojectbyvinod.herokuapp.com/movies" --header "Authorization: Bearer {access_token }"`<br>


#### POST /movies
* Definition: creates a new movie in the database
* Sample: `curl --location --request POST "https://capstoneprojectbyvinod.herokuapp.com/movies" --header "Authorization: Bearer {access_token}" --header "Content-Type: application/json" --data-raw "{\"title\": \"Captain America\", \"release_date\": \"2020-03-02\", \"genre\": \"SuperHero\"}"`<br>


#### DELETE /movies/{movie.id}
* Definition: delete a existing movie from the database
* Sample: `curl --location --request DELETE "https://capstoneprojectbyvinod.herokuapp.com/movies/{movie.id}" --header "Authorization: Bearer {access_token}"`<br>
