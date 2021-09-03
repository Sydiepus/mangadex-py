import os, json
from mangadex_py.fs import replace_single_quote


file_name = ".dex"
home = os.path.expanduser("~")
file = os.path.join(home, file_name)


def write_auth_file(hexbytes) :
    f = open(file, "wb")
    f.write(hexbytes)
    f.close()

def read_auth_file() :
    f = open(file, "r")
    content = f.readline().encode("utf-8")
    return content

def auth_file_exists() :
    if os.path.exists(file) :
        return True
    else :
        return False

def deserialize_json(bytes) :
    return json.loads(replace_single_quote(bytes))