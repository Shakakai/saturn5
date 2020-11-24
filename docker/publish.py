import os
from pathlib import Path
from saturn5.project import ACCEPTED_NODE_VERSIONS

PYTHON_BASE = "python-base"
LOCAL_DJANGO_WORKER = "local-django-worker"
LOCAL_DJANGO_SERVER = "local-django-server"
LOCAL_FRONTEND_BUILDER = "local-frontend-builder"


def run_docker_build(context_path, tag, build_args=None):
    print(f"Running docker build for: {context_path}")
    build_args_str = ""
    if build_args is not None:
        for key in build_args:
            build_args_str += f" --build-arg {key}={build_args[key]}"

    print(f"Executing command: docker build -t {tag}{build_args_str} {context_path}")
    with os.popen(f"docker build -t {tag}{build_args_str} {context_path}") as stream:
        print(stream.read())
    print(f"Executing command: docker push {tag}")
    with os.popen(f"docker push {tag}") as stream:
        print(stream.read())
    print(f"Complete build for: {context_path}")


def tag(project, version="latest"):
    return f"shakakai/{project}:{version}"


def run_builder_build(version):
    context_path = Path.cwd() / LOCAL_FRONTEND_BUILDER
    builder_tag = tag(LOCAL_FRONTEND_BUILDER, f"nodejs-{version}")
    args = {
        "NODE_VERSION": version
    }
    return run_docker_build(context_path, builder_tag, args)


def run_builds():
    # python base
    run_docker_build(Path.cwd() / PYTHON_BASE, tag(PYTHON_BASE))

    # django server
    run_docker_build(Path.cwd() / LOCAL_DJANGO_SERVER, tag(LOCAL_DJANGO_SERVER))

    # django worker
    run_docker_build(Path.cwd() / LOCAL_DJANGO_WORKER, tag(LOCAL_DJANGO_WORKER))

    # frontend builder
    for version in ACCEPTED_NODE_VERSIONS:
        run_builder_build(version)


if __name__ == "__main__":
    run_builds()
