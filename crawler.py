import urllib2
from scrapy import Selector

extract_data = {
    'the-hindu': 'div.article p::text',
}


def crawl(url, source=None):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    sel = Selector(text=page)
    content = sel.css(extract_data[source]).extract()
    return ' '.join(line for line in content)
