import mangadex_py.http as http

api_url_manga = "https://api.mangadex.org/manga"
api_url_home = "https://api.mangadex.org/at-home/server"

def get_chapter_images(chapter_id_list, quality) : #other quality mode : "dataSaver" for compressed images
    """
    this function will return the chapter hash , the base url and a list of pictures filenames
    which are all needed to download the pictures.
    """
    for chapter_id in chapter_id_list :
        images_info = http.get(f"{api_url_home}/{chapter_id}").json()
        if images_info["result"] == "error" :
            print("no images found could be an external link.")
            continue
        else :
            chapter_info = images_info["chapter"]
            chapter_images = chapter_info[quality]
            base_url = images_info["baseUrl"]
            chapter_hash = chapter_info["hash"]
        return base_url, chapter_hash, chapter_images
    return None, None, None

def get_chap_vol(chap_vol_info) :
    volumes_list = list(chap_vol_info.keys())[::-1] #list from last to first volume this is why i reversed it.
    chapters_complete = list()
    for volume in volumes_list :
        chapters = chap_vol_info[volume]["chapters"] #workaround for f6e7ce00-e09c-4ed2-b806-eb2fdc7a5f60 
        if type(chapters) is dict :
            chapters_list = list(chapters.keys())[::-1]
            chapters_complete += [*chapters_list]
        else :
            continue
    return chapters_complete, volumes_list

def get_chapters(uuid) :
    """returns 2 lists of all volumes and chapters respectively"""
    chap_vol_info = http.get(f"{api_url_manga}/{uuid}/aggregate").json()["volumes"]
    chapters_complete, volumes = get_chap_vol(chap_vol_info)
    return chapters_complete, volumes

def gen_chapters(sel_chap) :
    sel_chap_list = sel_chap.strip().split(" ")
    gen_sel_list = list()
    for chap in sel_chap_list :
        if "-" in chap :
            rg = chap.split("-")
            for i in range(int(rg[0]), int(rg[-1]) + 1) :
                gen_sel_list.append(str(i))
            continue
        gen_sel_list.append(chap)
    return sorted(set(gen_sel_list))


def get_chapters_by_lang(uuid, lang, sel_chap) :
    if lang == None :
        lang = "en"
    chapters_data = http.get(f"{api_url_manga}/{uuid}/aggregate?translatedLanguage%5B%5D={lang}").json()["volumes"]
    avl_chap_list, avl_vol_list = get_chap_vol(chapters_data)
    if sel_chap:
        gen_chap = gen_chapters(sel_chap)
    return avl_chap_list, avl_vol_list, chapters_data, gen_chap if sel_chap else None

def prep_chap_down(lang_resp, avl_vol, avl_chap, down_chap) :
    down_chap_list = list()
    for vol in avl_vol :
        for chap in down_chap if down_chap else avl_chap:
            chapter_info = lang_resp[vol]["chapters"][chap]
            chapter_count = chapter_info["count"]
            chapter_id_list = list()
            chapter_id = chapter_id_list.append(chapter_info["id"])
            if chapter_count > 1 :
                for chapter_id in chapter_info["others"] :
                    chapter_id_list.append(chapter_id)
            down_chap_list.append((vol, "Oneshot", chapter_id_list) if chap == "none" else (vol, chap, chapter_id_list)) #https://github.com/frozenpandaman/mangadex-dl/blob/3883aa49d52e2c7c3f914f43a6e5fdd3aeebbedf/mangadex-dl.py#L102
    return down_chap_list