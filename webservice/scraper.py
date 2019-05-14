from bs4 import BeautifulSoup
from models.review import Review, Marketplace
import requests
import time
import datetime
import re
import platform
from selenium import webdriver

# takes the url to the app store and returns processed list of comments
# url = url from appstore
def scan_apple_reviews(url):
	app_id = re.sub("((id)|\?)","",re.findall("id[\d]+\?", url)[0])

	# link for testing purposes, will be replaced with user input / string manip later
	#Helpful = mostHelpful#
	#fb text link: https://itunes.apple.com/us/rss/customerreviews/id=284882215/sortBy=mostRecent/xml#
	xml_link = "https://itunes.apple.com/us/rss/customerreviews/id="+app_id+"/sortBy=mostRecent/xml"
	soup = BeautifulSoup(requests.get(xml_link).content, "lxml")
	reviews = []

	# runs through xml and extracts information about each review
	for review in soup.find_all('entry'):
		id = int(review.find('id').text)
		# converting string to timestamp
		# date = time.mktime(datetime.datetime.strptime(review.find('updated').text.split('T')[0], "%Y-%m-%d").timetuple())
		date = review.find('updated').text
		# title of comment
		title = review.find('title').text
		# content body
		content = review.find('content').text
		# number of review stars
		stars = int(review.find('im:rating').text)
		# version no
		version = float(review.find('im:version').text)
		# number of upvotes
		upvotes = int(review.find('im:votesum').text)

		review = Review(id, date, title, content, stars, version, upvotes, Marketplace.APP_STORE)
		reviews.append(review)

	return reviews


def scan_google_reviews(url):
	url = url + "&showAllReviews=true"

	# headless chromium to render JS on website
	options = webdriver.ChromeOptions()
	options.add_argument('headless')

	driver_path = None
	system = platform.system()
	if system == 'Windows':
		driver_path = './resources/chromedriver.exe'
	elif system == 'Darwin':
		driver_path = './resources/chromedriver-mac'
	else:
		driver_path = './resources/chromedriver-linux'

	driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
	# getting results#
	driver.get(url)
	result = driver.page_source

	soup = BeautifulSoup(result, "html.parser")
	reviews = []
	#unique id no#
	code = 0
	for review in soup.find_all('div', 'd15Mdf'):
		# getting stars
		stars = -1
		content = ""
		title = ""
		date = ""

		for div in review.findChildren("div", recursive = True):
			label = ""
			try:
				label = div["aria-label"]
			except:
				pass
			if("1" in label):
				stars = 1
			elif("2" in label):
				stars = 2
			elif("3" in label):
				stars = 3
			elif("4" in label):
				stars = 4
			elif("5" in label):
				stars = 5

		date = review.find("span", "p2TkOb").get_text()
		# getting content
		content = review.find("span", jsname = "fbQN7e").get_text()
		#getting upvotes#
		upvotes = int(review.find("div", "jUL89d").get_text())
		# play does not have titles
		title = 'N/A'
		version = 'N/A'

		reviews.append(Review(code, date, title, content, stars, version, upvotes, Marketplace.PLAY_STORE))
		code += 1
	return reviews


def main():
	print(scan_apple_reviews("https://itunes.apple.com/us/app/facebook/id284882215?mt=8&v0=WWW-NAUS-ITSTOP100-FREEAPPS&l=en&ign-mpt=uo%3D4")[0].content)
	print(scan_google_reviews("https://play.google.com/store/apps/details?id=com.moonton.magicrush&hl=en_US")[0].stars)


if __name__ == '__main__':
	main()
