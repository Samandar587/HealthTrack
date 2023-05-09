README

This project implements a RESTful service that allows doctors and medical professionals to access and update a patient's medical history. The service allows for basic CRUD operations, including creating new patient records, retrieving existing patient records, updating existing patient records, and deleting patient records. The patient's medical history includes basic information such as their name, date of birth, and medical conditions.

To run the application and tests, follow the steps below:

## Set up and Run the Application

1. Clone the repository and navigate to the project directory:

```
https://github.com/Samandar587/HealthTrackAPI.git
cd HealthTrackAPI
```

2. Create and activate a Python virtual environment:

```
python3 -m venv env
source env/bin/activate
```

3. Create a .env file in the root directory of the project and add the following environment variables:

```
SECRET_KEY=your_secret_key_here
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=database_host
DB_PORT=database_port

```


4. Install the required packages:

```
pip install -r requirements.txt
```

5. Start the application:

```
docker-compose up -d
```

This command will start the application and its dependencies (database, etc.) in Docker containers.

6. Run database migrations:

```
docker-compose exec web python manage.py migrate
```

7. Create a superuser account:

```
docker-compose exec web python manage.py createsuperuser
```

8. Access the API at http://localhost:8000/health_track/api/

## Run the Tests

1. Run the unit tests:

```
docker-compose exec web coverage run --source='.' manage.py test patient_records/tests/
```

2. Generate a coverage report:

```
docker-compose exec web coverage report
```

## Accessing the API Endpoints

The API endpoints can be accessed at http://localhost:8000/health_track/api/. The following endpoints are available:

- `/patient/`: Make a get request to this endpoint to list all patients or create a new patient record.
- `/patient/{id}/`: Make a get, put and delete requests to retrieve, update and delete a patient record respectively.
- `/filtered_patients/?name=John`: Search or filter the patient records by name, address, and date of birth
- `/medical_files/{id}/upload`: Upload a medical file for a patient.
- `/medical_files/{id}/download`: Download a patient's file.

To access any of these endpoints, you will need to provide appropriate authentication credentials. Specifically, only authorized medical professionals should be able to access a patient's medical history. You can use your superuser username and password to authenticate. The authentication type is Basic Auth.

## Uploading and Downloading Medical Files

To upload a medical file, make a POST request to the `/medical_files/{id}/upload` endpoint with the file in the request body.

To download a medical file, make a GET request to the `/medical_files/{id}/download/` endpoint.