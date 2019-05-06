from bs4 import BeautifulSoup
import requests
import time
import datetime
#test link#
class Review():
	def __init__(self, date, title, content, stars, version):
		self.date = date
		self.title = title
		self.content = content
		self.stars = stars
		self.version = version
xml_link = "https://itunes.apple.com/us/rss/customerreviews/id=1057889290/sortBy=mostRecent/xml"
xml_content = ""
soup = BeautifulSoup(requests.get(xml_link).text, "lxml")
reviews = []
#runs through xml and extracts information about each review#
for review in soup.find_all('entry'):
	#converting string to timestamp#
	date = time.mktime(datetime.datetime.strptime(review.find('updated').text.split('T')[0], "%Y-%m-%d").timetuple())
	#title of comment#
	title = str(review.find('title').text.encode('utf-8'))
	#content body#
	content = str(review.find('content').text.encode('utf-8'))
	#number of review stars#
	stars = int(review.find('im:rating').text)
	#version no#
	version = float(review.find('im:version').text)
	
	review = Review(date, title, content, stars, version)
	reviews.append(review)
