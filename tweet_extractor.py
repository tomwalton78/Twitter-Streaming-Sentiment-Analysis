import nlp_model_v3 as text_sent

filter_words = ['bitcoin', 'ethereum']


with open('stream_data.txt', 'rb+') as f:
	lines = f.readlines()
line_length = float(len(lines))
with open('filter_words_sent.txt', 'w') as g:
	i = 0
	for line in lines:
		line_conv = str(line).replace(
			'b', '').replace(
			'"', '').replace(
			"'", "").replace(
			'\n', ' ') + '\n'

		for word in filter_words:
			if word.lower() in line_conv.lower():
				split_line = line_conv.split('::::')
				timestamp = split_line[0]
				sent, conf = text_sent.sentiment(split_line[1])
				if float(conf) >= 0.8:
					g.write('::::'.join([word, timestamp, sent]))
					g.write('\n')

		if i % 1000 == 0:
			print(round((i / line_length) * 100, 2), ' %%')
		i += 1


with open('filter_words_sent.txt', 'r') as h:
	lines = h.readlines()
line_length = float(len(lines))

for word in filter_words:
	with open(word + '_tweets.txt', 'w') as e:
		i = 0
		for line in lines:
			split_line = line.replace('\n', '').split('::::')
			if word == split_line[0]:
				e.write(','.join(split_line[1:]))
				e.write('\n')

			if i % 100000 == 0:
				print((i / line_length) * 100, ' %%')
			i += 1
