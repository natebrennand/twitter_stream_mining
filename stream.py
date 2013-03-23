
import tweepy.streaming
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import atexit
import py_tweet
import sqlite3


class StdOutListener( tweepy.streaming.StreamListener):

	def on_data(self, data):
		tweet_match = py_tweet.tweet(data)

		if hashtag_filter(tweet_match.hashtag_list):
			print getattr(tweet_match,'time')

			sql_insert = """
			INSERT or IGNORE
			INTO {} VALUES (?,?,?,?,?);
			""".format( db_name )
			db.cursor().execute( sql_insert , tweet_match.get_tuple() )
			db.commit()

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

def start_record(db_name):
	sql_init = """
	CREATE TABLE if NOT EXISTS {} (
		url TEXT,
		user TEXT,
		message TEXT,
		hashtags TEXT,
		time TEXT,
		PRIMARY KEY (url)
	);
	""".format(db_name)
	db = sqlite3.connect( 'logs/data.db' )
	atexit.register( clean_up, db )

	cursor = db.cursor()
	cursor.execute( sql_init )
	return db


# Closes database at the end of logging
def clean_up( db ):
	db.close()

# POSSIBLLY NEEDS TO BE ALTERED FOR VIEWING OF TWEETS AFTER LOGGING
def choose_outputs():
	output_options = ['user','message','url','time','hashtags']
	output_choices = []

	print "Enter Y or N for all of the following output options."
	for choice in output_options:
		choice = str( raw_input(choice.ljust(12))).upper()
		if 'Y' in choice:
			output_choices.append(True)
		else:
			output_choices.append(False	)

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

	query = str(raw_input('Enter the hashtags you would like to search for '
				+ 'separated by spaces: ')).lower()
	hashtag_queries = query.split(' ')

	search_type = str(
		raw_input('Should returned tweets include all or >=1 hashtags? Enter '+
		'"all" or "one"')).lower()

	if 'all' in search_type:
		hashtag_filter = hashtag_AND_filter
	else:
		hashtag_filter = hashtag_OR_filter

	db_name = ''
	for tag in hashtag_queries:
		db_name += tag + '_'
	print db_name
	db = start_record(db_name)

	stream.filter( track = hashtag_queries )




