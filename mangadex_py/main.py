import mangadex_py.manga as manga
import mangadex_py.chapters as chapter
import mangadex_py.download as download

def main(url, langWithIndex, quality_mode, Manga_main_dir, thread) :
    print("getting uuid.")
    uuid = manga.get_uuid(url)
    print("fetching manga info 'Title' 'description' 'status' based on your language setting.")
    title, desc, status = manga.get_info(uuid, langWithIndex)
    print("fetching chapters info 'available languages' 'available volumes if any' 'available chapters' 'total chapters (language independent)'.")
    language, volumes, chapters, totalchap = chapter.get_manga_chapters_info(uuid)
    print("fetching 'chapter list by language' 'total chapters by language.'")
    chap_list, lang_chap = chapter.get_chapter_info_by_lang(uuid, totalchap, langWithIndex[0])
    print(f"found {len(lang_chap)} out of {totalchap} for {langWithIndex[0]}")
    print("fetching available images for every chapter. (it'll take sometime base on the manga and your internet connection)")
    chap_fetch = chapter.chapters_fetch(chap_list)
    print("getting a server url to download the images from.")
    base_url = chapter.base_url_fetch(chap_list)
    print("filtering chapters images base on quality")
    chapters_images = chapter.get_chapters_images(chap_fetch, quality_mode)
    print("generating images links")
    images_link = chapter.get_images_links(chapters_images, base_url)
    print("starting download")
    download.main(title, images_link, desc, status, Manga_main_dir, thread)