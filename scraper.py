from bs4 import BeautifulSoup
import requests
import time
import datetime
import re
#test link#
class Review():
	def __init__(self, date, title, content, stars, version):
		self.date = date
		self.title = title
		self.content = content
		self.stars = stars
		self.version = version

#takes the url to the app store and returns processed list of comments#
#url = url from appstore#
def scan_reviews(url):
	#extracting app id from appstore url#
	app_id = re.sub("((id)|\?)","",re.findall("id[\d]+\?", url)[0])
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

	return(reviews)
#output to make sure it works#
print(scan_reviews("https://itunes.apple.com/us/app/facebook/id284882215?mt=8&v0=WWW-NAUS-ITSTOP100-FREEAPPS&l=en&ign-mpt=uo%3D4")[0].content)