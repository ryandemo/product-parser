from datetime import datetime
from yattag import Doc, indent

class Report:
    def __init__(self, data):
        self.data = data

        self.doc, self.tag, self.text = Doc().tagtext()
        self.doc.asis('<!DOCTYPE html>')

    def head(self):
        name = self.data['appname']
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
        name = self.data['appname']
        today_str = datetime.today().strftime('%B %d, %Y at %I:%M %p')
        title = name + ' App Review Report'

        with self.tag('div', id='columns01', klass='container'):
            with self.tag('div', klass='inner'):
                with self.tag('h1', id='text02'):
                    self.text(title)

                with self.tag('p', id='text01'):
                    self.text('Generated ' + today_str)

    def links(self):
        pass

    def average_reviews(self):
        pass

    def ratings_table(self):
        pass

    def review_sentiment(self):
        pass

    def comment_topics_pos(self):
        pass

    def comment_topics_neg(self):
        pass

    def pos_reviews(self):
        pass

    def neg_reviews(self):
        pass

    def generate(self):
        with self.tag('html', lang='en'):
            self.head()

            with self.tag('body', klass='is-loading'):
                with self.tag('div', id='wrapper'):
                    with self.tag('div', id='main'):
                        with self.tag('div', klass='inner'):
                            self.title()
                            self.links()
                            self.average_reviews()
                            self.ratings_table()
                            self.review_sentiment()
                            self.comment_topics_pos()
                            self.comment_topics_neg()
                            self.pos_reviews()
                            self.neg_reviews()

                with self.tag('script', src='assets/main.js'):
                    self.text('')

        return indent(self.doc.getvalue())


def main():
    data = {'appname': 'Facebook'}
    report = Report(data)
    html = report.generate()
    with open('report.html', 'w+') as file:
        file.write(html)


if __name__ == '__main__':
    main()
