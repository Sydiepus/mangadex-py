import json
import time
import mangadex_py.http as http

api_url = "https://api.mangadex.org/chapter/"
api_url_manga = "https://api.mangadex.org/manga/"
api_url_home = "https://api.mangadex.org/at-home/server/"
chapters_fetched, base_url, chapters_images, images_links = list(), str(), list(), list()
avail_vol, avail_lang, avail_chap = list(), list(), list() #global non lang dependant stuff
avail_id, avail_lang_chap_list, avail_lang_chap = list(), list(), list() #only when fetching with lang 

def chapter_fetch(chap_hash) : 
    chapters_fetched.clear()
    chapter_fetch_rep = http.get(f"{api_url}{chap_hash}")
    chapter_fetch = json.loads(chapter_fetch_rep.text)
    chapters_fetched.append(chapter_fetch)
    return chapters_fetched #returns a list containing a dict with the chapter and the images for that chapter.

def base_url_fetch(lang_chap_list) :
    base_url = http.get(f"{api_url_home}{lang_chap_list[0][-1]}").json()["baseUrl"]
    return base_url

def get_chapter_images(chapters_fetched, quality_mode="data") : #dataSaver for compressed images.
    chapters_images.clear()
    for i in chapters_fetched :
        images = list()
        tmp_num = i["data"]["attributes"]["chapter"]
        tmp_hash = i["data"]["attributes"]["hash"]
        if len(i["data"]["attributes"][quality_mode]) == 0 :
            print("no images found for that chapter could be an external link.")
            return None
        for k in i["data"]["attributes"][quality_mode] :
            images.append(k)
        chapters_images.append((tmp_num, tmp_hash, quality_mode, images))
    return chapters_images

def get_images_links(chapters_images, baseurl) :
    images_links.clear()
    for i in chapters_images :
        tmp_links = list()
        chap_num = i[0]
        chap_hash = i[1]
        quality_mode = i[2]
        if quality_mode == "dataSaver" :
            quality_mode = "data-saver"
        for images in i[-1] :
            if "mangaplus" in images :
                print("mangaplus links are not supported for now i hope")
                return None
            else :
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
    resp = http.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&offset={offset}").json()
    total_chap = resp["total"]
    if total_chap < 500 :
        get_info(resp)
    else :
        offset += 500
        get_info(resp)
        while offset < total_chap :
            chapter_req = http.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&offset={offset}")
            time.sleep(0.25)
            resp = chapter_req.json()
            get_info(resp)
            offset += 500
    return avail_lang, avail_vol, avail_chap, total_chap

def save_lang_time(resp) :
    get_info(resp)
    for i in resp["results"] :
        try :
            tmp_vol = i["data"]["attributes"]["volume"]
            tmp_chap = i["data"]["attributes"]["chapter"]
            if tmp_chap not in avail_lang_chap :
                avail_lang_chap.append(tmp_chap)
            tmp_id = i["data"]["id"]
            if tmp_vol == None :
                avail_lang_chap_list.append(("Oneshot", tmp_id) if tmp_chap == None else (tmp_chap, tmp_id))
            else :
                avail_lang_chap_list.append(("Oneshot", tmp_vol, tmp_id) if tmp_chap == None else (tmp_chap, tmp_vol, tmp_id))
        except KeyError :
            continue

def get_chapter_info_by_lang(uuid, total_chap, lang="en") : 
    offset = 0
    chapter_req = http.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}")
    resp = chapter_req.json()
    if total_chap < 500 :
        save_lang_time(resp)
    else :
        offset += 500
        save_lang_time(resp)
        while offset < total_chap :
            chapter_req = http.get(f"{api_url_manga}{uuid}/feed?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]={lang}&offset={offset}")
            time.sleep(0.25)
            resp = chapter_req.json()
            get_info(resp)
            for i in resp["results"] :
                try :
                    tmp_vol = i["data"]["attributes"]["volume"]
                    tmp_chap = i["data"]["attributes"]["chapter"]
                    if tmp_chap not in avail_lang_chap :
                        avail_lang_chap.append(tmp_chap)
                    tmp_id = i["data"]["id"]
                    if tmp_vol == None :
                        avail_lang_chap_list.append(("Oneshot", tmp_id) if tmp_chap == None else (tmp_chap, tmp_id)) #https://github.com/frozenpandaman/mangadex-dl/blob/3883aa49d52e2c7c3f914f43a6e5fdd3aeebbedf/mangadex-dl.py#L102
                    else :
                        avail_lang_chap_list.append(("Oneshot", tmp_vol, tmp_id) if tmp_chap == None else (tmp_chap, tmp_vol, tmp_id))
                except KeyError :
                    continue
            offset += 500
    if avail_lang_chap_list == [] :
        print(f"no chapters for '{lang}' were found.")
        return None, None
    return avail_lang_chap_list, avail_lang_chap

def scanlation_group_selector(list_chap, quality_mode) :
    fetched_list = []
    images_list = list()
    len_list = list()
    for i in list_chap :
        fetch = chapter_fetch(i[-1])
        fetched_list = fetched_list[:] + fetch
    for i in fetched_list :
        images_list = images_list[:] + get_chapter_images([i], quality_mode)
    for i in images_list :
        len_list.append(len(i[-1]))
    index = len_list.index(max(len_list))
    return images_list[index]

def sort_chap_with_multi_scanlation(chapter, chapter_list, have_vol) :
    list_chap = list()
    if have_vol :
        for i in chapter_list[0:] :
            if (chapter[0], chapter[1]) == (i[0], i[1]) :
                list_chap.append(i)
                chapter_list.pop(chapter_list.index(i))
    else :
        for i in chapter_list[0:] :
            if chapter[0] == i[0] :
                list_chap.append(i)
                chapter_list.pop(chapter_list.index(i))
    return list_chap