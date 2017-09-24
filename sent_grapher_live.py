import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
pos_incr = 0.3
neg_incr = 0.7


def animate(i):
	global filter_word
	data_in = open("twitter_out.txt", "r").read()
	lines = data_in.split('\n')
	filter_word = lines[0]
	x_data, y_data = [], []
	y = 0

	# for l in lines[-200:]:
	for l in lines[1:-1]:
		split_line = l.split(',')
		datetimestamp = datetime.strptime(split_line[0], "%Y-%m-%d %H:%M:%S.%f")
		sentiment = split_line[1].replace(' ', '').replace('\n', '')
		if sentiment == 'pos':
			y += pos_incr
		elif sentiment == 'neg':
			y -= neg_incr
		else:
			print("ERROR READING LINE--------------------------------------------------------------------------------------------------------------------------------------")

		x_data.append(datetimestamp)
		y_data.append(y)

	ax1.clear()
	plt.xlabel('Time')
	plt.ylabel('Sentiment')
	plt.title(
		"Live twitter sentiment analysis on: '" + filter_word + "'")
	ax1.plot_date(x_data, y_data)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
