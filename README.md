Twitter Stream Mining
=====================

Filters the live stream of tweets. Input the hashtag(s) you're interested in and see what the world is saying with them.

All matched tweets will be saved into a text file.




	The Twitter credentials file should contain these variables, named as such.
	Access Token : access_token
	Access Token Secret : access_token_secret
	Consumer Key : consumer_key
	Consumer Secret : consumer_secret


To Run
=====================

	// While in the directory
	virtualenv --no-site-packages .
	pip install -r requirements.txt
	python stream.py
	

goals
=====================

- [x] multiple hashtag searches
- [ ] seach by geographic area
- [ ] search for all tweets mentioning a user(s)
- [ ] add qualifiers like follower count or total tweet count
- [ ] populate database as opposed to writing to text file
- [ ] GUI



