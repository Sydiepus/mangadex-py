import mangadex_py.manga as manga
import mangadex_py.chapters as chapter
import mangadex_py.download as download
from tqdm import tqdm

def main(url, langWithIndex, quality_mode, Manga_main_dir, thread, manga_name, zip_name, sel_chap):
    bar = tqdm(desc="Initializing", total=4)
    uuid = manga.get_uuid(url)
    if manga_name == None:
        title, desc, status, trans_lang = manga.get_info(uuid, langWithIndex)
    else:
        title = manga_name.strip()
        _, desc, status, trans_lang = manga.get_info(uuid, langWithIndex)
    if not manga.check_trans(trans_lang, langWithIndex[0]):
        tqdm.write(f"No translated chapters found for {'en' if langWithIndex[0] == None else langWithIndex[0]}")
        bar.close()
        return 1
    tqdm.write(f"{title} :")
    bar.update(2)
    total_chap_list, total_vol_list = chapter.get_chapters(uuid)
    total_chap_lang_list, total_vol_lang_list, lang_response, gen_chap = chapter.get_chapters_by_lang(uuid, langWithIndex[0], sel_chap)
    bar.update(1)
    if not gen_chap :
        to_down = None
        tqdm.write(f"found {len(total_chap_lang_list)}/{len(total_chap_list)} chapters and {len(total_vol_lang_list)}/{len(total_vol_list)} volumes for {'en' if langWithIndex[0] == None else langWithIndex[0]}")
    else :
        to_down = sorted(list(set(total_chap_lang_list).intersection(gen_chap)))
        if len(to_down) == 0 :
            tqdm.write("specified chapter(s) do not exist(s)")
            bar.close()
            return 1
        tqdm.write(f"found {len(to_down)}/{len(gen_chap)} chapters for {'en' if langWithIndex[0] == None else langWithIndex[0]}")
    down_chap_list = chapter.prep_chap_down(lang_response, total_vol_lang_list, total_chap_lang_list, to_down)
    bar.update(1)
    bar.close()
    print("starting download :")
    download.main(title, down_chap_list, desc, status, quality_mode, Manga_main_dir, thread, zip_name)