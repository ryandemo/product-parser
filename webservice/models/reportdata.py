from collections import defaultdict
from functools import reduce
from .review import Marketplace

import numpy as np

class ReportData:
    def __init__(self, app_name, app_store_link, play_store_link, analyzed_reviews, common_topics):
        self.app_name = app_name
        self.app_store_link = app_store_link
        self.play_store_link = play_store_link
        self.analyzed_reviews = analyzed_reviews
        self.ratings = Ratings(analyzed_reviews)
        self.common_topics = common_topics

    def reviews_for_marketplace(self, marketplace_filter):
        filtered_reviews = list()
        for rating, marketplace_reviews in self.analyzed_reviews.items():
            for marketplace, reviews in marketplace_reviews.items():
                if marketplace_filter == marketplace:
                    filtered_reviews += reviews
        return filtered_reviews

    def reviews_for_ratings(self, rating_range, limit):
        reviews = []
        for rating in rating_range:
            filtered_reviews = [item for sublist in self.analyzed_reviews[rating].values() for item in sublist]
            filtered_reviews = sorted(filtered_reviews, key=lambda x: x.upvotes, reverse=True)[:limit]
            reviews.extend(filtered_reviews)

        return sorted(reviews, key=lambda x: x.upvotes, reverse=True)[:limit]

    def common_topics_rows(self, rating):
        return self.common_topics[rating]

    def reviews_for_rating_topic(self, rating, topic):
        reviews = []
        marketplace_instances = defaultdict(int)
        for marketplace, marketplace_reviews in self.analyzed_reviews[rating].items():
            for review in marketplace_reviews:
                if topic in review.topics:
                    reviews.append(review)
                    marketplace_instances[marketplace] += 1

        return sorted(reviews, key=lambda x: x.upvotes, reverse=True), marketplace_instances


class Ratings:
    def __init__(self, rated_reviews):
        self.counts = defaultdict(lambda: defaultdict(int))
        for rating, marketplace_reviews in rated_reviews.items():
            for marketplace, reviews in marketplace_reviews.items():
                self.counts[rating][marketplace] = len(reviews)

    def count(self, rating, marketplace):
        if rating not in self.counts:
            return 0

        return self.counts[rating][marketplace]

    def total_rating(self, rating):
        return sum(self.counts[rating].values())

    def total_marketplace(self, marketplace):
        total_stars = 0
        total_possible = 0
        for rating, marketplaces in self.counts.items():
            total_stars += marketplaces[marketplace] * rating
            total_possible += marketplaces[marketplace] * 5

        return (total_stars, total_possible)

    def total_reviews(self):
        return sum(list(map(lambda rating: self.total_rating(rating), range(1, 6))))

    def average(self, marketplace):
        total_stars, total_possible = self.total_marketplace(marketplace)
        return round(float(total_stars)/float(total_possible if total_possible > 0 else 1) * 5, 2)

    def average_all_marketplaces(self):
        total_stars = 0
        total_possible = 0
        for marketplace in Marketplace.all():
            stars, possible = self.total_marketplace(marketplace)
            total_stars += stars
            total_possible += possible
        return round(float(total_stars)/float(total_possible if total_possible > 0 else 1) * 5, 2)

    def describe_rating_count(self, rating, marketplace):
        _, total_marketplace = self.total_marketplace(marketplace)
        count_rating_marketplace = self.count(rating, marketplace)
        percent = round(float(count_rating_marketplace)/float(total_marketplace/5) * 100)
        return str(count_rating_marketplace) + ' (' + str(percent) + '%)'

    def describe_total_rating_count(self, rating):
        total = self.total_reviews()
        count_rating = self.total_rating(rating)
        percent = round(float(count_rating)/float(total) * 100)
        return str(count_rating) + ' (' + str(percent) + '%)'

    def rows(self):
        row_list = list()
        total = self.total_reviews()
        for rating in reversed(range(1, 6)):
            marketplace_counts = list(map(lambda marketplace: self.describe_rating_count(rating, marketplace), Marketplace.all()))
            row_list.append([str(rating) + '-Star', self.describe_total_rating_count(rating)] + marketplace_counts)

        marketplace_totals = list(map(lambda marketplace: int(self.total_marketplace(marketplace)[1]/5), Marketplace.all()))
        row_list.append(['Total', self.total_reviews()] + marketplace_totals)
        return row_list
