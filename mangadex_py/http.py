#https://stackoverflow.com/a/35504626
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def get(url) :
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.25,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    request = s.get(url)
    return request