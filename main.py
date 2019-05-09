from analyzer import analyze
from scraper import scan_apple_reviews, scan_google_reviews
from collections import defaultdict
from models.reportdata import ReportData
from report_generator import Report

APP_NAME = 'Facebook'
APP_STORE_LINK = 'https://itunes.apple.com/us/app/facebook/id284882215?mt=8&v0=WWW-NAUS-ITSTOP100-FREEAPPS&l=en&ign-mpt=uo%3D4'
PLAY_STORE_LINK = 'https://play.google.com/store/apps/details?id=com.facebook.katana&hl=en_US'

def main():
    apple = scan_apple_reviews(APP_STORE_LINK)
    google = [] #scan_google_reviews(PLAY_STORE_LINK)
    reviews = apple + google
    rated_reviews, common_topics = analyze(reviews)
    report_data = ReportData(APP_NAME, APP_STORE_LINK, PLAY_STORE_LINK, rated_reviews, common_topics)
    report = Report(report_data)
    html = report.generate()
    with open('report.html', 'w+') as file:
        file.write(html)


if __name__ == '__main__':
    main()
