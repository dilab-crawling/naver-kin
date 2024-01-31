import pickle
import os
import requests
from bs4 import BeautifulSoup as bs

with open("dirId_list.pickle", "rb") as f:
    dirId_list = pickle.load(f)

os.mkdir('data', dir_fd=True)

if os.listdir('data')!=0:
    last_docId = os.listdir('data')[-1]
else:
    last_docId = 463372378

def get_url(dirId, docId):
    if len(dirId) % 2 == 0:
        num = dirId[:2]
    else:
        num = dirId[0]
    return f"https://kin.naver.com/qna/detail.naver?d1id={num}&dirId={dirId}&docId={i}"

for docId in range(last_docId, 0):
    for dirId in dirId_list:
        url = get_url(dirId, docId)
        try:
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            if soup.head.meta['name']=="decorator":
                pass
            else:
                with open(f"saved_page_{dirId}_{docId}.html", "w", encoding="utf-8") as file:
                    file.write(response.text)
        except:
            pass