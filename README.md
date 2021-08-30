# Mangadex-py
![PyPI](https://img.shields.io/pypi/v/Sydiepus-mangadex-py?color=gree&label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/Sydiepus-mangadex-py?color=gree)
![GitHub issues](https://img.shields.io/github/issues/Sydiepus/mangadex-py)

A manga downloader for [MangaDex.org](https://mangadex.org/), Using the new [API](https://api.mangadex.org/docs.html).

## Inspiration
If these projects weren't available, mangadex-py would be a gallimaufry of python code.  
some snippets were taken from them.  
1. [manga-py](https://github.com/manga-py/manga-py)
2. [mangadex-dl](https://github.com/frozenpandaman/mangadex-dl)
3. [MangaDex.py](https://github.com/Proxymiity/MangaDex.py)
## Requirements
- Python >= 3 should be fine.
## How to use

1. Install the package  
The project had to be named Sydiepus-mangadex-py because 'mangadex-py' was creating conflict with another package.
```
pip3 install Sydiepus-mangadex-py 
# or
pip install Sydiepus-mangadex-py
```
### To upgrade 
```
pip install --upgrade Sydiepus-mangadex-py
# or
pip3 install --upgrade Sydiepus-mangadex-py
```

2. Use program.
``` 
mangadex-py
```
### Downloading Manga
- By default no threads will be used.
- By default the english language will be used.
- By default the images will be download without any compression. 
- By default a 'series.json' will be created inside manga_name folder like [Mylar](https://github.com/mylar3/mylar3/wiki/series.json-examples) to be used by a comic server e.g  : [komga](https://github.com/gotson/komga)
```
mangadex-py mangadexurl -t 4 #download with 4 threads.

mangadex-py mangadexurl -l ru #download russian manga translation.

mangadex-py mangadexurl -ds data-save #download compressed images.

mangadex-py mangadexurl -d Books #will download to pwd/Books/manganame/

mangadex-py mangadexurl --name 'Manga Name' #change manga directory name

mangadex-py -F Manga.txt #will use pwd/Manga.txt as source of mangadexurl and manga name
```
## -F / --File option
The file should be in the following format :  
``` 
url1, manga name
url2
url3, manga name
```
Example :
```
https://mangadex.org/title/32712fc7-466c-4f59-a481-9c608d374c66
https://mangadex.org/title/e78a489b-6632-4d61-b00b-5206f5b8b22b, reincarnated as a slime
```
## Help
```
mangadex-py -h 
# or
mangadex-py --help
```
## Notice
**This is the first release of the program bugs are to be expected.**
## TODO
- ~~Complete the File support for bulk downloading.~~ [Done]
- Add threaded download for zip fix.
- ~~Try to make the chapter_fetch more efficient.~~ [Done]
- ~~Add a progress bar.~~ [Done]
- ~~Add option to use a custom manga name for folder.~~ [Done]
