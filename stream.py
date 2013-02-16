import tweepy.streaming
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import json

class StdOutListener( tweepy.streaming.StreamListener):

	def on_data(self, data):

		tweet = json.loads(data)
		if str('#'+hashtag_query) in tweet['text']:
			print url_tweet(tweet)
		return True

	def on_error(self, status):
		print status

def prettify_tweet(tweet):
	user = str(tweet['user']['screen_name'])
	text = str(tweet['text'])
	pretty = str(user + '\t tweeted\n\t' + text)
	return pretty

def url_tweet(tweet):
	user = str(tweet['user']['screen_name'])
	tweet_id = str(tweet['id'])
	return str('https://twitter.com/'+user+'/status/'+tweet_id)

if __name__ == '__main__':

	consumer_key = credentials.consumer_key
	consumer_secret = credentials.consumer_secret
	access_token = credentials.access_token
	access_token_secret = credentials.access_token_secret

	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = Stream(auth, l)	

	hashtag_query = str(raw_input('Enter the hashtag you would like to search for: '))
	stream.filter(track=[hashtag_query])

