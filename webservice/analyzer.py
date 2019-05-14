import itertools
import re
import string
from collections import Counter, defaultdict
from functools import reduce
from operator import itemgetter
from typing import Dict, List, NamedTuple

import numpy as np
from numpy.linalg import norm
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from models.review import Marketplace

### File IO and processing

def read_stopwords(file):
    with open(file) as f:
        return set([x.strip() for x in f.readlines()])

stopwords = read_stopwords('resources/common_words')
stemmer = SnowballStemmer('english')


### Term-Document Matrix

def compute_review_freq(review):
    '''
    Computes review frequency, i.e. how many reviews contain a specific phrase
    '''
    freq = Counter()
    phrases = set()
    for sec in [review.processed_content]:
        # bigrams
        for i in range(len(sec) - 1):
            phrases.add(' '.join([sec[i], sec[i+1]]))

        # trigrams
        for i in range(len(sec) - 2):
            phrases.add(' '.join([sec[i], sec[i+1], sec[i+2]]))

    for phrase in phrases:
        freq[phrase] += 1

    return freq

def compute_review_freqs(reviews):
    '''
    Computes review frequency, i.e. how many reviews contain a specific phrase
    '''
    freq = Counter()
    marketplace_freq = defaultdict(Counter)
    for review in reviews:
        phrases = set()
        for sec in [review.processed_content]:
            # bigrams
            for i in range(len(sec) - 1):
                phrases.add(' '.join([sec[i], sec[i+1]]))

            # trigrams
            for i in range(len(sec) - 2):
                phrases.add(' '.join([sec[i], sec[i+1], sec[i+2]]))

        for phrase in phrases:
            freq[phrase] += 1
            marketplace_freq[review.marketplace][phrase] += 1

    return freq, marketplace_freq


def process_review(review):
    review.processed_content = review.content.translate(str.maketrans('', '', string.punctuation + '’'))
    review.processed_content = list(map(lambda word: word.lower(), word_tokenize(review.processed_content)))
    review.processed_content = [word for word in review.processed_content if word not in stopwords]
    # review.processed_content = [stemmer.stem(word) for word in review.processed_content]
    review.topics = compute_review_freq(review)


def analyze(reviews):
    rated_reviews = defaultdict(lambda: defaultdict(list))
    for review in reviews:
        process_review(review)
        rated_reviews[review.stars][review.marketplace].append(review)

    common_topics = defaultdict(list)
    for rating, marketplaces in rated_reviews.items():
        topics = []
        reviews_for_freq = [item for sublist in marketplaces.values() for item in sublist]
        freqs, marketplace_freqs = compute_review_freqs(reviews_for_freq)
        top_topics = sorted(freqs.items(), key=itemgetter(1), reverse=True)[:7]
        for topic, freq in top_topics:
            marketplace_freq = list(map(lambda x: marketplace_freqs[x][topic], Marketplace.all()))
            topics.append([topic, freq] + marketplace_freq)

        common_topics[rating] = topics

    return rated_reviews, common_topics
