import tweepy
import urllib2

auth = tweepy.OAuthHandler("pR3JDWZSJGtAPNK6X1VPxRpVu", "MVxGRv7Hl59mjNeuQ3QjWhtPrFL8bD9iQM3bVvuyzvGiwjcUCX")
auth.set_access_token("1014109820385939456-JIX4nPJ4IIMzxSvUNWvEH5MgF2wrxn", "qw87e6otiwYBbEIrLzRzGbwAHmkALmZ0JfR1l47rNmBxL")

api = tweepy.API(auth)

public_tweets = api.home_timeline()

def parsePopular(response):
	
	print response

class TrevorRequest:
	def makeRequest(self, modelId):
		base_url = "http://trevor-producer-cdn.api.bbci.co.uk/content"
		full_url = base_url + modelId
		contents = urllib2.urlopen(full_url).read()
		return contents

trevor_request = TrevorRequest()
response = trevor_request.makeRequest("/most_popular/news")
parsePopular(response)