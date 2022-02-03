import mangadex_py.http as http
import re 
from .fs import remove_special_character

api_url = "https://api.mangadex.org"

def get_default_title(resp) :
    title = list(resp["title"].values())[0]
    return title

def get_altTitles_lang(resp, lang, n=0) :
    altTitles = resp["altTitles"]
    altTitles_lang = []
    for i in altTitles :
        try :
            altTitles_lang.append(i[f"{lang}"])
        except KeyError :
            continue
    if len(altTitles_lang) > 0 :
            return altTitles_lang[n]
    else : 
        return get_default_title(resp)
        
def get_title(resp, langWithIndex) :
    if langWithIndex == (None, 0) :
        return get_default_title(resp)
    else :
        return remove_special_character(get_altTitles_lang(resp, langWithIndex[0], langWithIndex[1]))            

def get_default_description(resp) :
    description = list(resp.values())[0]
    return description

def get_description_lang(resp, lang) :
    desc_lang = resp.get(lang)
    if desc_lang == None :
        return get_default_description(resp)
    else :
        return desc_lang

def get_description(resp, lang) :
    if lang == None :
        return get_default_description(resp)
    else :
        return get_description_lang(resp, lang)

def get_status(resp) :
    status = resp["status"]
    return status

def get_info(uuid, langWithIndex) :
    request = http.get(f"{api_url}/manga/{uuid}")
    if request.status_code == 200 :
        resp = request.json()["data"]["attributes"]
        title = get_title(resp, langWithIndex)
        desc = get_description(resp["description"], langWithIndex[0])
        status = get_status(resp)
        return title, desc, status
    else :
        error = f"Something is wrong i can feel it {request}"
        return error

def get_uuid(url) :
    if "mangadex" in url :
        for i in url.split("/") :
            uuid = re.findall(".+-.+-.+-.+", i)
            if len(uuid) == 1 :
                return uuid[0]
    else :
        uuid = re.findall(".+-.+-.+-.+", url)
        if len(uuid) == 1 :
            return uuid[0]
        else :
            print("Please enter a mangadex url")