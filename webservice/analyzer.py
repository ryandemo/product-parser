import itertools
import re
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

def compute_review_freqs(reviews):
    '''
    Computes review frequency, i.e. how many reviews contain a specific phrase
    '''
    freq = Counter()
    marketplace_freq = defaultdict(Counter)
    for review in reviews:
        phrases = set()
        for sec in review.sections():
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

# def compute_tf(doc: Document, doc_freqs: Dict[str, int], num_docs: int):
#     vec = defaultdict(float)
#     for docsection in doc.sections():
#         for i in range(len(docsection) - 1):
#             vec[docsection[i]] += 1
#             if docsection[i] not in stopwords and docsection[i+1] not in stopwords:
#                 vec['+'.join([docsection[i], docsection[i+1]])] += 1
#         if len(docsection):
#             vec[docsection[-1]] += 1
#
#         chars = '_'.join(docsection)
#         for i in range(len(chars) - 4):
#             vec[chars[i:i+5]] += 1
#
#     return dict(vec)  # convert back to a regular dict
#
# def compute_tfidf(doc, doc_freqs, num_docs):
#     vec = compute_tf(doc, doc_freqs, num_docs)
#     for word in vec:
#         if word in doc_freqs:
#             vec[word] *= np.log(num_docs / doc_freqs[word])
#     return vec
#
# def average_vectors(docs):
#     acc_dict = defaultdict(float)
#     for doc in docs:
#         doc_dict = uniform(doc)
#         for word in doc_dict:
#             acc_dict[word] += doc_dict[word]
#
#     for acc_dict in acc_dicts:
#         for k in acc_dict:
#             acc_dict[k] /= len(docs)
#
#     return acc_dicts[0], acc_dicts[1]
#
# def uniform(doc):
#     doc_dict = defaultdict(int)
#     for word in doc.words:
#         doc_dict[word] += 1
#
#     chars = '_'.join(doc.words)
#     for i in range(len(chars) - 4):
#         doc_dict[chars[i:i+5]] += 1
#
#     return doc_dict
#
#
# ### Vector Similarity
#
# def dictdot(x: Dict[str, float], y: Dict[str, float]):
#     '''
#     Computes the dot product of vectors x and y, represented as sparse dictionaries.
#     '''
#     keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
#     return sum(x.get(key, 0) * y.get(key, 0) for key in keys)
#
# def cosine_sim(x, y):
#     '''
#     Computes the cosine similarity between two sparse term vectors represented as dictionaries.
#     '''
#     num = dictdot(x, y)
#     if num == 0:
#         return 0
#     return num / (norm(list(x.values())) * norm(list(y.values())))


### Search

def process_review(review):
    review.processed_content = list(map(lambda word: word.lower(), word_tokenize(review.content)))
    review.processed_content = [word for word in review.processed_content if word not in stopwords]
    # review.processed_content = [stemmer.stem(word) for word in review.processed_content]
    review.topics = compute_review_freqs([review])


def analyze(reviews):
    rated_reviews = defaultdict(lambda: defaultdict(list))
    for review in reviews:
        process_review(review)
        rated_reviews[review.stars][review.marketplace].append(review)

    common_topics = defaultdict(list)
    for rating, marketplaces in rated_reviews.items():
        topics = []
        reviews = [item for sublist in marketplaces.values() for item in sublist]
        freqs, marketplace_freqs = compute_review_freqs(reviews)
        top_topics = sorted(freqs.items(), key=itemgetter(1), reverse=True)[:7]
        for topic, freq in top_topics:
            marketplace_freq = list(map(lambda x: marketplace_freqs[x][topic], Marketplace.all()))
            topics.append([topic, freq] + marketplace_freq)

        common_topics[rating] = topics

    return rated_reviews, common_topics


# def search(doc_vectors, query_vec, sim):
#     results_with_score = [(doc_id + 1, cosine_sim(query_vec, doc_vec))
#                     for doc_id, doc_vec in enumerate(doc_vectors)]
#     results_with_score = sorted(results_with_score, key=lambda x: -x[1])
#     results = [x[0] for x in results_with_score]
#     return results
