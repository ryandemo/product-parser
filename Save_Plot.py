import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
def save_plot(word_to_freq_apple, word_to_freq_google):
	apple_labels = word_to_freq_apple.keys()
	google_labels = word_to_freq_google.keys()

	apple_values = word_to_freq_apple.values()
	google_values = word_to_freq_google.values()

	apple_indexes = np.arange(len(apple_values))
	google_indexes = np.arange(len(google_values))
	
	bar_width = .35
	
	fig = plt.figure()

	fig.add_subplot(1, 2, 1)
	plt.bar(apple_indexes, apple_values)
	plt.xticks(apple_indexes, apple_labels)
	plt.title("Apple App Store")

	fig.add_subplot(1, 2, 2)
	plt.bar(google_indexes, google_values)
	plt.xticks(google_indexes, google_labels)
	plt.title("Google Play Store")
	plt.savefig("./assets/bar_graph")
save_plot({"potato":10, "apple":13, "Zucc":5}, {"zucchini":10, "orange":13, "trump":5})

