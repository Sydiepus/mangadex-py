# Mangadex-py
A manga downloader for [MangaDex.org](https://mangadex.org/), Using the new [API](https://api.mangadex.org/docs.html).

## inspiration
if these projects weren't available, mangadex-py would be a gallimaufry of python code.  
some snippets were taken from them.  
1. [manga-py](https://github.com/manga-py/manga-py)
2. [mangadex-dl](https://github.com/frozenpandaman/mangadex-dl)
3. [MangaDex.py](https://github.com/Proxymiity/MangaDex.py)
## Requirements
- Python >= 3 should be fine.
## How to use

1. Download the repository.
```
git clone https://github.com/Sydiepus/mangadex-py
```

2. Use program.
``` 
cd mangadex-py
python mangadex-py.py mangadexurl
```
### Downloading Manga
- By default no threads will be used.
- By default the english language will be used.
- By default the images will be download without any compression. 
- By default a 'series.json' will created inside  manga_name folder like [Mylar](https://github.com/mylar3/mylar3/wiki/series.json-examples) to be used by comic server e.g  : [komga](https://github.com/gotson/komga)
```
python mangadex-py.py mangadexurl -t 4 #download with 4 threads.

python mangadex-py.py mangadexurl -l ru #download russian manga translation.

python mangadex-py.py mangadexurl -ds data-save #download compressed images.

python mangadex-py.py mangadexurl -d Books #will download to pwd/Books/manganame/
```
## Help
```
python mangadex-py.py -h 
# or
python mangadex-py.py --help
```
## Notice
this is the first release of the program bugs are to be expected.
## TODO
- complete the File support for bulk downloading.
- add threaded download for zip fix.
- try to make the chapter_fetch more efficient.
- add a progress bar.
- add option to use a custom manga name for folder. 
- publish project as a python package.
