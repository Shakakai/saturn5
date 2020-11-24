from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from saturn5.utils.file import read_json

EXAMPLE = {
  "name": "django-todo-react",
  "database": {
    "engine": "postgres",
    "version": "12.3",
    "port": 5432
  },
  "backend": {
    "directory": "./backend",
    "port": 5000
  },
  "frontend": {
    "directory": "./frontend",
    "buildCommand": "npm install && npm build",
    "developmentCommand": "npm install && npm start",
    "buildDirectory": "./frontend/build",
    "nodeVersion": "6.1.14",
    "port": 8000
  },
  "cache": {
    "engine": "redis",
    "version": "5.0",
    "port": 6379
  },
  "email": {
    "httpPort": 8025,
    "smtpPort": 1025
  }
}

BACKEND_SCHEMA = {
    "type": "object",
    "properties": {
        "directory": {"type": "string"},
        "port": {"type": "number"}
    },
    "required": ["directory", "port"]
}

FRONTEND_SCHEMA = {
    "type": "object",
    "properties": {
        "directory": {"type": "string"},
        "buildCommand": {"type": "string"},
        "developmentCommand": {"type": "string"},
        "buildDirectory": {"type": "string"},
        "nodeVersion": {"type": "string"},
        "port": {"type": "number"}
    },
    "required": ["directory", "buildCommand", "developmentCommand", "buildDirectory", "nodeVersion", "port"]
}

DATABASE_SCHEMA = {
    "type": "object",
    "properties": {
        "engine": {"type": "string"},
        "version": {"type": "string"},
        "port": {"type": "number"},
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["engine", "version", "port"]
}

CACHE_SCHEMA = {
    "type": "object",
    "properties": {
        "engine": {"type": "string"},
        "version": {"type": "string"},
        "port": {"type": "number"}
    },
    "required": ["engine", "version", "port"]
}

EMAIL_SCHEMA = {
    "type": "object",
    "properties": {
        "httpPort": {"type": "number"},
        "smtpPort": {"type": "number"}
    },
    "required": ["httpPort", "smtpPort"]
}

MAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "backend": BACKEND_SCHEMA,
        "frontend": FRONTEND_SCHEMA,
        "database": DATABASE_SCHEMA,
        "cache": CACHE_SCHEMA,
        "email": EMAIL_SCHEMA,
        "name": {"type": "string"},
        "version": {"type": "string"}
    },
    "required": ["backend", "database", "cache", "name", "version"]
}

SATURN_JSON = "./saturn5.json"


def key_exists_and_isnt_none(obj, key):
    return key in obj and obj[key] is not None


def rel_path(pth):
    return Path.cwd() / Path(pth)


ACCEPTED_NODE_VERSIONS = [
    "10",
    "12",
    "14",
    "15"
]


class Frontend:
    def __init__(self, metadata):
        self.directory = rel_path(metadata["directory"])
        self.build_command = metadata["buildCommand"]
        self.development_command = metadata["developmentCommand"]
        self.build_directory = rel_path(metadata["buildDirectory"])
        self.node_version = metadata["nodeVersion"]
        self.node_major_version = self.node_version.split(".")[0]
        if self.node_major_version not in ACCEPTED_NODE_VERSIONS:
            raise Exception(f"Node version is not supported. \n" +
                            f"Major Node version provided: {self.node_major_version} \n" +
                            f"Accepted Major Node versions: {ACCEPTED_NODE_VERSIONS}")
        self.port = metadata["port"]


class Backend:
    def __init__(self, metadata):
        self.directory = rel_path(metadata["directory"])
        self.port = metadata["port"]


class Database:
    def __init__(self, metadata):
        self.engine = metadata["engine"]
        self.version = metadata["version"]
        self.port = metadata["port"]
        self.username = metadata["username"]
        self.password = metadata["password"]


class Cache:
    def __init__(self, metadata):
        self.engine = metadata["engine"]
        self.version = metadata["version"]
        self.port = metadata["port"]


class Email:
    def __init__(self, metadata):
        self.http_port = metadata["httpPort"]
        self.smtp_port = metadata["smtpPort"]


PROJECT_CLASS_MAP = {
    "frontend": Frontend,
    "backend": Backend,
    "database": Database,
    "cache": Cache,
    "email": Email
}


class Project:

    def __init__(self):
        self._directory = Path.cwd()
        self._app_metadata = None
        self.frontend = None
        self.backend = None
        self.database = None
        self.cache = None
        self.email = None
        self._load_metadata()
        self._validate_metadata()
        self._setup_subobjects()

    def _load_metadata(self):
        metadata_path = self._directory / SATURN_JSON
        if not metadata_path.exists():
            raise Exception("Error: saturn5.json file does not exist in current working directory.")
        self._app_metadata = read_json(metadata_path)

    def _validate_metadata(self):
        try:
            validate(instance=self._app_metadata, schema=MAIN_SCHEMA)
        except ValidationError as e:
            raise Exception(f"Invalid saturn5.json metadata. {e}")

    def _meta_exists(self, key):
        return key_exists_and_isnt_none(self._app_metadata, key)

    def _setup_subobjects(self):
        for key in PROJECT_CLASS_MAP:
            if self._meta_exists(key):
                value = PROJECT_CLASS_MAP[key](self._app_metadata[key])
                setattr(self, key, value)

    @property
    def app_metadata(self):
        return self._app_metadata

    @property
    def directory(self):
        return Path.cwd()

    @property
    def name(self):
        return self._app_metadata["name"]

    @property
    def version(self):
        return self._app_metadata["version"]

