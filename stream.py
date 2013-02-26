import tweepy.streaming
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import atexit
import py_tweet
from time import ctime


class StdOutListener( tweepy.streaming.StreamListener):
	def on_data(self, data):
		tweet_match = py_tweet.tweet(data)

		if hashtag_filter(tweet_match.hashtag_list):
			output = ''
			for i in range(len(output_choices)):
				if output_choices[i]:
					output += getattr(tweet_match,output_options[i])+'\n'
			log_file.write(output + '\n')
			print output

		return True

# Requires ONE hashtag to be in the tweet.
def hashtag_OR_filter(hashtags):
	for query in hashtag_queries:
		if query in hashtags:
			return True
	return False

# Requres ALL hashtags to be in the tweet.
def hashtag_AND_filter(hashtags):
	for query in hashtag_queries:
		if query not in hashtags:
			return False
	return True

def start_record():
	start_time = ctime()
	log_file = open(str("logs/"+'-'.join(hashtag_queries)+
			"_log+"+start_time+".txt"),'w+')
	log_file.write('Log file of tweets containing the hashtag '+
		'-'.join(hashtag_queries)+'.\n\tLog began at '+start_time+'\n\n')
	atexit.register( clean_up,log_file)
	return log_file

def clean_up(log):
	log.write('\n\tLog closed at '+ctime())
	log.close()

def choose_outputs(output_options):
	output_choices = []

	print "Enter Y for yes or N for no if for all of the following output options."
	for choice in output_options:
		choice = str( raw_input(choice.ljust(12))).upper()
		if 'Y' in choice:
			output_choices.append(True)
		else:
			output_choices.append(False)
	if False not in output_choices:		# Outputs URL by default if no options are chosen.
		output_choices[2] = True
	# Return array of boolean choices
	return output_choices


if __name__ == '__main__':
	listener = StdOutListener()
	auth = OAuthHandler(credentials.consumer_key, 
						credentials.consumer_secret)
	auth.set_access_token(credentials.access_token,
						credentials.access_token_secret)
	stream = Stream(auth, listener)	

	query = str(raw_input('Enter the hashtags you would like to search for '
				+ 'separated by spaces: ')).lower()
	hashtag_queries = query.split(' ')

	search_type = str(raw_input('Should returned tweets include all or 1< hashtags? Enter '+
		'"all" or "one"')).lower()
	if 'all' in search_type:
		hashtag_filter = hashtag_AND_filter
	else:
		hashtag_filter = hashtag_OR_filter

	output_options = ['user','message','url','time','hashtags']
	output_choices = choose_outputs(output_options)

	log_file = start_record()

	stream.filter( track = hashtag_queries )




