from analyzer import analyze
from scraper import scan_apple_reviews, scan_google_reviews
from collections import defaultdict
from models.reportdata import ReportData
from report_generator import Report
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/report', methods=['GET'])
def report():
    app_name = request.args.get('app-name')
    apple_link = request.args.get('app-store-link')
    google_link = request.args.get('play-store-link')

    # TODO: param checking

    apple = scan_apple_reviews(apple_link)
    # google = scan_google_reviews(google_link)
    reviews = apple# + google
    rated_reviews, common_topics = analyze(reviews)
    report_data = ReportData(app_name, apple_link, google_link, rated_reviews, common_topics)
    report = Report(report_data)
    html = report.generate()
    return html


if __name__=='__main__':
    app.run(debug=True)
