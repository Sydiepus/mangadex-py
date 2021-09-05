from .main import main

def file_main(file, langWithIndex, quality_mode, Manga_main_dir, thread, zip_name=None) :
    f = open(file, 'r')
    lines = f.readlines()
    for i in lines :
        url_name = i.split(",")
        if len(url_name) > 1 :
            main(url_name[0], langWithIndex, quality_mode, Manga_main_dir, thread, url_name[1], zip_name)
        else :
            main(url_name[0], langWithIndex, quality_mode, Manga_main_dir, thread, zip_name=zip_name)