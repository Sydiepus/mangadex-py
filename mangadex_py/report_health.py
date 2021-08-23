import requests, json

from requests.sessions import session

report_api = "https://api.mangadex.network/report"

#need revision.
#reporting not working.
#basurl is invalid according to the api.
#https://reqbin.com/woeukxik

def report(url, success, cached, bytes, duration) :
    session = requests.session()
    headers = {"Content-Type": "application/json"}
    data = {"url": url, "success": success, "cached": cached, "bytes": bytes, "duration": duration}
    req = session.post(report_api, headers=headers, data=json.dumps(data))
    if req.status_code == 200 :
        print("reporting successful")
    else :
        print(req.status_code)
        print(req.content)
        print("failed to report. Maybe the api is down ?")