from bs4 import BeautifulSoup # web scraping
import numpy as np # web scraping
import requests # web scraping and acessing online websites
import csv # acessing excel sheets
import re # article cleaning
import random # MC generating
from nltk.corpus import stopwords #filter1 stop words
from nltk.tokenize import word_tokenize #filter1 stop words

def getArticle(link):
    # input: String link - ex. 'https://www.sciencenewsforstudents.org/article/ai-can-learn-real-world-skills-playing-video-games'
    # Output: String final_article - the whole article in a string
    # function: the program takes all <p> tags from the website and puts them in a string
    #           you may get random sentences, but furthur filters handle those

    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    x = soup_article.find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)

    final_article = " ".join(list_paragraphs)
    return final_article


def parseDictionary2(word): #1% error rate + fast
    # input: String word - the keyword you want sentences for
    # output: String[] - sentences containg the keyword
    # function: grabs the first couple (5-10) sentences containg our wordfrom sentencedict.com

    link = "https://sentencedict.com/" + word + ".html"
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    # an array of sentences with our keyword
    sentences = []

    for foo in soup_article.find_all('div', attrs={'id': 'all'}):
        foo_descendants = foo.descendants
        for d in foo_descendants:
            if d.name == 'div':
                if d.get('id', '') == 'ad_marginbottom_0':
                    return sentences
                else:
                    # when retrieving data from parsedictionary2 (https://sentencedict.com/)
                    # the sentences contain an unwanted number at the start.
                    sentence = d.text
                    sentence = re.sub("[0-9][.,]? ","",sentence)
                    sentence = re.sub("[\(]?[0-9]\) ","",sentence)
                    sentences.append(sentence)

    return sentences

def sentenceCheck(sentList):
    # input: String[] sentList - list of sentences containg our keyword
    # output: String[] sList - list of sentences containg our keyword
    # function: filters out all sentences that do not contain a . ! ?
    sList = []
    for i in range(len(sentList)):
        if (re.search("\.",sentList[i]) or re.search("!",sentList[i]) or re.search("\?",sentList[i])):
            sList.append(sentList[i])
    return sList

def exactWordCheck(sentList,word):
    # input: String[] sentList - list of sentences containg our keyword
    # output: String[] sList - list of sentences containg our keyword
    # function: filters out all sentences that do not match our keyword exactly (no tenses)
    sList = []
    for i in range(len(sentList)):
        if(re.search(' ' + word+ ' ',sentList[i])):
            sList.append(sentList[i])
    return sList

def generateQuestions2(word):
    # input: String word: the keyword that you're generating MC question for
    # output: String sentenceString: MC question in the form "A. this is a ____ B. this is also a ____"
    # function: calls parseDictionary2 to grab an array of sentences from sentencedict.com
    #           calls sentenceCheck to grab only full sentences
    #           calls exactWordCheck to grab sentences with word in the same tense as our key word

    SentenceArr = parseDictionary2(word)
    Real_SentenceArr = sentenceCheck(SentenceArr)
    WithWord_SentenceArr = exactWordCheck(Real_SentenceArr, word)
    try:
        # it would be nice if we have exact sentence match and full sentence
        sentenceString = "A. " + WithWord_SentenceArr[0] + " B. " + WithWord_SentenceArr[1]
    except Exception: 
        # there are no sentences with the same tense as word
        sentenceString = "A. " + Real_SentenceArr[0] + " B. " + Real_SentenceArr[1]

    sentenceString = re.sub(word, "____", sentenceString)

    return sentenceString

def filter1StopWord(article):
    # input: String article - the whole article in a string
    # output: String[] - all the key words in a string array
    # function: filters out all the stop words ('the','and','to' etc.)

    stop_words = set(stopwords.words('english'))
    voc_list = []
    words = article.split()
    for word in words:
        word = word.lower()
        hasDigit = bool(re.search(r'\d', word))
        if hasDigit == False:
            if word.find("'") == -1:
                word = re.sub(r'[^\w\s]','',word)
                if not word in stop_words:
                    if not word in voc_list:
                        voc_list.append(word)

    return voc_list

def filter2CommonWord(article):
    # input: String[] - all the key words in a string array
    # output: String[] - all the hard words in a string array
    # function: grabs the 10k most common words and stores the words not in that set in a string array
    
    english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
    # Get the file of 10 k most common words from TXT file in a github repo
    response = requests.get(english_most_common_10k)
    data = response.text
    set_of_common_words = {x for x in data.split('\n')}
    hard_words = []
    for word in article:
        if not(word in set_of_common_words):
            hard_words.append(word)
    return hard_words

if __name__ == "__main__":

    articleLink = 'https://www.sciencenewsforstudents.org/article/ai-can-learn-real-world-skills-playing-video-games'
    my_article = getArticle(articleLink)
    vocabList = filter1StopWord(my_article)
    hardwordList = filter2CommonWord(vocabList)

    #generating the MC questions and putting them into a csv file
    MCList = [] # a random 3 words + answer word scrambled together
    with open('out.csv', 'w', newline='') as out_file:
        out_writer = csv.writer(out_file)
        # formatting
        out_writer.writerow(['Multiple Choice Questions for: ' + articleLink])
        out_writer.writerow([''])
        out_writer.writerow(['Word','','Question type','Points','Question Text','Answer 1','Answer 2','Answer 3','Answer 4'])
        # generating MC questions for each word in hardwordList
        for word in hardwordList:
            # generate MC answers
            # grab random choices from the stop word filtered list NOT common word filtered list
            MCList = random.sample(range(1,len(vocabList)),3)
            for i in range(3):
                MCList[i] = vocabList[MCList[i]]
            MCList.append('*'+word)
            # shuffle our MC list
            random.shuffle(MCList)

            # generate MC question
            try:
                questionText = generateQuestions2(word)
            except Exception:
                # the word is probally the name of a person and cannot be found at sentencedict.com
                print(word + " was not found at sentencedict.com")
                continue
            
            # enter MC question and answer into our csv file
            try:
                out_writer.writerow([word,'','MC','5',questionText] + MCList)
            except UnicodeEncodeError:
                # there maybe an error parsing unique characters from the sentence list
                out_writer.writerow([word,'','MC','5',"ERROR: unicode error"] + MCList)


