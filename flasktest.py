from __future__ import absolute_import, print_function
import flask
import time
import re
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
consumer_key="*********"
consumer_secret="*********"
access_token="*********-*********"
access_token_secret="*********"
text = []

app = flask.Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"
@app.route("/greet/<name>")
def greet(name):
	return "Hello, %s!" %name

@app.route("/tweets/<hashtag>")
def tweets(hashtag):
	class StdOutListener(StreamListener):
	    def __init__(self, time_limit=15):
	        self.start_time = time.time()
	        #print(self.start_time)
	        self.limit = time_limit
	        #print(self.limit)

	    def on_data(self, data):
	        if (time.time() - self.start_time) < self.limit:
	            #print(data)
	            #print("sup")
	            text.append(data)
	            return True
	        else:
	            return False

	    def on_error(self, status):
	        print(status)
	        #print("hey")

	print ("test")
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = Stream(auth, l)
	search = "#" + hashtag
	stream.filter(track=[search])
	#print(text)
	count = 0
	located_tweets = []
	for tweet in text:
	    if ("\"bounding_box\"") in tweet:
	        count+=1
	        located_tweets.append(tweet)

	hold = ""
	x1, y1 = 0, 0
	coordinates = []
	for chunk in located_tweets:
	    start = re.search("\[\[\[", chunk).start()
	    #print(start)
	    end = re.search("\]\]\]", chunk).start()
	    #print(end)
	    for i in range (start+2, end+1):
	        hold = hold + chunk[i]
	    hold = re.sub(r'\[','',hold)
	    hold = re.sub(r'\]','',hold)
	    #print(hold)
	    
	    iter = re.finditer(r"\,", hold)
	    indices = [m.start(0) for m in iter]
	    hold = hold[:indices[1]]
	    #print(hold)
	    x1= float(hold[:indices[0]])
	    y1= float(hold[indices[0]+1:])
	    
	    #print(x1,y1)
	    coordinates.append((x1,y1))
	    hold = ""

	return str(coordinates)

if __name__ == '__main__':
	app.run()
