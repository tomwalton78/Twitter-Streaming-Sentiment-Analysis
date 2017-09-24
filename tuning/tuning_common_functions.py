from datetime import datetime
from math import fabs


def extract_from_lines(lines, value_type):
	length = len(lines)
	timestamps = [0] * length
	values = [0] * length
	for i, j in enumerate(lines):
		split_line = j.split(',')
		try:
			timestamp = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S.%f")
		except(ValueError):
			timestamp = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S")
		timestamps[i] = timestamp
		if value_type == 'float':
			values[i] = float(split_line[1].replace('\n', ''))
		elif value_type == 'string':
			values[i] = split_line[1].replace('\n', '')
		else:
			print('please enter a valid value_type')
	return timestamps, values


def normalise(y_vals):
	"""Normalises input values between -1 and 1"""
	lower_bound, upper_bound = min(y_vals), max(y_vals)
	if lower_bound < 0:
		y_vals = [y - lower_bound for y in y_vals]
		lower_bound, upper_bound = min(y_vals), max(y_vals)
	new_y_vals = []
	for y_val in y_vals:
		fraction = ((y_val - lower_bound) / (upper_bound - lower_bound))
		new_y_val = (fraction * 2) - 1
		new_y_vals.append(new_y_val)
	return new_y_vals


def to_nearest_time_mark(timestamps, time_mark):
	if time_mark == 'minute':
		new_timestamps = [x.replace(
			second=0, microsecond=0) for x in timestamps]
	elif time_mark == 'hour':
		new_timestamps = [x.replace(
			minute=0, second=0, microsecond=0) for x in timestamps]
	elif time_mark == 'day':
		new_timestamps = [x.replace(
			hour=0, minute=0, second=0, microsecond=0) for x in timestamps]
	else:
		print('error, unknown time_mark value')
	return new_timestamps


def avg_of_list(list_in):
	return sum(list_in) / float(len(list_in))


def map_to_set(timestamps, values):
	set_of_timestamps = set(timestamps)
	# Group values that correspond to same (rounded) timestamp
	grouped_timestamps = {}
	for i, timestamp in enumerate(timestamps):
		if str(timestamp) not in list(grouped_timestamps.keys()):
			grouped_timestamps[str(timestamp)] = [values[i]]
		else:
			grouped_timestamps[str(timestamp)].append(values[i])

	# Average values for each unique timestamp
	new_values = []
	for unique_timestamp in set_of_timestamps:
		new_values.append(
			avg_of_list(grouped_timestamps[str(unique_timestamp)]))
	return set_of_timestamps, new_values


def common_only(common_x_list, x_list, y_list):
	as_dict = {}
	for index, val in enumerate(x_list):
		if val in common_x_list:
			as_dict[val] = y_list[index]
	return as_dict


def same_x_val_transform(x1, y1, x2, y2):
	common_x_vals = [x for x in x1 if x in x2]
	dict_1 = common_only(common_x_vals, x1, y1)
	dict_2 = common_only(common_x_vals, x2, y2)
	x1_, y1_, x2_, y2_ = [], [], [], []
	for key in dict_1.keys():
		x1_.append(key)
		y1_.append(dict_1[key])
		x2_.append(key)
		y2_.append(dict_2[key])
	return x1_, y1_, x2_, y2_


def get_similarity_score(common_x_vals, y1_vals, y2_vals):
	"""Computes similarity between 2 datasets based on avg difference between y
	data points"""
	delta_list = []
	for i, j in enumerate(common_x_vals):
		delta_list.append(fabs(y2_vals[i] - y1_vals[i]))
	avg_delta = sum(delta_list) / float(len(delta_list))
	return avg_delta


def trim_dict(dict_to_trim, trim_val):
	trimmed_dict = {}
	for key in dict_to_trim.keys():
		if dict_to_trim[key] <= trim_val:
			trimmed_dict[key] = dict_to_trim[key]
	return trimmed_dict
