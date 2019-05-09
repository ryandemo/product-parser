from datetime import datetime
from models.reportdata import ReportData
from models.review import Marketplace
from yattag import Doc, indent
import random

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
            self.doc.stag('link', rel='stylesheet', href='assets/main.css')

            with self.tag('noscript'):
                self.doc.stag('link', rel='stylesheet', href='assets/noscript.css')


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
            ('Frequent Comment Topics (4-5 Stars)', '#fct_45'),
            ('Frequent Comment Topics (3 Stars)', '#fct_3'),
            ('Frequent Comment Topics (1-2 Stars)', '#fct_12'),
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

    def comment_topics(self, topics_arr_name):
        self.table(['Topic', 'Total', 'App Store', 'Play Store', 'More'], self.data[topics_arr_name])

    def comment_topics_pos(self):
        self.subhead_divider('fct_45', 'Frequent Comment Topics (4-5 Stars)')
        self.comment_topics('topics_positive')

    def comment_topics_neutral(self):
        self.subhead_divider('fct_3', 'Frequent Comment Topics (3 Stars)')
        self.comment_topics('topics_neutral')

    def comment_topics_neg(self):
        self.subhead_divider('fct_12', 'Frequent Comment Topics (1-2 Stars)')
        self.comment_topics('topics_negative')

    def reviews(self, review_arr_name):
        for review in self.data.reviews_for_marketplace(Marketplace.APP_STORE):
            with self.tag('p', id='text03'):
                self.bold_title_reg_text('Title', str(review.title))
                self.bold_title_reg_text('Date', review.date)
                self.bold_title_reg_text('Marketplace', str(review.marketplace))
                self.bold_title_reg_text('Rating', str(review.stars) + '/5')

                with self.tag('span'):
                    self.text(review.content)


    def pos_reviews(self):
        self.subhead_divider('rpr', 'Recent Positive Reviews')
        self.reviews('reviews')

    def neg_reviews(self):
        self.subhead_divider('rnr', 'Recent Negative Reviews')
        self.reviews('reviews')

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
                            sections = [
                                    self.ratings_table,
                                    # self.review_sentiment,
                                    # self.comment_topics_pos,
                                    # self.comment_topics_neutral,
                                    # self.comment_topics_neg,
                                    self.pos_reviews,
                                    # self.neg_reviews
                                ]

                            for section in sections:
                                section()
                                self.go_to_toc()

                with self.tag('script', src='assets/main.js'):
                    self.text('')

        return indent(self.doc.getvalue())


def main():
    data = {
        'app_name': 'Facebook',
        'app_store_link': '',
        'play_store_link': '',
        'average_review': 3.9,
        'average_review_app_store': 4.0,
        'average_review_play_store': 3.6,
        'ratings_table': [
            ['5-Star', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)],
            ['4-Star', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)],
            ['3-Star', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)],
            ['2-Star', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)],
            ['1-Star', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)]
        ],
        'sentiment': [
            ['Positive', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)],
            ['Negative', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)]
        ],
        'topics_positive': [
            ['groups', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['cover photos', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['suggested friends', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances']
        ],
        'topics_neutral': [
            ['messenger', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['tabs', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['news feed', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
        ],
        'topics_negative': [
            ['notifications', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['slow', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
            ['not working', random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), 'See instances'],
        ],
        'reviews': [
            {
                'title': 'Zuck This App',
                'author': 'SuperUser',
                'marketplace': 'App Store',
                'rating': '5/5',
                'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sollicitudin venenatis arcu, semper pulvinar magna fringilla non. Suspendisse at sem in metus tristique faucibus. Vestibulum luctus velit ut dolor cursus scelerisque. Nullam accumsan vestibulum ante sed suscipit. Donec quis commodo quam, ut commodo risus. Donec in luctus urna.'
            },
            {
                'title': 'Zuck This App',
                'author': 'SuperUser',
                'marketplace': 'App Store',
                'rating': '5/5',
                'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sollicitudin venenatis arcu, semper pulvinar magna fringilla non. Suspendisse at sem in metus tristique faucibus. Vestibulum luctus velit ut dolor cursus scelerisque. Nullam accumsan vestibulum ante sed suscipit. Donec quis commodo quam, ut commodo risus. Donec in luctus urna.'
            },
            {
                'title': 'Zuck This App',
                'author': 'SuperUser',
                'marketplace': 'App Store',
                'rating': '5/5',
                'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sollicitudin venenatis arcu, semper pulvinar magna fringilla non. Suspendisse at sem in metus tristique faucibus. Vestibulum luctus velit ut dolor cursus scelerisque. Nullam accumsan vestibulum ante sed suscipit. Donec quis commodo quam, ut commodo risus. Donec in luctus urna.'
            }
        ]
    }
    report = Report(data)
    html = report.generate()
    with open('report.html', 'w+') as file:
        file.write(html)


if __name__ == '__main__':
    main()
