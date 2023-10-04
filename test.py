import requests
from boilerpy3 import extractors


def getDataFromNews(url):
    y = requests.get(url)
    extractor = extractors.ArticleExtractor()
    content = extractor.get_content((y.content).decode('utf-8'))
    return content