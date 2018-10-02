#This script preprocesses tweet data by removing punctuation, tokenizing, and removing stop words.
# Credit https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

import nltk
import re
import fileinput
from nltk.corpus import stopwords
import string
import csv
from autocorrect import spell


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
emoticons_str,
 r'(?:@[\w_]+)', # @-mentions
 r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
 r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 r"'?\w[\w']*(?:-\w+)*'?", # words with - and '
 r'(?:[\w_]+)', # other words
r'\W*\b\w{1,3}\b', # short words i.e less than 3 letters
 r'(?:\S)' # anything else
]   

stop_words = set(stopwords.words('english')) # remove stop words using the nltk stopwords library
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE) #tokenizing using a regex
punctuation_re = re.compile('[%s]' % re.escape(string.punctuation))


 
def tokenize(s):
    return tokens_re.findall(s)

def rmvpunctuation(s):
    return punctuation_re.sub('', s)


def preprocess(s , lowercase=True):
    string = rmvpunctuation(s)
    tokens = tokenize(string)
    if lowercase:
        tokens = [token.lower() for token in tokens]
        filtered_sentence = [word for word in tokens if not word in stop_words] 
        num_filtered_sentence = [word for word in filtered_sentence if word.isalpha()] #remove number tokens
        return num_filtered_sentence

with open("C:/Users/Idah/Documents/Fall18/TxtMining/tv_datatwo.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(preprocess("".join(row)))




