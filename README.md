# twitter-streaming-sentiment-analysis
Python scripts for performing live sentiment analysis on tweets from twitter on a certain topic.

Instructions for use:
1. Install relevant modules: tweepy (from: https://github.com/tweepy/tweepy), matplotlib, nltk, pandas, sklearn
2. It is recommended to use these classified tweets as the training data (http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/), however you may need to only use a selection, due to intensive ram usage. Place into the 'training_data' folder.
3. Now run nlp_model_v3 to train the data, ensuring file_name is pointed to correct file in training_data folder, light_mode is False. Adjust percent_train and classifiers_to_use as necessary.
4. The training should take a while, however once it is done it is recommended to set light_mode to False, as this speeds up the module when running on pre-trained classifiers.
5. Now run the data_streamer.py file, entering in your key, secret and token values and specifiy the filter_word (topic to collect tweets on).

If you want to fine tune the pos_incr and neg_incr values in the sent_grapher_live.py file, in order to get the most accurate/relevant graph output, please use the tools in the 'tuning' folder:
1. The data_compare.py file will run over 1 weeks worth of data on either 'bitcoin' or 'ethereum' topics and try to match the results of the sentiment analysis to the pricing data collected over the same period, varying the pos_incr and neg_incr parameters, with the values being averaged to the nearest miute, hour or day, as specified by the time_mark parameter.
2. The sentiment analysis was found to have a positive bias, and so pos_incr was set to 0.3, neg_incr to 0.7 in order to account for this. However, further testing may suggest different parameters.
3. If you wish to collect your own tweets, you may use the tweet_collector.py and tweet_extractor.py scripts.
