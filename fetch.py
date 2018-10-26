import cPickle as pickle

with open('classify.pkl', 'rb') as fp:
    content = pickle.load(fp)
    model, vect = content[0], content[1]

from newsapi import NewsApiClient

api_keys = ['4b4233b0e7c243ea8bdd9abf5a19bbbd',
            'cb4e308246624d8188e9f254d721c345', '74b2cc200dcb4591b486369116c1cc41']
next_key_index = 0
newsapi = NewsApiClient(api_key=api_keys[next_key_index])
sources = 'the-hindu'  # bbc-news,fox-news,the-times-of-india,cnn,espn'

from preprocess import clean_text
from json import dumps
from crawler import crawl
from store import insert
from time import sleep


def fetch(page):
    result = newsapi.get_everything(sources=sources, language='en', page=page)
    articles = result['articles']
    for article in articles:
        if (not article['title']) or (not article['description']):
            continue
        values = [article['source']['name'], article['author'],
                  dumps(article['title']), dumps(article['description']),
                  article['url'], article['urlToImage'], article['publishedAt']]
        text = clean_text(crawl(values[4], article['source']['id']))
        category = model.predict(vect.transform([text]))[0]
        insert(values, category)
        print(category)
        print('='*len(category))
        print(text)
        print('')


form, limit = 1, 2
while(True):
    for page in range(form, limit):
        fetch(page)
    break
    # sleep(1500)
