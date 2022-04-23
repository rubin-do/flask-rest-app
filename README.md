# Rest flask user statistics website

## Build
```
    docker-compose build
```
## Run
```
    docker-compose up
```

## API

### Create new user
#### Source: localhost:5000/register

#### Method: POST
#### Data(JSON):
```
{
    "username": "example",
    "avatar": "http://example.com/pic.png",
    "sex": "Male",
    "email": "example@test.com"
}
```
Username field is required, other fields are optional. 

Returns user id:
```
{
    "id": 1
}
```
### Update user data
#### Source: localhost:5000/users/\<id>

#### Method: POST
#### Data(JSON):
```
{
    "username": "new_name",
    "avatar": "http://google.com/new_pic.png",
    "sex": "Female",
    "email": "newmail@test.com"
}
```
All fields are optional, needed to provide only fields that will change

### Get user profile
#### Source: localhost:5000/users/\<id>

#### Method: GET

Shows user profile and game statistics

### Delete user profile
#### Source: localhost:5000/users/\<id>

#### Method: DELETE

Deletes user profile

### Get all user profiles
#### Source: localhost:5000/users/all
#### Method: GET

Shows all user profiles on one page

### Get user statistics in pdf

#### Source: localhost:5000/users/\<id>/getstats
#### Method: GET
Returns:
```
{
    "link": "localhost:5000/pdf/\<id>"
}
```
After a short time pdf file with user statistics can be viewed via link

Note: custom user-avatar can increase waiting time

### Upload game statistics

#### Source: localhost:5000/add_game
#### Method: POST
#### Data(JSON):
```
{
    "duration": 1,
    "winners": [1,2,3],
    "losers": [4,5,6]
}
```
* duration -- time in hours
* winners -- id of players won the game
* losers -- id of players lost the game

## Example
1. Create users
    <details>
        <summary>Code</summary>

        
        curl --location --request POST 'http://127.0.0.1:5000/register' --header 'Content-Type: application/json' --data-raw '{"username": "Admin", "sex":"Male", "email":"secret@secret.com"}'
        

        
        curl --location --request POST 'http://127.0.0.1:5000/register' --header 'Content-Type: application/json' --data-raw '{"username": "Danya", "sex":"Male", "email":"danyarubin@gmail.com", "avatar":"https://img2.freepng.ru/20180523/tha/kisspng-businessperson-computer-icons-avatar-clip-art-lattice-5b0508dc6a3a10.0013931115270566044351.jpg"}'

        
    </details>
2. Update user info
    <details>
        <summary>Code</summary>

        curl --location --request POST 'http://127.0.0.1:5000/users/2' --header 'Content-Type: application/json' --data-raw '{"username": "Daniil"}'

    </details>
3. Upload game statistics
    <details>
        <summary>Code</summary>

        curl --location --request POST 'http://127.0.0.1:5000/add_game' --header 'Content-Type: application/json' --data-raw '{"winners":[1], "losers":[2], "duration":2}'

    </details>

4. Delete user
    <details>
        <summary>Code</summary>

        curl --location --request DELETE 'http://127.0.0.1:5000/users/2'

    </details>

5. Get user stats
    <details>
        <summary>Code</summary>

        curl --location --request GET 'http://127.0.0.1:5000/users/1/getstats'
    </details>