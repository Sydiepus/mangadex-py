import mangadex_py.manga as manga
import mangadex_py.chapters as chapter
import mangadex_py.download as download
from tqdm import tqdm

def main(url, langWithIndex, quality_mode, Manga_main_dir, thread, manga_name, zip_name) :
    bar = tqdm(desc="Initializing", total=4)
    uuid = manga.get_uuid(url)
    if manga_name == None :
        title, desc, status = manga.get_info(uuid, langWithIndex)
    else :
        title = manga_name.strip()
        _, desc, status = manga.get_info(uuid, langWithIndex)
    tqdm.write(f"{title} :")
    bar.update(2)
    totalchap = chapter.get_total_chap_vol(uuid)
    bar.update(1)
    chap_list, lang_chap = chapter.get_chapter_info_by_lang(uuid, langWithIndex[0], quality_mode)
    bar.update(1)
    if chap_list == None :
        return 1
    tqdm.write(f"found {len(lang_chap)} out of {len(totalchap)} for '{langWithIndex[0]}'")
    bar.close()
    print("starting download :")
    download.main(title, chap_list, desc, status, quality_mode, Manga_main_dir, thread, zip_name)