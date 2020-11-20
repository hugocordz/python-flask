Credijusto-Challenge
========================

# Create Docker image
`docker build . -t credijusto-app`

# Start app with Docker
`docker-compose up`

Note: this needs to be executed after you run the command to create Docker image

# UnitTest
you can run the unit test by `python3 -m unittest tests/test_app.py` just make sure you have DB running

# Run without docker
install dependencies `python install -r requirements.txt`
have a database and modify the uri db in `app.conf`
execute `python app.py`