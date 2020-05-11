import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#word_tokenize accepts a string as an input, not a file. 

grade = 8

current_path = os.path.dirname(__file__)
file_path = os.path.join(current_path, "article.txt")

stop_words = set(stopwords.words('english'))

voc_list = []

file = open(file_path, "r")
for line in file:
    words = line.split()
    for word in words:
        word = word.lower()
        hasDigit = bool(re.search(r'\d', word))
        if hasDigit == False:
            if word.find("'") == -1:
                word = re.sub(r'[^\w\s]','',word)
                if not word in stop_words:
                    if not word in voc_list:
                        voc_list.append(word)

file = open("voc_list_g{}.txt".format(grade),'w')
file.write("{}".format(voc_list))
file.close()