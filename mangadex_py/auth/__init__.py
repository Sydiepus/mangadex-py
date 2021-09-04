import mangadex_py.http as http
import json, re
from .auth_fs import write_auth_file, auth_file_exists, read_auth_file, deserialize_json
from .crypto import decrypt, encrypt

api_url = "https://api.mangadex.org/auth/"



def payload_handler(username_email, password) :
    if (re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", username_email)) : #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/ 
        email = username_email
        payload = {"email": email,
                   "password": password}
    else :
        username = username_email
        payload = {"username": username,
                   "password": password}
    return payload

def get_cred() :
    print("your username/email nor your password will be saved only the token.")
    username_email = str(input("Please enter your email or username : "))
    password = str(input("Please enter your password : "))
    return username_email, password

def get_token(username_email, password) :
    payload = payload_handler(username_email, password)
    req = http.post(api_url + "login", json=payload)
    resp = req.json()
    if req.status_code == 200 :
        token = resp["token"]["session"]
        refresh = resp["token"]["refresh"]
        return token, refresh
    else : 
        error = resp["errors"][0]["detail"]
        print(error)
        return auth_file_setup()

def auth_file_setup() :
    username_email, password = get_cred()
    token, refresh = get_token(username_email, password)
    hex_encrypted = encrypt(token, refresh)
    write_auth_file(hex_encrypted)
    return token, refresh

def read_auth_file_main() :
    content = read_auth_file()
    json_file = decrypt(content)
    return json_file

def check_token(token) :
    bearer = {"Authorization": f"Bearer {token}"}
    req = http.get(api_url + "check", headers=bearer)
    resp = req.content.decode("utf-8")
    resp_json = deserialize_json(resp)
    return resp_json["isAuthenticated"]

def refresh_token(refresh) :
    payload = {"token": refresh}
    req = http.post(api_url + "refresh", json=payload)
    resp = req.content.decode("utf-8")
    resp_json = json.loads(resp)
    if req.status_code == 200 :
        token = resp_json["token"]["session"]
        refresh_n = resp_json["token"]["refresh"]
        return token, refresh_n
    else : 
        error = resp["errors"][0]["detail"]
        print(error)
        return refresh_token(refresh)

def auth() :
    if auth_file_exists() :
        json_data = read_auth_file_main()
        token = json_data["token"]
        if not check_token(token) :
            refresh = json_data["refresh"]
            token, refresh = refresh_token(refresh)
    else :
        token, refresh = auth_file_setup()
    return token