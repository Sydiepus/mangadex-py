from unicodedata import bidirectional
from mangadex_py.fs import add_image_zip, chapter_zip_name_var, create_manga_chap_dir, create_manga_dir, create_manga_main_dir, force_create_manga_chap_dir, get_images_in_zip, write_series_json, zip_chapter_folder, add_image_zip, force_create_manga_chap_dir
import mangadex_py.download_methods as download_methods
import os
from tqdm import tqdm
from mangadex_py.chapters import chapter_fetch, get_chapter_images, get_images_links, scanlation_group_selector, sort_chap_with_multi_scanlation
import re

def new_download(manga_title, chapter_folder, images_list, thread, chapter) :
    if thread == 0 :
        for i in tqdm(images_list, desc=f"Downloading {chapter}") :
            image_name = re.findall(r"\d+", i.split("/")[-1].split("-")[0])[0] + ".jpg"
            full_image_name = os.path.join(chapter_folder, image_name)
            download_methods.normal_download(full_image_name, i)
        zip_chapter_folder(chapter_folder, manga_title)
    else :
        print("using threads.")
        download_methods.multithreaded_download(thread, chapter_folder, images_list)
        zip_chapter_folder(chapter_folder, manga_title)

def dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_list, thread, Manga_main_dir, chapter) :
    if not os.path.exists(chapter_zip_name) :
        new_download(manga_title, chapter_folder, images_list, thread, chapter)
    elif len(get_images_in_zip(chapter_zip_name)) < len(images_list) :
        force_create_manga_chap_dir(manga_title, chapter, Manga_main_dir) #https://stackoverflow.com/a/31414405
        print("Missing images in zip detected fixing it now.")
        zip_list = get_images_in_zip(chapter_zip_name)
        if  len(zip_list) == 0 :
            for i in tqdm(images_list, desc=f"fixing {chapter}.zip") :
                image_name = re.findall(r"\d+", i.split("/")[-1].split("-")[0])[0] + ".jpg"
                full_image_name = os.path.join(chapter_folder, image_name)
                download_methods.zip_fix_download(full_image_name, i, chapter_zip_name)
            add_image_zip(chapter_folder, chapter_zip_name)

        else :
            for i in tqdm(images_list, desc=f"fixing {chapter}.zip") :
                image_name = re.findall(r"\d+", i.split("/")[-1].split("-")[0])[0] + ".jpg"
                full_image_name = os.path.join(chapter_folder, image_name)
                if image_name not in zip_list :
                    download_methods.zip_fix_download(full_image_name, i, chapter_zip_name)
            add_image_zip(chapter_folder, chapter_zip_name)
    else :
        print(f"skipping {os.path.split(chapter_zip_name)[-1]}")


def main(manga_title, chap_list, description, status, quality_mode, base_url, volumes, Manga_main_dir="Manga", thread=0) :
    create_manga_main_dir(Manga_main_dir)
    create_manga_dir(manga_title, Manga_main_dir)
    write_series_json(manga_title, description, status, Manga_main_dir)
    for i in chap_list[0:] : #get the tuple that contains the chapter num along with the chapter hash
        if volumes != [] and len(i) == 3:
            contain_vol = True
            chapter = f"vol-{i[1]}-chapter-{i[0]}"
        else :
            chapter = f"chapter-{i[0]}"
            contain_vol = False
        chapter_folder = create_manga_chap_dir(manga_title, chapter, Manga_main_dir)
        chapter_zip_name = chapter_zip_name_var(manga_title, chapter_folder, Manga_main_dir)
        list_chap = sort_chap_with_multi_scanlation(i, chap_list, contain_vol)
        if len(list_chap) > 1 :
            print(f"{len(list_chap)} scanlation for {chapter} found, selecting the 'best one'.")
            chap_img = scanlation_group_selector(list_chap, quality_mode)
            images_link = get_images_links([chap_img], base_url)
            if images_link == None :
                continue
            dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_link[0][-1], thread, Manga_main_dir, chapter)
        elif len(list_chap) == 1 :
            chap_fetched = chapter_fetch(i[-1])
            chap_img = get_chapter_images(chap_fetched, quality_mode)
            if chap_img == None :
                continue
            images_link = get_images_links(chap_img, base_url)
            if images_link == None :
                continue
            dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_link[0][-1], thread, Manga_main_dir, chapter)
        else :
            continue