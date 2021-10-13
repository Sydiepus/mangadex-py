import mangadex_py.http as http
import re 
from .fs import remove_special_character

api_url = "https://api.mangadex.org/"

def get_default_title(resp) :
    title_default_lang = list(resp["data"]["attributes"]["title"])[0]
    title = resp["data"]["attributes"]["title"][f"{title_default_lang}"]
    return title

def get_altTitles_lang(resp, lang, *n) :
    altTitles = resp["data"]["attributes"]["altTitles"]
    altTitles_lang = []
    for i in altTitles :
        try :
            altTitles_lang.append(i[f"{lang}"])
        except KeyError :
            continue
    if len(altTitles_lang) > 0 :
        if n == () :
            return altTitles_lang[0]
        elif 0 <= n[0] < len(altTitles_lang) :
            return altTitles_lang[n[0]]
        elif n[0] >= len(altTitles_lang) :
            #print("index out of range using the first one in the list.")
            return altTitles_lang[0]
    else : 
        #print("No altTitles with that language found; using default title.")
        return get_default_title(resp)
        
def get_title(resp, langWithIndex) :
    if langWithIndex == () :
        return get_default_title(resp)
    else :
        if len(langWithIndex) > 1 :
            return remove_special_character(get_altTitles_lang(resp, langWithIndex[0], langWithIndex[1]))
        else :
            return remove_special_character(get_altTitles_lang(resp, langWithIndex[0])) 
            

def get_default_description(resp) :
    description_default_lang = list(resp["data"]["attributes"]["description"])[0]
    description = resp["data"]["attributes"]["description"].get(str(description_default_lang))
    return description

def get_description_lang(resp, lang) :
    description = resp["data"]["attributes"]["description"]
    if description.get(lang) == None :
        return get_default_description(resp)
    else :
        return description.get(lang)
    # else : 
    #     print("No description with that language found; using default title.")
    #     return get_default_title(resp)

def get_description(resp, langWithIndex) :
    if langWithIndex == () :
        return get_default_description(resp)
    else :
        return get_description_lang(resp, langWithIndex[0])

def get_status(resp) :
    status = resp["data"]["attributes"]["status"]
    return status

# def get_tags(resp) :
#     tags_list = list()
#     for i in resp["data"]["attributes"]["tags"] :
#         a = list(i["attributes"]["name"])
#         tags_list.append(i["attributes"]["name"][a[0]])
#     return tags_list

def get_info(uuid, langWithIndex) :
    request = http.get(f"{api_url}manga/{uuid}")
    if request.status_code == 200 :
        resp = request.json()
        title = get_title(resp, langWithIndex)
        desc = get_description(resp, langWithIndex)
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

def rename_main(naming, digits, curly_count, special=None) :
    if len(digits) <= curly_count :
        return rename(naming, digits, special)
    else :
        index = naming.find("{}")
        diff = len(digits) - curly_count
        new_naming = naming[:index] + "{}" * diff + naming[index:]
        return rename(new_naming, digits, special)

def rename(naming, digits, special=None) :
    b = naming
    if special == None :
        for i in range(0, len(digits) + 1) :
            try :
                b = rreplace(b, "{}", digits[i], 1)
            except IndexError :
                c = b.replace("{}", "0")
                return c
    else :
        for i in range(0, len(digits) + 1) :
            try :
                b = rreplace(b, "{}", digits[i], 1)
            except IndexError :
                c = b.replace("{}", "0")
                return c + f"-{special}"


def rreplace(string, old, new, occurrence) :
    li = string.rsplit(old, occurrence)
    return new.join(li)

def custom_naming_main(chapter_number, naming) :
    chapter = chapter_number.split(".") #check for special
    a = naming.count("{}")
    digits = []
    for i in chapter :
        for p in i :
            digits.append(p)
        digits = digits[::-1]
        if len(chapter) > 1 :
            special = chapter[-1]
            return rename_main(naming, digits, a, special)
        else :
            return rename_main(naming, digits, a)

def naming_main(volumes, i, zip_name=None) :
    if zip_name == None :
        if volumes != [] and len(i) == 3:
            contain_vol = True
            chapter = f"vol-{i[1]}-chapter-{i[0]}"
            return chapter, contain_vol
        else :
            chapter = f"chapter-{i[0]}"
            contain_vol = False
            return chapter, contain_vol
    else :
        contain_vol = False
        return custom_naming_main(i[0], zip_name), contain_vol