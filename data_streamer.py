from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys
from datetime import datetime
import nlp_model_v3 as text_sent
import subprocess

# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""

filter_word = 'bitcoin'


class listener(StreamListener):

	def on_data(self, data):
		try:
			parsed_data = json.loads(data)
			tweet = parsed_data['text']
			timestamp = str(datetime.now())
			sent, conf = text_sent.sentiment(tweet)
			print(timestamp + '\n')

			if conf * 100 >= 80:
				with open('twitter_out.txt', 'a') as g:
					g.write(', '.join([timestamp, sent]))
					g.write('\n')

			return True
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print(
				str(e) + ' line: ' + str(exc_tb.tb_lineno) + ', ' +
				str(datetime.now()) + '\n')

			return True

	def on_error(self, status):
		print(status)


def run_streamer():
		auth = OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)
		twitterStream = Stream(auth, listener())
		twitterStream.filter(track=[filter_word])

if __name__ == '__main__':
	with open('twitter_out.txt', 'w') as w:
		w.write(filter_word)
		w.write('\n')
	p = subprocess.Popen(
		[sys.executable, 'sent_grapher_live.py'], stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT)
	run_streamer()
