from datetime import datetime
from models.reportdata import ReportData
from models.review import Marketplace
from yattag import Doc, indent
import random

class InstanceLink:
    def __init__(self, text, rating, topic):
        self.text = text
        self.rating = rating
        self.topic = topic

    def link(self):
        return '/reviews?rating=' + str(self.rating) + '&topic=' + self.topic


class Report:
    def __init__(self, data):
        self.data = data

        self.doc, self.tag, self.text = Doc().tagtext()
        self.doc.asis('<!DOCTYPE html>')

    def subhead_divider(self, id, subhead):
        self.doc.stag('hr', id='divider01')
        with self.tag('h3', id=id):
            self.text(subhead)

    def bold_title_reg_text(self, title, text):
        with self.tag('span'):
            with self.tag('strong'):
                self.text(title + ': ')
            self.text(text)
        self.doc.stag('br')

    def link(self, text, url):
        with self.tag('a', href=url):
            self.text(text)

    def go_to_toc(self):
        with self.tag('p', id='text04'):
            with self.tag('span'):
                self.link('Go to Top ↑', '#toc')

    def table(self, titles, rows):
        with self.tag('div', id='table02', klass='table-wrapper'):
            with self.tag('div', klass='table-inner'):
                with self.tag('table'):
                    with self.tag('thead'):
                        with self.tag('tr'):
                            for th in titles:
                                with self.tag('th'):
                                    self.text(th)

                    with self.tag('tbody'):
                        for tr in rows:
                            with self.tag('tr'):
                                for td in tr:
                                    with self.tag('td'):
                                        if isinstance(td, InstanceLink):
                                            self.link(td.text, td.link())
                                        else:
                                            self.text(td)

    def head(self):
        name = self.data.app_name
        today_str = datetime.today().strftime('%B %d, %Y @ %I:%M %p')
        title = name + ' App Review Report'

        with self.tag('head'):
            with self.tag('title'):
                self.text(title)

            self.doc.stag('meta', charset='utf-8')
            self.doc.stag('meta', name='viewport', content='width=device-width,initial-scale=1,user-scalable=no')
            self.doc.stag('meta', name='description', content=title + ' | ' + today_str)
            self.doc.stag('link', rel='stylesheet', href='static/main.css')

            with self.tag('noscript'):
                self.doc.stag('link', rel='stylesheet', href='static/noscript.css')


    def title(self):
        name = self.data.app_name
        today_str = datetime.today().strftime('%B %d, %Y at %I:%M %p')
        title = name + ' App Review Report'

        with self.tag('div', id='columns01', klass='container'):
            with self.tag('div', klass='inner'):
                with self.tag('h1', id='text02'):
                    self.text(title)

                with self.tag('p', id='text01'):
                    self.text('Generated ' + today_str)

    def links(self):
        with self.tag('p', id='text04'):
            with self.tag('span'):
                with self.tag('strong'):
                    self.link('App Store Link', self.data.app_store_link)
            self.doc.stag('br')
            with self.tag('span'):
                with self.tag('strong'):
                    self.link('Play Store Link', self.data.play_store_link)

    def toc(self):
        self.subhead_divider('toc', 'Table of Contents')

        toc = [
            ('Ratings', '#ratings'),
            ('Review Sentiment', '#review_sentiment'),
            ('Frequent Comment Topics (5 Stars)', '#fct_5'),
            ('Frequent Comment Topics (4 Stars)', '#fct_4'),
            ('Frequent Comment Topics (3 Stars)', '#fct_3'),
            ('Frequent Comment Topics (2 Stars)', '#fct_2'),
            ('Frequent Comment Topics (1 Stars)', '#fct_1'),
            ('Recent Positive Reviews', '#rpr'),
            ('Recent Negative Reviews', '#rnr')
        ]

        with self.tag('p', id='text04'):
            for text, url in toc:
                self.link(text, url)
                self.doc.stag('br')

    def average_reviews(self):
        self.subhead_divider('ratings', 'Ratings')
        with self.tag('p', id='text04'):
            self.bold_title_reg_text('Average Review', self.data.ratings.average_all_marketplaces())
            for marketplace in Marketplace.all():
                self.bold_title_reg_text('Average ' + str(marketplace) + ' Review', self.data.ratings.average(marketplace))

    def ratings_table(self):
        self.table(['Ratings', 'Total', 'App Store', 'Play Store'], self.data.ratings.rows())

    def review_sentiment(self):
        self.subhead_divider('review_sentiment', 'Review Sentiment')
        self.table(['Sentiment', 'Total', 'App Store', 'Play Store'], self.data['sentiment'])

    def comment_topics(self, rating):
        self.subhead_divider('fct_' + str(rating), 'Frequent Comment Topics (' + str(rating) + ' Stars)')
        rows = self.data.common_topics_rows(rating)
        for row in rows:
            row += [InstanceLink('See instances', rating, row[0])]

        self.table(['Topic', 'Total', 'App Store', 'Play Store', 'More'], rows)

    def reviews(self, reviews):
        for review in reviews:
            with self.tag('p', id='text03'):
                self.bold_title_reg_text('Title', str(review.title))
                self.bold_title_reg_text('Date', review.date)
                self.bold_title_reg_text('App Version', review.version)
                self.bold_title_reg_text('Marketplace', str(review.marketplace))
                self.bold_title_reg_text('Rating', str(review.stars) + '/5')

                with self.tag('span'):
                    self.text(review.content)

    def pos_reviews(self):
        self.subhead_divider('rpr', 'Most Upvoted Positive Reviews')
        self.reviews(self.data.reviews_for_ratings(range(4, 6), 3))

    def neg_reviews(self):
        self.subhead_divider('rnr', 'Most Upvoted Negative Reviews')
        self.reviews(self.data.reviews_for_ratings(range(1, 4), 3))

    def generate(self):
        with self.tag('html', lang='en'):
            self.head()

            with self.tag('body', klass='is-loading'):
                with self.tag('div', id='wrapper'):
                    with self.tag('div', id='main'):
                        with self.tag('div', klass='inner'):
                            self.title()
                            self.links()
                            self.toc()
                            self.average_reviews()
                            self.ratings_table()
                            self.go_to_toc()

                            for rating in reversed(range(1,6)):
                                self.comment_topics(rating)
                                self.go_to_toc()

                            additional_sections = [
                                    self.pos_reviews,
                                    self.neg_reviews
                                ]

                            for section in additional_sections:
                                section()
                                self.go_to_toc()

                with self.tag('script', src='static/main.js'):
                    self.text('')

        return indent(self.doc.getvalue())
