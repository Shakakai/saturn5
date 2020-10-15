import os
import json
import subprocess

from saturn5.project import Project
from saturn5.utils.docker import validate_docker_installation, get_docker_client, run_docker_compose


def check():
    # Make sure Docker and Docker Compose are installed
    valid, reason = validate_docker_installation()
    if not valid:
        print(f"Error. {reason}")
        return False

    # Read JSON file
    try:
        project = Project()
    except Exception as e:
        print("Loading saturn5.json failed.")
        print(e)
        return False

    # Confirm manage.py location
    manage_path = project.backend.directory / "manage.py"
    if not manage_path.exists():
        print("Configured djangoRoot does not contain a manage.py file. Check path set in saturn5.json")
        return False

    print("Saturn5 Validation Succeed")
    return True


def run():
    if not check():
        return False

    project = Project()

    env_vars = {
        "PROJECT_DIR": str(project.directory),
    }

    if project.backend is not None:
        env_vars["BACKEND_PORT"] = project.backend.port
        env_vars["BACKEND_DIR"] = str(project.backend.directory)

    if project.frontend is not None:
        env_vars["FRONTEND_DIR"] = str(project.frontend.directory)
        env_vars["FRONTEND_PORT"] = str(project.frontend.port)
        env_vars["NODE_VERSION"] = project.frontend.node_version
        env_vars["FRONTEND_BUILD_CMD"] = project.frontend.build_command
        env_vars["FRONTEND_DEV_CMD"] = project.frontend.development_command
        env_vars["FRONTEND_BUILD_DIR"] = str(project.frontend.build_directory)

    if project.database is not None:
        env_vars["DATABASE_ENGINE"] = project.database.engine
        env_vars["DATABASE_PORT"] = project.database.port
        env_vars["DATABASE_VERSION"] = project.database.version
        env_vars["DATABASE_USERNAME"] = project.database.username
        env_vars["DATABASE_PASSWORD"] = project.database.password

    if project.cache is not None:
        env_vars["CACHE_ENGINE"] = project.cache.engine
        env_vars["CACHE_VERSION"] = project.cache.version
        env_vars["CACHE_PORT"] = project.cache.port

    if project.email is not None:
        env_vars["EMAIL_SMTP_PORT"] = project.email.smtp_port
        env_vars["EMAIL_HTTP_PORT"] = project.email.http_port

    try:
        run_docker_compose(project.name, ["up"], env_vars)
    except Exception as e:
        run_docker_compose(project.name, ["down"], env_vars)

    return True


def new():
    pass


def shell():
    if not check():
        return False
    return True
