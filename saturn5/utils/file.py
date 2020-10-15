import json


def write_dotenv(path, env_vars:dict):
    keys = env_vars.keys()
    if len(keys) == 0:
        raise Exception("Must pass value to write env file. No key/values provided.")

    output = ""
    for key in env_vars.keys():
        output += f"{key}={env_vars[key]}\n"

    write_file(path, output)


def write_file(path, value):
    with path.open(mode="w") as f:
        f.write(value)


def read_file(path):
    result = ""
    with path.open(mode="r") as f:
        result = f.read()
    return result


def read_json(path):
    result = read_file(path)
    return json.loads(result)
