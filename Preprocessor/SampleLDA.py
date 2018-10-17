%%time # prints the total processing time of the program
import nltk
import re
from nltk.corpus import stopwords
import pandas as pd
import string
import csv
from nltk.tokenize import WhitespaceTokenizer
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora, models
from nltk.stem import PorterStemmer


stop_words = set(stopwords.words('english')) #set nltk stopwords library


def preprocess(s , lowercase=True):
    ws_tok = WhitespaceTokenizer()
    tokens = ws_tok.tokenize(s)
    ps = PorterStemmer()

    if lowercase:
        tokens = [token.lower() for token in tokens] #to lower
        stp_wrd_filtered_words= [word for word in tokens if not word in stop_words] #filter stop words
        num_filtered_tokens = [word for word in stp_wrd_filtered_words if word.isalpha()] #remove number tokens
        n_char_filtered_tokens = [re.sub(r'\W*\b\w{1,3}\b', "", word) for word in num_filtered_tokens] #remove url tokens
        stem_tokens = [ps.stem(word) for word in n_char_filtered_tokens]
        return stem_tokens
    
        
with open("C:/Users/Idah/knime-workspace/Example Workflows/TheData/Misc/500 Restaurant Reviews.csv", encoding='utf-8') as file:
            reader= csv.reader(file)
            preprocsd_reviews = []
            for row in reader:
                preprocsd_review = preprocess(str(row))
                preprocsd_reviews.append(list(filter(None, preprocsd_review)))
            dictionary = corpora.Dictionary(preprocsd_reviews)
            corpus = [dictionary.doc2bow(preprocsd_review) for preprocsd_review in preprocsd_reviews]
            lda_model = models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)
            print(lda_model.print_topics(num_topics=10, num_words=5))
            
            #Comment out the code below to export results to csv file
           # top_words_per_topic = []
           # for t in range(lda_model.num_topics):
               # top_words_per_topic.extend([(t, ) + x for x in lda_model.show_topic(t, topn = 5)])
#pd.DataFrame(top_words_per_topic, columns=['Topic', 'Word', 'P']).to_csv("C:/Users/Idah/knime-workspace/Example Workflows/TheData/Misc/top_words500.csv")

