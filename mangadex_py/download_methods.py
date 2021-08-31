import os
import mangadex_py.http as http
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
#import mangadex_py.report_health as report

def normal_download(path, link) :
    if not os.path.exists(path) :
        req = http.get(link)
        # try : #https://github.com/Proxymiity/MangaDex.py/blob/4445efe131db8fb38c7eda8b76548f93bc74c241/MangaDexPy/downloader.py#L31
        #     cached = True if req.headers["x-cache"] == "HIT" else False
        # except KeyError :  # No cache header returned: the client is at fault
        #     cached = False
        if req.status_code == 200 :
            # success = True
            with open(path, 'wb') as f :
                f.write(req.content)
                f.close()
            time.sleep(0.25) #5 requests per second = 1 request per 0.2 seconds i suppose.
            #report.report(link, success, cached, len(req.content), int(req.elapsed.microseconds/1000))
        #else :
            #success = False
            #report.report(link, success, cached, len(req.content), int(req.elapsed.microseconds/1000))

def multithreaded_download(thread, chapter_folder, images_list):
    print("progress bar for threaded download broken.")
    threads = []
    if thread <= 4 :
        with ThreadPoolExecutor(max_workers=thread) as executor:
            for i in tqdm(images_list) :
                image_name =  i.split("/")[-1].split("-")[0].split("x")[-1] + ".jpg"
                full_image_name = os.path.join(chapter_folder, image_name)
                threads.append(executor.submit(normal_download, full_image_name, i))
    else :
        print("please use less than 5 threads (4 and less) to stay within the rate limit.")

def zip_fix_download(path, link, chapter_zip_name) :
    if not os.path.exists(path) :
        req = http.get(link)
        if req.status_code == 200 :
            with open(path, 'wb') as f :
                f.write(req.content)
            time.sleep(0.25)