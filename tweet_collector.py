from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys
from datetime import datetime
import os

# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""

filter_list = ['bitcoin', 'ethereum']


def handle_new_lines():
	"""handle new lines on different OS"""
	if os.name == 'nt':
		n_line = '\n'
	elif os.name == 'posix':
		n_line = '\r\n'
	else:
		print("Unkown OS.")
		n_line = '\n'
	return n_line


def create_stop_file():
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	f = open("deleteMeToStopTweetCollection.txt", "w")
	f.close()


new_line = handle_new_lines()
create_stop_file()


class listener(StreamListener):

	def on_data(self, data):
		if not os.path.isfile("deleteMeToStopTweetCollection.txt"):
			return False
		else:
			try:
				parsed_data = json.loads(data)
				tweet = parsed_data['text'].replace('\n', '')
				timestamp = str(datetime.now())
				print(timestamp)

				content_to_keep = '::::'.join([timestamp, tweet]) + new_line
				content_to_keep = content_to_keep.encode("utf-8").decode("utf-8")
				# '::::' is a delimiter that we don't expect to appear in tweet text
				with open('stream_data.txt', 'a', encoding="utf-8") as f:
					f.write(content_to_keep)
				return True
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print(
					str(e) + ' line: ' + str(exc_tb.tb_lineno) + ', ' +
					str(datetime.now()) + new_line)

				return True

	def on_error(self, status):
		print(status)


def run_streamer():
		auth = OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)
		twitterStream = Stream(auth, listener())
		twitterStream.filter(track=filter_list)

if __name__ == '__main__':
	run_streamer()
