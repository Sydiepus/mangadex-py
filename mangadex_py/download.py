from mangadex_py.fs import add_image_zip, chapter_zip_name_var, create_manga_chap_dir, create_manga_dir, create_manga_main_dir, force_create_manga_chap_dir, get_images_in_zip, write_series_json, zip_chapter_folder, add_image_zip, force_create_manga_chap_dir
import mangadex_py.download_methods as download_methods
import os, re
from tqdm import tqdm
from mangadex_py.chapters import get_chapter_images
from .naming import naming_main

def new_download(manga_title, chapter_folder, images_list, thread, chapter, Manga_main_dir) :
    if thread == 0 :
        for i in tqdm(images_list, desc=f"Downloading {chapter}") :
            image_name = re.findall(r"\d+", i.split("/")[-1].split("-")[0])[0] + ".jpg"
            full_image_name = os.path.join(chapter_folder, image_name)
            download_methods.normal_download(full_image_name, i)
        zip_chapter_folder(chapter_folder, manga_title, Manga_main_dir)
    else :
        print("using threads.")
        download_methods.multithreaded_download(thread, chapter_folder, images_list)
        zip_chapter_folder(chapter_folder, manga_title, Manga_main_dir)

def dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_list, thread, Manga_main_dir, chapter) :
    if not os.path.exists(chapter_zip_name) :
        new_download(manga_title, chapter_folder, images_list, thread, chapter, Manga_main_dir)
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

def create_img_links(base_url, chapter_hash, img_list, quality) :
    img_link = list()
    if quality == "dataSaver" :
        quality = "data-saver"
    for img in img_list :
        img_link.append(f"{base_url}/{quality}/{chapter_hash}/{img}")
    return img_link

def main(manga_title, chap_list, description, status, quality_mode, Manga_main_dir, thread, zip_name) :
    create_manga_main_dir(Manga_main_dir)
    create_manga_dir(manga_title, Manga_main_dir)
    write_series_json(manga_title, description, status, Manga_main_dir)
    for vol, chap, id, fetched in chap_list : #get the volume, chapter and id. 
        chapter = naming_main(vol, chap, zip_name) # how to name the chapters ?
        chapter_folder = create_manga_chap_dir(manga_title, chapter, Manga_main_dir) #create the manga directory.
        chapter_zip_name = chapter_zip_name_var(manga_title, chapter_folder, Manga_main_dir) # how to name the chapter zip file ?
        if fetched :
            base_url, chap_hash, chap_img = id
        else :
            base_url, chap_hash, chap_img = get_chapter_images(id, quality_mode) #get the necessary stuff for the download, will return None in case of error.
        if chap_hash == None :
            continue
        images_link = create_img_links(base_url, chap_hash, chap_img, quality_mode)
        dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_link, thread, Manga_main_dir, chapter)