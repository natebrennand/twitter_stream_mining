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

		output = ''
		for i in range(len(output_choices)):
			if output_choices[i]:
				output += getattr(tweet_match,output_options[i])+'\n'
		log_file.write(output + '\n')
		print output

		return True

def start_record():
	start_time = ctime()
	log_file = open(str("logs/"+hashtag_query+"_log+"+start_time+".txt"),'w+')
	log_file.write('Log file of tweets containing the hashtag '+hashtag_query
			+'.\n\tLog began at '+start_time+'\n\n')
	atexit.register( clean_up,log_file)
	return log_file

def clean_up(log):
	log.write('\n\tLog closed at '+ctime())
	log.close()

def choose_outputs(output_options):
	output_choices = []

	print "Enter Y for yes or N for no if for all of the following output options."
	for choice in output_options:
		choice = str( raw_input(choice+'\t')).upper()
		if 'Y' in choice:
			output_choices.append(True)
		else:
			output_choices.append(False)
	# Outputs URL by default if no options are chosen.
	if False not in output_choices:
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

	hashtag_query = str(raw_input('Enter the hashtag you would like to search for: ')).lower()

	output_options = ['user','message','url','time','hashtags']
	output_choices = choose_outputs(output_options)

	log_file = start_record()

	stream.filter(track=[str('#'+hashtag_query)])




