import os, zipfile, pathlib, shutil, json, sys

current_working_dir = str(pathlib.Path().resolve().absolute())

def remspc(string) :
    #special characters if the user is using windows.
    #windows doesn't like these characters 
    special_characters=[
        "<",
        ">",
        ":",
        "\"",
        "/",
        "\\",
        "|",
        "?",
        "*"]
    for i in string :
        if i in special_characters :
            t = string.replace(i, "")
            return remspc(t)
    return string

def isusingwindows() : 
    if sys.platform.startswith("win32") or sys.platform.startswith("cygwin") :
        return True
    else :
        return False

def chapter_zip_name_var(Manga_title, chapter_folder, Manga_main_dir="Manga") :
    return os.path.join(current_working_dir, Manga_main_dir, Manga_title, os.path.basename(chapter_folder)) + ".zip"

def create_manga_main_dir(Manga_main_dir="Manga") :
    if not os.path.exists(os.path.join(current_working_dir, Manga_main_dir)) :
        os.makedirs(os.path.join(current_working_dir, Manga_main_dir))
    else :
        None

def create_manga_dir(manga_title, Manga_main_dir="Manga") :
    if not os.path.exists(os.path.join(current_working_dir, Manga_main_dir, manga_title)) :
        os.makedirs(os.path.join(current_working_dir, Manga_main_dir, manga_title))
    else :
        None

def create_manga_chap_dir(manga_title, chapter, Manga_main_dir="Manga") :
    if not os.path.exists(os.path.join(current_working_dir, Manga_main_dir, manga_title, chapter)) :
        if not os.path.exists(os.path.join(current_working_dir, Manga_main_dir, manga_title, chapter + ".zip")) :
            os.makedirs(os.path.join(current_working_dir, Manga_main_dir, manga_title, chapter))
    else :
        None
    return str(os.path.join(current_working_dir, Manga_main_dir, manga_title, chapter))

#https://github.com/frozenpandaman/mangadex-dl/blob/3883aa49d52e2c7c3f914f43a6e5fdd3aeebbedf/mangadex-dl.py#L219
def zip_chapter_folder(chapter_folder, Manga_title, Manga_main_dir="Manga") :
    chapter_zip_name = chapter_zip_name_var(Manga_title, chapter_folder, Manga_main_dir)
    print("zipping chapter folder.")
    with zipfile.ZipFile(chapter_zip_name, "w") as f :
        for root, dirs, files in os.walk(chapter_folder) :
            for file in files:
                path = os.path.join(root, file)
                f.write(path, os.path.basename(path))
    shutil.rmtree(chapter_folder)

def get_images_in_zip(chapter_zip_name) :
    with zipfile.ZipFile(chapter_zip_name, 'r') as f :
        zip_content = f.namelist()
        return zip_content

def add_image_zip(chapter_folder, chapter_zip_name) :
    zip_file = zipfile.ZipFile(chapter_zip_name, 'a')
    for root, dirs, files in os.walk(chapter_folder) :
        for file in files :
            path = os.path.join(root, file)
            zip_file.write(path, os.path.basename(path))
    shutil.rmtree(chapter_folder)

def write_series_json(manga_title, description, status, Manga_main_dir="Manga") :
    series_json = os.path.join(current_working_dir, Manga_main_dir, manga_title, "series.json")
    if not os.path.exists(series_json) :
        print("writing json")
        data = {
            "metadata": {
            "name": manga_title,
            "description_formatted": description,
            "status": status
            }
        }
        with open(series_json, "w", encoding='utf-8') as f :
            json.dump(data, f, ensure_ascii=False, indent=4)

def force_create_manga_chap_dir(manga_title, chapter, Manga_main_dir="Manga") :
    chap_dir = os.path.join(current_working_dir, Manga_main_dir, manga_title, chapter)
    if not os.path.exists(chap_dir) :
        os.makedirs(chap_dir)
    return str(chap_dir)

def remove_special_character(string) :
    if isusingwindows() :
        return remspc(string)
    else :
        return string