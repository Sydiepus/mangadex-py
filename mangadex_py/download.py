from mangadex_py.fs import add_image_zip, chapter_zip_name_var, create_manga_chap_dir, create_manga_dir, create_manga_main_dir, get_images_in_zip, write_series_json, zip_chapter_folder, add_image_zip
import mangadex_py.download_methods as download_methods
import os

def new_download(manga_title, chapter_folder, images_list, thread) :
    if thread == 0 :
        for i in images_list :
            image_name = i.split("/")[-1].split("-")[0] + ".jpg"
            full_image_name = os.path.join(chapter_folder, image_name)
            download_methods.normal_download(full_image_name, i)
        zip_chapter_folder(chapter_folder, manga_title)
    else :
        print("using threads.")
        download_methods.multithreaded_download(thread, chapter_folder, images_list)
        zip_chapter_folder(chapter_folder, manga_title)

def dl_chapter(manga_title, chapter_zip_name, chapter_folder, images_list, thread) :
    if not os.path.exists(chapter_zip_name) :
        new_download(manga_title, chapter_folder, images_list, thread)
    elif len(get_images_in_zip(chapter_zip_name)) < len(images_list) :
        zip_list = get_images_in_zip(chapter_zip_name)
        if  len(zip_list) == 0 :
            for i in images_list :
                image_name = i.split("/")[-1].split("-")[0] + ".jpg"
                full_image_name = os.path.join(chapter_folder, image_name)
                download_methods.zip_fix_download(full_image_name, i, chapter_zip_name)
            add_image_zip(chapter_folder, chapter_zip_name)

        else :
            for i in images_list :
                image_name = i.split("/")[-1].split("-")[0] + ".jpg"
                full_image_name = os.path.join(chapter_folder, image_name)
                if image_name not in zip_list :
                    download_methods.zip_fix_download(full_image_name, i, chapter_zip_name, chapter_folder)
            add_image_zip(chapter_folder, chapter_zip_name)


def main(manga_title, images_links, description, status, Manga_main_dir="Manga", thread=0) :
    create_manga_main_dir(Manga_main_dir)
    create_manga_dir(manga_title)
    write_series_json(manga_title, description, status, Manga_main_dir)
    for i in images_links : #get the tuple that contains the chapter num along with the links for the images
        chapter = f"chapter-{i[0]}"
        chapter_folder = create_manga_chap_dir(manga_title, chapter)
        chapter_zip_name = chapter_zip_name_var(manga_title, chapter_folder)
        dl_chapter(manga_title, chapter_zip_name, chapter_folder, i[-1], thread)