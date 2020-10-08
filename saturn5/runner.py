import os
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from docker.api import APIClient
from docker.constants import DEFAULT_DOCKER_API_VERSION

EXAMPLE = {
    "djangoDir": "./backend",
    "staticFrontend": {
        "buildDir": "./frontend",
        "buildCommand": "yarn build",
        "serveDir": "./frontend/build"
    }
}

BACKEND_SCHEMA = {
    "type": "object",
    "properties": {
        "djangoDir": {"type": "string"}
    },
    "required": ["djangoDir"]
}

FRONTEND_SCHEMA = {
    "type": "object",
    "properties": {
        "buildDir": {"type": "string"},
        "buildCommand": {"type": "string"},
        "serveDir": {"type": "string"}
    },
    "required": ["buildDir", "buildCommand", "serveDir"]
}

SCHEMA = {
    "type": "object",
    "properties": {
        "backend": BACKEND_SCHEMA,
        "frontend": FRONTEND_SCHEMA
    },
    "required": ["backend"]
}

SATURN_JSON = "./saturn5.json"


def __get_docker():
    client = APIClient(version=DEFAULT_DOCKER_API_VERSION)
    return client


def __get_saturn_json():
    with open(SATURN_JSON, "r") as f:
        app_metadata = json.load(f)
    return app_metadata


def check():
    # Make sure Docker and Docker Compose are installed
    try:
        client = __get_docker()
        client.ping()
    except Exception as e:
        print("Docker is not installed.")
        print(e)
        return False

    # Confirm saturn5.json is in project
    if not os.path.exists(SATURN_JSON):
        print("Not in project directory or no saturn5.json file created yet.")
        return False

    # Read JSON file
    try:
        app_metadata = __get_saturn_json()
    except Exception as e:
        print("saturn5.json could not be accessed. Are permissions set properly?")
        print(e)
        return False

    # Validate Saturn5 JSON
    try:
        validate(instance=app_metadata, schema=SCHEMA)
    except ValidationError as e:
        print("saturn5.json failed validation")
        print(e)
        return False

    # Confirm manage.py location
    django_root = app_metadata["backend"]["djangoDir"]
    manage_path = os.path.join(django_root, "manage.py")
    if not os.path.exists(manage_path):
        print("Configured djangoRoot does not contain a manage.py file. Check path set in saturn5.json")
        return False

    print("Saturn5 Validation Succeed")
    return True


def run():
    if not check():
        return False

    # Create Docker Client
    client = __get_docker()

    # Fire up Docker Compose for the current build

    # Use bind mounts to mount the
    client.create_volume()
    container = client.containers.run('ubuntu:latest', 'ls -ltr /tmp',
                                      volumes={os.getcwd(): {'bind': '/tmp/', 'mode': 'rw'}}, detach=True)
    print(container.logs())

    # Need to use bind mounts
    # https://docs.docker.com/storage/bind-mounts/

    #

    return True


def new():
    pass


def shell():
    if not check():
        return False
    return True
