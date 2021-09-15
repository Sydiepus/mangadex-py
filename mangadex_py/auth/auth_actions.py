import mangadex_py.http as http
from mangadex_py.fs import write_follow_list

api_url = "https://api.mangadex.org/user/"

def get_follow_list(token) :
    bearer = {"Authorization": f"Bearer {token}"}
    offset = 0
    body = {"limit": 100, "offset": offset}
    req = http.get(api_url + "follows/manga", headers=bearer, params=body).json()
    total = req["total"]
    uuid_list = list()
    if total <= 100 :
        for i in req["data"] :
            uuid = i["id"]
            uuid_list.append(uuid)
    else :
        offset += 100
        while offset <= total :
            req = http.get(api_url + "follows/manga", headers=bearer, params=body).json()
            for i in req["data"] :
                uuid = i["id"]
                uuid_list.append(uuid)
    file = write_follow_list(uuid_list)
    return file