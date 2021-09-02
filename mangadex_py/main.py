import mangadex_py.manga as manga
import mangadex_py.chapters as chapter
import mangadex_py.download as download
from tqdm import tqdm

def main(url, langWithIndex, quality_mode, Manga_main_dir, thread, manga_name=None) :
    bar = tqdm(desc="Initializing", total=5)
    uuid = manga.get_uuid(url)
    if manga_name == None :
        title, desc, status = manga.get_info(uuid, langWithIndex)
    else :
        title = manga_name.strip()
        _, desc, status = manga.get_info(uuid, langWithIndex)
    tqdm.write(f"{title} :")
    bar.update(2)
    language, volumes, _, totalchap = chapter.get_manga_chapters_info(uuid)
    bar.update(1)
    chap_list, lang_chap = chapter.get_chapter_info_by_lang(uuid, totalchap, langWithIndex[0])
    bar.update(1)
    if chap_list == None :
        tqdm.write(f"available languages are {language}")
        return 1
    tqdm.write(f"found {len(lang_chap)} out of {totalchap} for '{langWithIndex[0]}'")
    base_url = chapter.base_url_fetch(chap_list)
    bar.update(1)
    bar.close()
    print("starting download :")
    download.main(title, chap_list, desc, status, quality_mode, base_url, volumes, Manga_main_dir, thread)