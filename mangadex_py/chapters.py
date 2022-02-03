import time
import mangadex_py.http as http

api_url = "https://api.mangadex.org/chapter"
api_url_manga = "https://api.mangadex.org/manga"
api_url_home = "https://api.mangadex.org/at-home/server"
avail_lang_chap_list, avail_lang_chap = list(), list() #only when fetching with lang 

"""
this function will return the chapter hash , the base url and a list of pictures filenames
which are all needed to download the pictures.
"""
def get_chapter_images(chapter_id, quality) : #other quality mode : "dataSaver" for compressed images
    images_info = http.get(f"{api_url_home}/{chapter_id}").json()
    if images_info["result"] == "error" :
        print("no images found could be an external link.")
        base_url, chapter_hash, chapter_images = None, None, None
    else :
        chapter_info = images_info["chapter"]
        chapter_images = chapter_info[quality]
        base_url = images_info["baseUrl"]
        chapter_hash = chapter_info["hash"]
    return base_url, chapter_hash, chapter_images

def get_lang(chapter_data) :
    avail_lang = list()
    for chapter in chapter_data :
        lang = chapter["attributes"]["translatedLanguage"]
        if lang not in avail_lang and avail_lang != None :
            avail_lang.append(lang)
    return avail_lang

def get_total_chap_vol(uuid) :
    chap_vol_info = http.get(f"{api_url_manga}/{uuid}/aggregate").json()["volumes"]
    volumes_list = list(chap_vol_info.keys())[::-1] #list from last to first volume this is why i reversed it.
    chapters_complete = list()
    for volume in volumes_list :
        chapters = chap_vol_info[volume]["chapters"] #workaround for f6e7ce00-e09c-4ed2-b806-eb2fdc7a5f60 
        if type(chapters) is dict :
            chapters_list = list(chapters.keys())[::-1]
            chapters_complete += [*chapters_list]
        else :
            continue
    return chapters_complete #volumes are not being used so it's best if i don't return them.

def get_avail_lang(uuid) :
    chapter_data = http.get(f"{api_url_manga}/{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500").json()["data"]
    avail_lang = get_lang(chapter_data)
    return avail_lang

def save_lang_time(chapter_data, quality) :
    for chapter in chapter_data :
        try :
            vol = chapter["attributes"]["volume"]
            chap = chapter["attributes"]["chapter"]
            id = chapter["id"]
            fetched = False
            if f"{vol}-{chap}" not in avail_lang_chap :
                avail_lang_chap.append(f"{vol}-{chap}")
            else :
                index = avail_lang_chap.index(f"{vol}-{chap}")
                chapter = avail_lang_chap_list[index]
                fetched = chapter[3]
                if fetched :
                    continue
                double_id = chapter[2]
                base_url, chap_hash, chap_img = get_chapter_images(double_id, quality)
                if base_url == chap_hash == chap_img == None :
                    base_url, chap_hash, chap_img = get_chapter_images(id, quality)
                    if base_url == chap_hash == chap_img == None :
                        continue
                fetched = True
                avail_lang_chap_list[index] = (vol, "Oneshot", (base_url, chap_hash, chap_img), fetched) if chap == None else (vol, chap, (base_url, chap_hash, chap_img), fetched)
                continue
            avail_lang_chap_list.append((vol, "Oneshot", id, fetched) if chap == None else (vol, chap, id, fetched)) #https://github.com/frozenpandaman/mangadex-dl/blob/3883aa49d52e2c7c3f914f43a6e5fdd3aeebbedf/mangadex-dl.py#L102
        except KeyError :
            continue

def no_chap_for_lang(uuid, lang) :
    avail_lang =  get_avail_lang(uuid)
    print(f"no chapters for '{lang}' were found.")
    print(f"available languages {avail_lang}")

def get_chapter_info_by_lang(uuid, lang, quality) : 
    offset = 0
    chapter_resp = http.get(f"{api_url_manga}/{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}").json()
    chapter_data = chapter_resp["data"]
    total_chap = chapter_resp["total"]
    if total_chap == 0 :
        no_chap_for_lang(uuid, lang)
        return None, None
    if total_chap < 500 :
        save_lang_time(chapter_data, quality)
    else :
        offset += 500
        save_lang_time(chapter_data, quality)
        while offset < total_chap :
            chapter_data = http.get(f"{api_url_manga}/{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}").json()["data"]            
            save_lang_time(chapter_data)
            offset += 500
            time.sleep(0.25)
    return avail_lang_chap_list, avail_lang_chap