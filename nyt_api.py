import requests 
import nltk
import pprint

from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

from wordcloud import WordCloud
import matplotlib.pyplot as plt


options = [ 'arts', 'automobiles', 'books', 'business',
            'fashion', 'food', 'health', 'home',
            'insider', 'magazine', 'movies', 'nyregion',
            'obituaries', 'opinion', 'politics', 'realestate',
            'science', 'sports', 'sundayreview', 'technology',
            'theater', 't-magazine', 'travel', 'upshot',
            'us', 'world']


nyt_top_base = "https://api.nytimes.com/svc/topstories/v2/"
nyt_popular_base = "https://api.nytimes.com/svc/mostpopular/v2/"

def gen_top_url (subj, key, base = nyt_top_base):
    return base + subj + ".json?api-key=" + key

def gen_popular_url (share_method, timeframe, key, base = nyt_popular_base):
    return base + share_method + "/" + str(timeframe) + ".json?api-key=" + key



nltk.download("punkt")
nltk.download("stopwords")


# now tokenize and all that
def compile_dict_list_fields (dlist, field):
    return [entry[field] for entry in dlist]

def clean_tokens(text, stopwords):
    return [word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stopwords]


def tokenize_topic_abstracts (url, stopwords = stopwords.words("english")):
    response = requests.get(url).json()

    article_list = response["results"]
    full_text = ' '.join(compile_dict_list_fields(article_list, field = "abstract"))

    cleaned_list = clean_tokens(full_text, stopwords)
    return cleaned_list



def wc_of_abstracts (url, stopwords = stopwords.words("english")):
    cleaned_list = tokenize_topic_abstracts(url, stopwords)
    clean_text = ' '.join(cleaned_list)

    wc = WordCloud().generate(clean_text)
    return wc


def freqdist_of_abstracts (url, stopwords = stopwords.words("english")):
    cleaned_list = tokenize_topic_abstracts(url, stopwords)

    fdist = FreqDist(cleaned_list)
    return fdist
