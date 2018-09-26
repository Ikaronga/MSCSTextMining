#This script preprocesses tweet data by removing punctuation, tokenizing, and removing stop words.
# Credit https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

import nltk
import re
import fileinput
from nltk.corpus import stopwords
import string
import csv

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
  r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
 r"'?\w[\w']*(?:-\w+)*'?", # words with - and '
 r'(?:[\w_]+)', # other words
 r'(?:\S)' # anything else
]   
stop_words = set(stopwords.words('english')) 

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
punctuation_re = re.compile('[%s]' % re.escape(string.punctuation))

 
def tokenize(s):
    return tokens_re.findall(s)

def rmvpunctuation(s):
    return punctuation_re.sub('', s)

def preprocess(s, lowercase=True):
    string = rmvpunctuation(s)
    tokens = tokenize(string)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        filtered_sentence = [w for w in tokens if not w in stop_words] 
        return filtered_sentence

with open("file.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
     print(preprocess("".join(row)))


