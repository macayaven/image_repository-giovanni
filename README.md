# Image repository

## Requirements

- Python 3.8

## Basic usage

1. Clone this repo
2. Enter the repository folder and create a virtual environment: `python3 -m venv venv`
3. Activate the newly created virtual environment: `source venv/bin/activate`
4. Install the needed packages: `pip install -r requirements.txt`
5. Copy the `.env.example` file into `.env` and fill it with your database and Azure credentials.
6. Run the migrations: `python3 manage.py migrate`
7. Execute it with `python3 manage.py runserver`

Now, you can access the application through `localhost:8000` (api is under `localhost:8000/api/v1`)

### Test in Postman

You can use `data/image_repository.postman_collection.json` file to test the endpoints. 

To do so, you need to register in the app, login and the copy the token from the response. You must paste this token under Authorization section in the folder settings. The authorization type is API Key with 'Authorization' as key and 'tokan {response.token}' as value.