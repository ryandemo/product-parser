from enum import Enum

class Marketplace(Enum):
	APP_STORE = 0
	PLAY_STORE = 1

	def __str__(self):
		if self == Marketplace.APP_STORE:
			return "App Store"
		else:
			return "Play Store"

	@classmethod
	def all(cls):
		return [Marketplace.APP_STORE]#, Marketplace.PLAY_STORE]

class Review:
	def __init__(self, id, date, title, content, stars, version, upvotes, marketplace):
		self.id = id
		self.date = date
		self.title = title
		self.content = content
		self.stars = stars
		self.version = version
		self.upvotes = upvotes
		self.marketplace = marketplace

	def sections(self):
		return [self.processed_content]
