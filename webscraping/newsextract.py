import requests
import re
import feedparser
from bs4 import BeautifulSoup
import numpy as np
import os
def getSTEMlink(source):
    #input: int source 
    #output: array of article links depending on specifed 'source'
    #   possible sources:
    #   0 - new york times, tech based
    #   1 - science daily, science based //error -403: Forbidden (the access to the website was denied)
    #   2 - the guardian, tech based //error
    #   3 - the guardian, sience based
    #   4 - dailymail, science and tech based
    #   5 - the verge, tech based
    #   6 - the verge, science based
    #   7 - momgineer //error
    #   8 - scientix //error
    #   9 - thestemlaboratory //error
    #   10 - themakermom //error
    #   11 - definedstem //error
    #   12 - yahoo, science based
    #   13 - bbc, tech based //error
    #   14 - bbc, science and environment based //error
    #   15 - futurumcareers, youth based 


    sources = [
            ['https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml','technology'],
            ['https://www.sciencedaily.com/rss/top/science.xml',''],
            ['https://www.theguardian.com/uk/technology/rss','technology'],
            ['https://www.theguardian.com/science/rss','science'],
            ['https://www.dailymail.co.uk/sciencetech/index.rss','sciencetech'],
            ['https://www.theverge.com/tech/rss/index.xml ',''],
            ['https://www.theverge.com/science/rss/index.xml',''],
            ['http://feeds.feedburner.com/Momgineer',''],
            ['http://blog.scientix.eu/feed/',''],
            ['https://thestemlaboratory.com/feed/',''],
            ['http://feeds.feedburner.com/themakermom/tmdu',''],
            ['https://www.definedstem.com/feed/',''],
            ['https://news.yahoo.com/rss/science/',''],
            ['http://feeds.bbci.co.uk/news/video_and_audio/technology/rss.xml','technology'],
            ['http://feeds.bbci.co.uk/news/video_and_audio/science_and_environment/rss.xml',''],
            ['https://futurumcareers.com/feed','']
            ]

    #News sources for younger audiences: https://blog.feedspot.com/stem_rss_feeds/
    currentSource = sources[source]
    linkarray = []
    d = feedparser.parse(currentSource[0])

    for post in d.entries:
        if re.search(currentSource[1],post.link,re.I):
            linkarray.append(post.link)

    return linkarray

def parseArticles(linkarray,fiveArticles):
    #input: String[] linkarray -array containing links to articles
    #       bool fiveArtilces - True: processes first 5 links, False: processes all links in linkarray
    #purpose: creates text files of all articles specified by links

    if fiveArticles:
        numofArticles = 2
    else:
        numofArticles = len(linkarray)
    # Reading the content (it is divided in paragraphs)
    for link in range(numofArticles):
        article = requests.get(linkarray[link])
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')
        x = soup_article.find_all('p')

        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        with open(str(link)+".txt",'w') as the_file:
            the_file.write(final_article)

        return final_article


def parseArticle(link):
    
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    x = soup_article.find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        print(paragraph)
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    with open("article.txt",'w') as the_file:
        the_file.write(final_article)
        
def rmTXTfiles():
    #removes all .txt files in the current directory
    mydir = os.getcwd()
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))


    

#1,2

if __name__ == '__main__':
    rmTXTfiles()
    linkarray = getSTEMlink(15)
    print(linkarray)
    parseArticles(linkarray,True)
    #parseArticle('http://feedproxy.google.com/~r/Momgineer/~3/nAFLUexwmzE/bingo-games-in-math-classroom.html')