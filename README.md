Challenge
========================

# Create Docker image
`docker build . -t challengeapp`

# Start app with Docker
`docker-compose up`

Note: this needs to be executed after you run the command to create Docker image

# UnitTest
you can run the unit test by `python3 -m unittest tests/test_app.py` just make sure you have DB running

# Run without docker
install dependencies `python install -r requirements.txt`
have a database and modify the uri db in `app.conf`
execute `python app.py`

# PostMan Link 
`https://www.getpostman.com/collections/263d14fa976716c6aba9`

# Terminal Commands
- Register user
```shell script
curl --location --request POST 'localhost:5000/register' \                                                                                                                                      Sat Nov 21 03:37:48 2020
                      --header 'Content-Type: application/json' \
                      --data-raw '{
                          "password": "test",
                          "name": "test",
                          "admin": false
                      }'
```

- Login (this will return the token to be used after
```shell script
curl --location --request POST 'localhost:5000/register' \                                                                                                                                      Sat Nov 21 03:37:48 2020
                      --header 'Content-Type: application/json' \
                      --data-raw '{
                          "password": "test",
                          "name": "test",
                          "admin": false
                      }'
```

- Get Exchange values
```shell script
curl --location --request GET 'localhost/exchange' \
--header 'x-access-token: USE THE TOKEN RETURNED IN LAST CALL'```
