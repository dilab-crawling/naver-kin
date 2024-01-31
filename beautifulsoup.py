import requests
from bs4 import BeautifulSoup
import re
import pickle

dirId_list = list()
new_dirId_list = list()

def get_initial_dir_id(url):
    match = re.search(r'dirId=(\d+)', url)
    return match.group(1) if match else None

def crawl_link(url, base_url, visited_urls, initial_dir_id=None):
    if url in visited_urls:
        return {}
    visited_urls.add(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 최초의 dirId 값을 설정
    if initial_dir_id is None:
        initial_dir_id = get_initial_dir_id(url)

    links_mapping = []
    spot_directory = soup.find('div', class_='spot_directory')
    if spot_directory and not spot_directory.find('div', class_='tag_area'):
        # 하위 링크 수집
        li_tags = spot_directory.find_all('li')
        for li in li_tags:
            a_tag = li.find('a')
            if a_tag and a_tag.has_attr('href'):
                link = base_url + a_tag['href']
                # 재귀적으로 크롤링
                links_mapping.extend(crawl_link(link, base_url, visited_urls, initial_dir_id))
    else:
    
        # 최초 dirId와 매핑
        loc_link = extract_location_links(soup)
        dir_id = get_initial_dir_id(loc_link)
        
        if dir_id:
            dirId_list.append(dir_id)
        if len(dir_id) % 2 == 0:
            num = dir_id[:2]
        else:
            num = dir_id[0]
        print(f"https://kin.naver.com/qna/detail.naver?d1id={num}&dirId={dir_id}&docId={i}")
        new_dirId_list.append(dir_id)
        return [dir_id]

    dirId_list.clear()
      
    return links_mapping

def extract_location_links(soup):
    location_ul = soup.find('ul', class_='location', id='au_location')
    location_links = []
    if location_ul:
        li_class = location_ul.find('li', class_='last')
        if li_class is None:
            li_class = location_ul.find('li', class_='last on')
        return li_class.a['href']
       
    return location_links



# 링크 수집 및 크롤링 시작
base_url = "https://kin.naver.com"
start_url = f"{base_url}/qna/list.naver"
visited_urls = set()
initial_dir_id = get_initial_dir_id(start_url)


i = 463232569
dirId_list = crawl_link(start_url, base_url, visited_urls, initial_dir_id)
with open("dirId_list.pickle", "wb") as f:
    pickle.dump(dirId_list, f)
i -= 1  # 모든 dirId 처리 후 i 값을 감소