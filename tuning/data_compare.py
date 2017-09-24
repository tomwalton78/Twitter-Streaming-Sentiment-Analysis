import os
from matplotlib import pyplot as plt
import tuning_common_functions as tcf

ref_file_name = 'USDT_BTC_date,price.csv'
processed_tweets_file_name = 'bitcoin_tweets.txt'
time_mark = 'hour'  # valid values are 'minute', 'hour', 'day'

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

y2_datasets = {}
ratio_list = []
for l in range(1, 11):
	print(l)
	for m in range(1, 11):
		ratio = m / float(l)
		if ratio not in ratio_list:
			ratio_list.append(ratio)
			current_y_data = []
			y_score = 0
			pos_incr, neg_incr = l / 10.0, m / 10.0
			for i, j in enumerate(tweets_sent):
				if j == 'pos':
					y_score += pos_incr
				elif j == 'neg':
					y_score -= neg_incr
				else:
					print('ERROR READING SENT VALUE!')
					print(j)
				current_y_data.append(y_score)

			current_y_data = tcf.normalise(current_y_data)
			key_string = 'pos_incr: {}, neg_incr: {}'.format(
				str(pos_incr), str(neg_incr))
			y2_datasets[key_string] = current_y_data


nearest_min_ref_timestamps = tcf.to_nearest_time_mark(
	ref_timestamps, time_mark)
nearest_min_tweets_timestamps = tcf.to_nearest_time_mark(
	tweets_timestamps, time_mark)


similarity_dict = {}
key_list = list(y2_datasets.keys())
y1_data_save = y1_data
nearest_min_ref_timestamps_save = nearest_min_ref_timestamps
nearest_min_tweets_timestamps_save = nearest_min_tweets_timestamps
for key in key_list:
	y2_data = y2_datasets[key]
	nearest_min_ref_timestamps, y1_data = tcf.map_to_set(
		nearest_min_ref_timestamps_save, y1_data_save)
	nearest_min_tweets_timestamps, y2_data = tcf.map_to_set(
		nearest_min_tweets_timestamps_save, y2_data)
	nearest_min_ref_timestamps, y1_data, nearest_min_tweets_timestamps, y2_data = tcf.same_x_val_transform(
		nearest_min_ref_timestamps, y1_data, nearest_min_tweets_timestamps, y2_data)

	similarity_dict[key] = tcf.get_similarity_score(
		nearest_min_ref_timestamps, y1_data, y2_data)
	print(key)
	y2_datasets[key] = y2_data

similarity_dict = tcf.trim_dict(similarity_dict, 0.6)
print(similarity_dict)

# Plotting graph for parameters with lowest similarity score
best_val = min(list(similarity_dict.values()))
for key in similarity_dict.keys():
	if similarity_dict[key] == best_val:
		best_key = key
		break
y2_data = y2_datasets[best_key]
print(best_key)
print(len(nearest_min_tweets_timestamps))
print(len(y2_data))
plt.plot_date(nearest_min_ref_timestamps, y1_data, label='reference_data')
plt.plot_date(
	nearest_min_tweets_timestamps, y2_data, label='tweets sent score')
plt.xlabel('Time')
plt.title('Parameter tuning comparison (visual)')
plt.legend()
plt.show()
