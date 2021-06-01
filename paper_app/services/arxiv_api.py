import requests
from bs4 import BeautifulSoup
from scirate.client import ScirateClient
from scirate.paper import SciratePaper
from datetime import datetime
from time import sleep
# import random 

base_url = 'http://export.arxiv.org/api/query?search_query='
gs_base_url = 'https://scholar.google.com/scholar?hl=en&q=arxiv:'

key_map = {
    'title':'ti',
    'author':'au',
    'abstract':'abs',
    'category':'cat',
    'all':'all',
    'link_end':'id'
    }

def get_paper(keyword,key,value,start_date=None,end_date=None):
    if start_date is None or end_date is None:
        end_url = f"{key_map[key]}:{value}&start=0&max_results=1000"
    else:
        end_url = f"{key_map[key]}:{value}+AND+submittedDate:[{start_date}+TO+{end_date}]&start=0&max_results=1000"
    response = requests.get(base_url+end_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paper_list = soup.select('entry')
    paper_dict_list = []
    for paper in paper_list:
        paper_dict = {}
        paper_dict['link_end'] = paper.find('id').text.split('abs/')[1].split('v')[0]
        paper_dict['title'] = paper.find('title').text
        paper_dict['abstract'] = paper.find('summary').text
        paper_dict['published_date'] = datetime.strptime(paper.find('published').text, "%Y-%m-%dT%H:%M:%SZ").date()
        paper_dict['scites'] = get_scites(paper_dict['link_end'])
        paper_dict['category'] = paper.find('category').attrs['term']
        paper_dict['author_list'] = [author.find('name').text for author in paper.select('author')]
        paper_dict['keyword'] = keyword
        paper_dict_list.append(paper_dict)
    sleep(3)
    return paper_dict_list

def get_scites(link_end):
    client = ScirateClient()
    paper_data = client.paper(link_end)
    scites = paper_data.scites if paper_data.scites is not None else 0
    sleep(2)
    return scites