import sys
from importlib import reload
reload(sys)


import newspaper
from newspaper import Article
import csv, os
from bs4 import BeautifulSoup
import urllib.request


with open("keywords.txt") as f:
    req_keywords = f.readlines()

req_keywords = [x.strip().lower() for x in req_keywords] 

newspaper_base_url = 'https://www.indiatoday.in'
category = 'world'


def checkif_kw_exist(list_one, list_two):
    common_kw = set(list_one) & set(list_two)
    if len(common_kw) == 0: return False, common_kw
    else: return True, common_kw

def get_article_info(url):
    a = Article(url)
    a.download()
    a.parse()
    a.nlp()
    success, checked_kws = checkif_kw_exist(req_keywords, a.text.split())
    if success:
        return [url, a.publish_date, a.title, a.text,a.summary,a.keywords]
    else: return False


output_file = "./output.csv"
if not os.path.exists(output_file):
    open(output_file, 'w').close() 
    
for index in range(1,3700,1):
    print ('--------------------')
    print ('checking page: {id}'.format(id=index))
    print ('--------------------')
    page_url = newspaper_base_url + '/' + category + '?page='+str(index)
    features="lxml"
    page_soup = BeautifulSoup( urllib.request.urlopen(page_url).read())

    primary_tag = page_soup.find_all("h2", attrs={"class": ""})

    for tag in primary_tag:
        url = tag.find("a")
        print (url)
        url = newspaper_base_url + url.get('href')

        result = get_article_info(url)
        if result is not False:
            with open(output_file, 'a') as f:
                writeFile = csv.writer(f)
                writeFile.writerow(result)
                f.close
        else: pass