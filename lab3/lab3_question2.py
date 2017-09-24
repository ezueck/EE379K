!pip install git+https://github.com/timClicks/slate.git
!pip install Downloads/pyenchant*

from bs4 import BeautifulSoup as bs
import requests
import slate
import re
import enchant
import os.path
from collections import Counter
import pandas as pd
import math
import random

def getUrls():
    mainUrl = "http://proceedings.mlr.press/v70/"
    website = requests.get(mainUrl)
    soup = bs(website.text, "lxml")
    urls = [link.get('href') for link in soup.find_all('a') if link.contents[0] == "Download PDF"]
    return urls

def downloadFile(url):
    r = requests.get(url, stream=True)
    local_filename = url.split('/')[-1]
    if os.path.isfile(local_filename):
        return local_filename
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    return local_filename

def getPdfText(pdf):
    with open(pdf) as f:
        text_pages = slate.PDF(f);
        return text_pages

def getListOfWords(text):
    d = enchant.Dict("en_US")
    regex = r'\w+'
    list1=re.findall(regex,text)
    listfixed = [word for word in list1 if len(word)<20 and len(word)>3]
    return [word for word in listfixed if d.check(word)]

def getAllWords():
    urls = getUrls();
    words = []
    for url in urls :
        file_pdf = downloadFile(url)
        print file_pdf
        pdf = getPdfText(file_pdf)
        for t in pdf:
            pdf_words = getListOfWords(t)
            words.append(pdf_words)
    return words

# Part 1 (saving to csv to avoid parsing if my computer crashes)

words = [x.lower() for x in getAllWords()]
counts = Counter(allWords)
counts.most_common(10)
df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
df = df.rename(columns={'index':'word', 0:'count'})
df = df.sort_values(['count'], ascending=False)
df.to_csv("wordcount.csv")

# Part 2 

def calculateProbability(row):
    count_sum = df['count'].sum()
    return row['count']/count_sum

entropy = 0
for x in df['probability']:
    entropy += -(x * math.log(x, 2))

# Part 3 

countList = df['count'].tolist()
wordList = df['word'].tolist()
lotteryList = [countList[0]-1]
for i in range(1, len(countList)):
    lotteryList.append(lotteryList[i-1]+countList[i])

def getRandomWord():
    tick = random.randrange(0, sum(countList))
    for i in range(0, len(lotteryList)):
        if(tick <= lotteryList[i]):
            return wordList[i]

paragraph = ""
for i in range(0, 100):
    paragraph += getRandomWord() + " "
paragraph
