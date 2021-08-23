import requests, json

api_url = "https://api.mangadex.org/chapter/"
api_url_manga = "https://api.mangadex.org/manga/"
api_url_home = "https://api.mangadex.org/at-home/server/"
chapters_fetched, base_url, chapters_images, images_links = list(), str(), list(), list()
avail_vol, avail_lang, avail_chap = list(), list(), list() #global non lang dependant stuff
avail_id, avail_lang_chap_list, avail_lang_chap = list(), list(), list() #only when fetching with lang 

def chapters_fetch(lang_chap_list) :
    for i in lang_chap_list :
        chapter_fetch_rep = requests.get(f"{api_url}{i[-1]}")
        chapter_fetch = json.loads(chapter_fetch_rep.text)
        chapters_fetched.append(chapter_fetch)
    return chapters_fetched #returns a list containing a dict with the chapter and the images for that chapter.

def base_url_fetch(lang_chap_list) :
    base_url = requests.get(f"{api_url_home}{lang_chap_list[0][-1]}").json()["baseUrl"]
    return base_url

def get_chapters_images(chapters_fetched, quality_mode="data") : #data-saver for compressed images.
    for i in chapters_fetched :
        images = list()
        tmp_num = i["data"]["attributes"]["chapter"]
        tmp_hash = i["data"]["attributes"]["hash"]
        for k in i["data"]["attributes"][quality_mode] :
            images.append(k)
        chapters_images.append((tmp_num, tmp_hash, quality_mode, images))
    return chapters_images

def get_images_links(chapters_images, baseurl) :
    for i in chapters_images :
        tmp_links = list()
        chap_num = i[0]
        chap_hash = i[1]
        quality_mode = i[2]
        for images in i[-1] :
            tmp_links.append(f"{baseurl}/{quality_mode}/{chap_hash}/{images}")
        images_links.append((chap_num, tmp_links))
    return images_links

def get_info(resp) :
    for i in resp["results"] :
        tmp_lang = i["data"]["attributes"]["translatedLanguage"]
        tmp_chap = i["data"]["attributes"]["chapter"]
        try :
            tmp_vol = i["data"]["attributes"]["volume"]
            if tmp_vol not in avail_vol and tmp_vol != None :
                avail_vol.append(tmp_vol)
        except KeyError :
            print("no Volumes for this manga.")
            continue
        if tmp_lang not in avail_lang and tmp_lang != None:
            avail_lang.append(tmp_lang)
        if tmp_chap not in avail_chap and tmp_chap != None:
            avail_chap.append(tmp_chap)

def get_manga_chapters_info(uuid) :
    offset = 0
    resp = requests.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&offset={offset}").json()
    total_chap = resp["total"]
    if total_chap < 500 :
        get_info(resp)
    else :
        offset += 500
        get_info(resp)
        while offset < total_chap :
            chapter_req = requests.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&offset={offset}")
            resp = chapter_req.json()
            get_info(resp)
            offset += 500
    return avail_lang, avail_vol, avail_chap, total_chap

def save_lang_time(resp) :
    get_info(resp)
    for i in resp["results"] :
        try :
            tmp_chap = i["data"]["attributes"]["chapter"]
            if tmp_chap not in avail_lang_chap :
                avail_lang_chap.append(tmp_chap)
            tmp_id = i["data"]["id"]
            avail_lang_chap_list.append(("Oneshot", tmp_id) if tmp_chap == None else (tmp_chap, tmp_id))
        except KeyError :
            continue

def get_chapter_info_by_lang(uuid, total_chap, lang="en") : 
    offset = 0
    index = 0
    chapter_req = requests.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}")
    resp = chapter_req.json()
    if total_chap < 500 :
        save_lang_time(resp)
    else :
        offset += 500
        save_lang_time(resp)
        while offset < total_chap :
            chapter_req = requests.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}")
            resp = chapter_req.json()
            get_info(resp)
            for i in resp["results"] :
                try :
                    tmp_chap = i["data"]["attributes"]["chapter"]
                    if tmp_chap not in avail_lang_chap :
                        avail_lang_chap.append(tmp_chap)
                    tmp_id = i["data"]["id"]
                    avail_lang_chap_list.append(("Oneshot", tmp_id) if tmp_chap == None else (tmp_chap, tmp_id)) #https://github.com/frozenpandaman/mangadex-dl/blob/3883aa49d52e2c7c3f914f43a6e5fdd3aeebbedf/mangadex-dl.py#L102
                except KeyError :
                    continue
            offset += 500
    return avail_lang_chap_list, avail_lang_chap