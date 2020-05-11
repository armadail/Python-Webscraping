from bs4 import BeautifulSoup
import numpy as np
import requests
import csv
import re
import random 
def parseDictionary(word): #10% error + really slow
    link = "https://dictionary.cambridge.org/dictionary/english/" + word
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')

    list_paragraphs = []
    #getting text under the b1 tab
    x = soup_article.find_all("span",{"class":"eg deg"}) 
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
    #getting text under the 'More examples' tab
    x = soup_article.find_all("li",{"class":"eg dexamp hax"})
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)

    return list_paragraphs
 
def parseDictionary2(word): #1% error rate + fast
    link = "https://sentencedict.com/" + word + ".html"
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')

    list_paragraphs = []
    # for foo in soup_article.find_all('div', attrs={'id': 'all'}):
    #     bar = foo.find('div')
    #     print(bar.text)
    for foo in soup_article.find_all('div', attrs={'id': 'all'}):
        foo_descendants = foo.descendants
        for d in foo_descendants:
            if d.name == 'div':
                if d.get('id', '') == 'ad_marginbottom_0':
                    return list_paragraphs
                else:
                    # when retrieving data from parsedictionary2 (https://sentencedict.com/)
                    # the sentences contain an unwanted number at the start.
                    sentence = d.text
                    sentence = re.sub("[0-9][.,]? ","",sentence)
                    sentence = re.sub("[\(]?[0-9]\) ","",sentence)
                    list_paragraphs.append(sentence)

    return list_paragraphs

def parseDictionary3(word): #really slow
    link = "https://www.wordhippo.com/what-is/sentences-with-the-word/" + word + ".html"
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    #class="exv2row1" ,
    list_paragraphs = []
    x = soup_article.find_all("tr",{"class":"exv2row1"}, limit=4) 
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        # removing the '\n' stuff
        paragraph = re.sub("\\n" , "",paragraph)
        list_paragraphs.append(paragraph)

    return list_paragraphs

def sentenceCheck(sentList):
    sList = []
    for i in range(len(sentList)):
        if (re.search("\.",sentList[i]) or re.search("!",sentList[i]) or re.search("\?",sentList[i])):
            sList.append(sentList[i])
    return sList

def exactWordCheck(sentList,word):
    sList = []
    for i in range(len(sentList)):
        if(re.search(' ' + word+ ' ',sentList[i])):
            sList.append(sentList[i])
    return sList

# def numberclean(sentList):
#     sentenceString = re.sub()
#     return sentenceString


def generateQuestions2(word):
    SentenceArr = parseDictionary2(word)
    Real_SentenceArr = sentenceCheck(SentenceArr)
    WithWord_SentenceArr = exactWordCheck(Real_SentenceArr, word)
    try:
        sentenceString = "A. " + WithWord_SentenceArr[0] + " B. " + WithWord_SentenceArr[1]
    except Exception: #there are no sentences with the same tense as word
        sentenceString = "A. " + Real_SentenceArr[0] + " B. " + Real_SentenceArr[1]

    sentenceString = re.sub(word, "____", sentenceString)

    return sentenceString

def generateQuestions3(word):
    SentenceArr = parseDictionary3(word)
    Real_SentenceArr = sentenceCheck(SentenceArr)
    WithWord_SentenceArr = exactWordCheck(Real_SentenceArr, word)
    try:
        sentenceString = "A. " + WithWord_SentenceArr[0] + " B. " + WithWord_SentenceArr[1]
    except Exception: #there are no sentences with the same tense as word
        sentenceString = "A. " + Real_SentenceArr[0] + " B. " + Real_SentenceArr[1]

    sentenceString = re.sub(word, "____", sentenceString)

    return sentenceString

# if __name__ == '__main__':
#     word = "planetesimal"
#     a = parseDictionary3(word)
#     print("done")

if __name__ == '__main__':
    rowcounter = 1
    vocabList = [] # our vocabulary list taken from the first column of our input file
    MCList = [] # a random 3 words + answer word scrambled together
    questions = 'A. I just complete the piano____.        B. The boy has learned a hard ____ that he will not forget. '
    with open('input2.csv') as in_file:
        in_reader = csv.reader(in_file, delimiter=',')
        # first get your vocabulary array
        for row in in_reader:
            try:
                vocabList.append(row[0])
            except IndexError:
                vocabList.append('')
        # remove the first three elemnt in our vocab list (this is just formating stuff)
        vocabList.pop(0) 
        vocabList.pop(0)
        vocabList.pop(0)

    with open('out.csv', 'w', newline='') as out_file:
        out_writer = csv.writer(out_file)
        with open('input2.csv') as in_file:
            in_reader = csv.reader(in_file, delimiter=',')

            for row in in_reader:

                if rowcounter < 4:
                    out_writer.writerow(row)
                else:
                    # generate our MC list
                    MCList = random.sample(range(1,len(vocabList)),3)
                    for i in range(3):
                        MCList[i] = vocabList[MCList[i]]
                    MCList.append('*'+row[0])
                    # shuffle our MC list
                    random.shuffle(MCList)
                    # generate our questions, tries out 2 mirrors before giving up
                    try:
                        questions = generateQuestions2(row[0])
                    except Exception:
                        continue
                        # try:
                        #     questions = generateQuestions3(row[0])
                        # except Exception:
                        #     questions = "ERROR: no sentences found at " + row[0]
                    try:
                        out_writer.writerow([row[0],row[1],row[2],row[3],'','MC','5',questions] + MCList)
                        #out_writer.writerow([row[0],'','MC','5',questions] + MCList)
                    except UnicodeEncodeError:
                        out_writer.writerow([row[0],row[1],row[2],row[3],'','MC','5',"ERROR: unicode error"] + MCList)

                rowcounter += 1
                print("processed " + str(rowcounter) + " out of " + str(len(vocabList)+3))

