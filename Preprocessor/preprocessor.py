#This script preprocesses tweet data by removing punctuation, tokenizing, and removing stop words.
# Credit https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

import nltk
import re
import fileinput
from nltk.corpus import stopwords
import string
import csv
import pandas as pd


emoticons_str = r""" 
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )""" #remove emoticons
 
regex_str = [
emoticons_str,
 r'(?:@[\w_]+)', # @-mentions
 r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
 r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 r"'?\w[\w']*(?:-\w+)*'?", # words with - and '
 r'(?:[\w_]+)', # other words
r'\W*\b\w{1,3}\b', # short words i.e less than 3 letters
 r'(?:\S)' # anything else
]   #regular expressions to use for tokenization

nltk_stop_words = set(stopwords.words('english')) # stop words from the nltk stopwords library
cust_stop_words = open("C:/Users/Idah/Documents/Fall18/TxtMining/custom_stopwords.txt", "r").read().split() 
stop_words = nltk_stop_words.union(cust_stop_words) #combine custom stop words list with the nltk list

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE) #tokenizing using a regex
punctuation_re = re.compile('[%s]' % re.escape(string.punctuation))
thewords = []
 
def tokenize(s):
    return tokens_re.findall(s)

def rmvpunctuation(s):
    return punctuation_re.sub('', s)

def preprocess(corpus , lowercase=True):
    corpus_ = rmvpunctuation(corpus)
    tokens = tokenize(corpus_)
    if lowercase:
        tokens = [token.lower() for token in tokens] # to lower case
        stopw_filtered_tokens = [word for word in tokens if not word in stop_words] 
        num_filtered_tokens = [word for word in stopw_filtered_tokens if word.isalpha()] #remove number tokens
        url_filtered_tokens = [re.sub(r"http\S+", "", word) for word in num_filtered_tokens] #remove url tokens
        return filter(None, url_filtered_tokens) #filter function removes empty strings

with open("C:/Users/Idah/Documents/Fall18/TxtMining/ToPreprocess/KaepernickAug17toMar18.csv") as f: #if getting invalid start byte error use encoding='utf-8'
    reader = csv.reader(f)
    for row in reader:
        thewords += preprocess("".join(row))
            
pd.DataFrame(thewords).to_csv("C:/Users/Idah/Documents/Fall18/TxtMining/Kaepernick17to18_preprocessed.csv", header=False, index=False)


