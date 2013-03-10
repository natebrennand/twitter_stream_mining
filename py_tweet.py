import string
import json


# strips non ascii characters
def strip_non_ascii(text):
	text = filter(lambda x: x in string.printable, text)
	text = str(text)
	return text

# object for every tweet
class tweet(object):
	def __init__(self, tweet_data):
		json_tweet = json.loads(tweet_data)
		self.message = strip_non_ascii(json_tweet['text'])
		self.user = strip_non_ascii(json_tweet['user']['screen_name'])
		self.time = json_tweet['created_at']
		
		self.hashtag_list = []
		for tag in json_tweet['entities']['hashtags']:
			self.hashtag_list.append( strip_non_ascii(tag[u'text']).lower() )
		self.hashtags = self.hashtag_string()

		tweet_id = str(json_tweet['id'])	#Unique
		self.url = str('https://twitter.com/'+self.user+'/status/'+tweet_id)

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
		tag_string = "Hashtags: "
		
		if not self.hashtag_list:
			tag_string += "none"
		else:
			for tag in self.hashtag_list:
				tag_string += tag+" "
		
		return tag_string

