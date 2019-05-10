from datetime import datetime
from models.reportdata import ReportData
from models.review import Marketplace
from yattag import Doc, indent
import random

class CommonTopics:
    def __init__(self, data, rating, topic):
        self.data = data
        self.rating = rating
        self.topic = topic

        self.doc, self.tag, self.text = Doc().tagtext()
        self.doc.asis('<!DOCTYPE html>')

    def divider(self):
        self.doc.stag('hr', id='divider01')

    def bold_title_reg_text(self, title, text):
        with self.tag('span'):
            with self.tag('strong'):
                self.text(title + ': ')
            self.text(text)
        self.doc.stag('br')

    def link(self, text, url):
        with self.tag('a', href=url):
            self.text(text)

    def head(self):
        with self.tag('head'):
            with self.tag('title'):
                self.text('"' + self.topic + '" Topic Instances')

            self.doc.stag('meta', charset='utf-8')
            self.doc.stag('meta', name='viewport', content='width=device-width,initial-scale=1,user-scalable=no')
            self.doc.stag('meta', name='description', content='Common Topic Instances | ' + self.topic)
            self.doc.stag('link', rel='stylesheet', href='static/main.css')

            with self.tag('noscript'):
                self.doc.stag('link', rel='stylesheet', href='static/noscript.css')

    def title(self, instances, marketplace_instances):
        with self.tag('div', id='columns01', klass='container'):
            with self.tag('div', klass='inner'):
                with self.tag('h1', id='text02'):
                    self.text('"' + self.topic + '" Topic Instances')

                with self.tag('p', id='text01'):
                    self.bold_title_reg_text('Topic', self.topic)
                    self.bold_title_reg_text('Rating', str(self.rating) + '/5')
                    self.bold_title_reg_text('Total Instances', instances)
                    for marketplace in Marketplace.all():
                        self.bold_title_reg_text(str(marketplace) + ' Instances', marketplace_instances[marketplace])

        self.divider()

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

    def generate(self):
        reviews_topic, marketplace_instances = self.data.reviews_for_rating_topic(self.rating, self.topic)

        with self.tag('html', lang='en'):
            self.head()

            with self.tag('body', klass='is-loading'):
                with self.tag('div', id='wrapper'):
                    with self.tag('div', id='main'):
                        with self.tag('div', klass='inner'):
                            self.title(len(reviews_topic), marketplace_instances)
                            self.reviews(reviews_topic)

                with self.tag('script', src='static/main.js'):
                    self.text('')

        return indent(self.doc.getvalue())
