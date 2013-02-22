import tweepy.streaming
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import json
import string
import atexit
from time import ctime
from sys import argv

class StdOutListener( tweepy.streaming.StreamListener):
	def on_data(self, data):
		tweet = json.loads(data)
		if hashtag_query in hashtag_tweet(tweet):
			output = ""
			if output_url:
				output += url_tweet(tweet) + '\n'
			if output_user:
				output += user_tweet(tweet) + '\n'
			if output_message:
				output += message_tweet(tweet) + '\n'
			if output_time:
				output += time_tweet(tweet) + '\n'
			if output_hashtag:
				output += hashtag_tweet(tweet) + '\n'
			print output,
			log_file.write(output)
		return True
	
def url_tweet(tweet):
	user = str(tweet['user']['screen_name'])
	tweet_id = str(tweet['id'])
	return str('https://twitter.com/'+user+'/status/'+tweet_id)

# lower case and strips non ascii characters
def strip_non_ascii(text):
	text = filter(lambda x: x in string.printable, text)
	text = str(text)
	return text

def hashtag_tweet(tweet):
	hashtags = tweet['entities']['hashtags']
	tag_list = []
	for tag in hashtags:
		tag_list.append( strip_non_ascii(tag[u'text']).lower() )
	return tag_list

def user_tweet(tweet):
	user = strip_non_ascii(tweet['user']['screen_name'])
	return user

def message_tweet(tweet):
	text = strip_non_ascii(tweet['text'])
	return text

def time_tweet(tweet):
	time = tweet['created_at']
	return time

def clean_up(log):
	log.write('\n\tLog closed at '+ctime())
	log.close()

if __name__ == '__main__':
	listener = StdOutListener()
	auth = OAuthHandler(credentials.consumer_key, 
						credentials.consumer_secret)
	auth.set_access_token(credentials.access_token,
						credentials.access_token_secret)
	stream = Stream(auth, listener)	

	if len(argv) == 3:
		hashtag_query = str(argv[1])
		output_choice = str(argv[2])
	else:
		hashtag_query = str(raw_input('Enter the hashtag you would like to search for: ')).lower()
	
		output_choice = str(raw_input('Output options, enter all that you '
			+'would like to view\nuser\tmessage\turl\ttime\thashtag\n')).lower()
	
	output_message = False
	if 'message' in output_choice:
		output_message = True
	output_user = False
	if 'user' in output_choice:
		output_tweet = True
	output_url = False
	if 'url' in output_choice:
		output_url = True
	output_time = False
	if 'time' in output_choice:
		output_time = True
	output_hashtag = False
	if 'hashtag' in output_choice:
		output_hashtag = True

	if not output_time or output_url or output_message or output_user or output_hashtag:
		output_tweet = True

	start_time = ctime()
	log_file = open(str(hashtag_query+"_log+"+start_time+".txt"),'w+')
	log_file.write('Log file of tweets containing the hashtag '+hashtag_query
			+'.\n\tLog began at '+start_time+'\n\n')
	atexit.register( clean_up,log_file)

	stream.filter(track=[str('#'+hashtag_query)])




