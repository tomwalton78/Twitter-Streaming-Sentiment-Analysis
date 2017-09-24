import os
from matplotlib import pyplot as plt
import tuning_common_functions as tcf

ref_file_name = 'USDT_BTC_date,price.csv'
processed_tweets_file_name = 'bitcoin_tweets.txt'
pos_incr = 0.3
neg_incr = 0.7

current_path = str(os.path.dirname(os.path.realpath(__file__)))
ref_file_path = current_path + '/tuning_data/' + ref_file_name
sent_analysed_tweets_file_path = (
	current_path + '/Processed Tweets/' + processed_tweets_file_name)

with open(ref_file_path, 'r') as f:
	lines = f.readlines()
ref_timestamps, y1_data = tcf.extract_from_lines(lines, 'float')

with open(sent_analysed_tweets_file_path, 'r') as f:
	lines = f.readlines()
tweets_timestamps, tweets_sent = tcf.extract_from_lines(lines, 'string')

y1_data = tcf.normalise(y1_data)

current_y_data = []
y_score = 0
for i, j in enumerate(tweets_sent):
	if j == 'pos':
		y_score += pos_incr
	elif j == 'neg':
		y_score -= neg_incr
	else:
		print('ERROR READING SENT VALUE!')
		print(j)
	current_y_data.append(y_score)

y2_data = tcf.normalise(current_y_data)

nearest_min_ref_timestamps = tcf.to_nearest_time_mark(
	ref_timestamps, 'minute')
nearest_min_tweets_timestamps = tcf.to_nearest_time_mark(
	tweets_timestamps, 'minute')


nearest_min_ref_timestamps, y1_data = tcf.map_to_set(
	nearest_min_ref_timestamps, y1_data)
nearest_min_tweets_timestamps, y2_data = tcf.map_to_set(
	nearest_min_tweets_timestamps, y2_data)
nearest_min_ref_timestamps, y1_data, nearest_min_tweets_timestamps, y2_data = tcf.same_x_val_transform(
	nearest_min_ref_timestamps, y1_data, nearest_min_tweets_timestamps, y2_data)

similarity = tcf.get_similarity_score(
	nearest_min_ref_timestamps, y1_data, y2_data)
print('pos_incr: {}, neg_incr: {}, similarity: {}'.format(
	str(pos_incr), str(neg_incr), str(similarity)))

plt.plot_date(nearest_min_ref_timestamps, y1_data, label='reference_data')
plt.plot_date(
	nearest_min_tweets_timestamps, y2_data, label='tweets sent score')
plt.xlabel('Time')
plt.title(
	'Parameter tuning: pos_incr = {}, neg_incr = {}, dataset = {}'.format(
		str(pos_incr), str(neg_incr), processed_tweets_file_name))
plt.legend()
plt.show()
