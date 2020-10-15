from pathlib import Path
import subprocess

from docker.api import APIClient
from docker.constants import DEFAULT_DOCKER_API_VERSION

from saturn5.utils.file import write_dotenv


def get_docker_client():
    client = APIClient(version=DEFAULT_DOCKER_API_VERSION)
    return client


def validate_docker_installation():
    # Make sure Docker and Docker Compose are installed
    msg = ""
    result = True

    try:
        client = get_docker_client()
        client.ping()
    except Exception as e:
        result = False
        msg = "Docker is not installed and is required."

    try:
        subprocess.run(["docker-compose", "version"], check=True, capture_output=True)
    except Exception as e:
        result = False
        msg += "Docker Compose is not installed and is required."

    return result, msg


def compose_file_path():
    current_file = Path(__file__)
    project_dir = current_file.parent.parent.parent
    return project_dir / "docker" / "compose.yml"


def run_docker_compose(project_name, commands, env_vars):
    if commands is None or len(commands) == 0:
        raise Exception("Must provide commands as a list larger than zero to run_docker_compose")

    # write the env vars to a file for use by docker-compose
    dotenv_path = Path(f"/tmp/{project_name}")
    write_dotenv(dotenv_path, env_vars)

    print("dotenv content")
    with dotenv_path.open() as f:
        print(f.read())

    # Lets do this.
    # Fire up docker-compose
    base_commands = [
        "docker-compose",
        "-f", str(compose_file_path()),
        "--env-file", str(dotenv_path)
    ]
    subprocess.run(base_commands + commands, check=True, capture_output=False)
