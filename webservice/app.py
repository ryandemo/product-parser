#!/usr/bin/env python

from analyzer import analyze
from scraper import scan_apple_reviews, scan_google_reviews
from models.reportdata import ReportData
from gen_common_topics import CommonTopics
from gen_report import Report
from flask import Flask, render_template, request

app = Flask(__name__)
report_data = None

def generate_report(args):
    global report_data

    app_name = args.get('app-name')
    apple_link = args.get('app-store-link')
    google_link = args.get('play-store-link')

    if report_data and report_data.app_name == app_name:
        return

    apple = scan_apple_reviews(apple_link)
    google = scan_google_reviews(google_link)
    reviews = apple + google
    rated_reviews, common_topics = analyze(reviews)
    report_data = ReportData(app_name, apple_link, google_link, rated_reviews, common_topics)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    global report_data
    generate_report(request.args)

    report = Report(report_data)
    html = report.generate()
    return html

@app.route('/reviews')
def list_reviews():
    global report_data
    generate_report(request.args)

    rating = int(request.args.get('rating'))
    topic = request.args.get('topic')

    topics = CommonTopics(report_data, rating, topic)
    html = topics.generate()
    return html

if __name__=='__main__':
    app.run(debug=True)
