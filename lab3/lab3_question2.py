from bs4 import BeautifulSoup as bs
import requests

def getUrls():
    mainUrl = "http://proceedings.mlr.press/v70/"
    website = requests.get(mainUrl)
    soup = bs(website.text, "lxml")
    urls = [link.get('href') for link in soup.find_all('a') if link.contents[0] == "Download PDF"]
    return urls

def downloadFile(url):
	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
	    for chunk in r.iter_content(chunk_size=1024): 
	        if chunk:
	            f.write(chunk)
	return local_filename