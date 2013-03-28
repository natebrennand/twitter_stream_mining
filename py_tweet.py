import string
import json
import requests
from credentials import username

# strips non ascii characters
def strip_non_ascii(text):
	text = filter(lambda x: x in string.printable, text)
	text = str(text)
	return text

def reverse_geoencode(latitude,longitude):
	payload = {'lat':latitude,'lng':longitude,'username':username}
	r = requests.get('http://api.geonames.org/countrySubdivisionJSON',params=payload)
	data = json.loads(r.text)
	country = data[u'countryName'].encode('ascii','ignore')
	state = data[u'adminName1'].encode('ascii','ignore')
	state_initial = data[u'adminCode1'].encode('ascii','ignore')
	return country,state,state_initial


# object for every tweet
class tweet(object):

	def __init__(self, tweet_data):
		json_tweet = json.loads(tweet_data)
		self.message = strip_non_ascii(json_tweet['text'])
		self.user = strip_non_ascii(json_tweet['user']['screen_name'])
		self.time = json_tweet['created_at'].encode('ascii','ignore')
		
		self.hashtag_list = []
		for tag in json_tweet['entities']['hashtags']:
			self.hashtag_list.append( strip_non_ascii(tag[u'text']).lower() )
		self.hashtags = self.hashtag_string()

		if json_tweet['coordinates'] is None:
			self.longitude = None
			self.latitude = None
			self.country = None
			self.state = None
			self.state_initial = None
		else:
			self.longitude = json_tweet['coordinates']['coordinates'][0]
			self.latitude = json_tweet['coordinates']['coordinates'][1]
			self.country,self.state,self.state_initial = reverse_geoencode(
				self.longitude,self.latitude)

		tweet_id = str(json_tweet['id'])	#Unique
		self.url = str('https://twitter.com/'+self.user+'/status/'+tweet_id)

	def get_tuple(self):
		return ( self.url, self.user, self.message, self.hashtags, self.time,
			self.longitude, self.latitude, self.country, self.state, self.state_initial)

	def to_string(self):
		pretty = self.message+'\n'
		if self.user:
			pretty = self.user + '\n' + user
		if self.time:
			pretty += '\n' + time
		if self.hashtag_list:
			pretty += '\n' + self.hashtag_string
		return pretty

	def hashtag_string(self):
		tag_string = ''
		if not self.hashtag_list:
			tag_string += "none"
		else:
			for tag in self.hashtag_list:
				tag_string += tag+" "
		
		return tag_string

