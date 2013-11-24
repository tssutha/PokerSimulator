# This file contains source code generating various 
# plot for poker simulator 
# Libraries used : MatPlotLib, Numpy, SciPy, PyLab
#
#
#


import numpy.numarray as na
import numpy as np
from pylab import *
import matplotlib.pyplot as plt

# P - One Pair , TP - Two Pair, 3K - Three of a Kind
# S - Straight, F - Flush, FH - Full House,
# 4K - Four of a Kind , SF - Straight Flush
# SNL - Sorry, No Luck :(


labels = ['P', 'TP','3K','S','F','FH','4K','SF']
#data   = [0.44977, 0.23749, 0.04880, 0.01980, 0.02981, 0.02570, 0.00156, 0.00020]
data = [0.42013, 0.04799, 0.02043, 0.00369, 0.00197, 0.00124, 0.00031,0.00003]
data_wiki = [0.4226, 0.0475, 0.02110, 0.0039, 0.00196, 0.001441, 0.00024, 0.000015]

colors  = ['magenta','darkblue','green','skyblue','pink','yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
error  = [0,0,0,0,0,0,0,0]
ytickmarks = [ 0,0.1,0.2,0.3,0.4,0.5]


def plot_bar_chart():
	"""
		Plot a Bar chart of probability of each rank 
		after 10000 rounds of shuffling 
	"""
	xlocations = na.array(range(len(data))) + 0.5
	width = 0.5
	bar(xlocations, data, yerr= error, width = width)
	yticks(ytickmarks)
	xticks(xlocations + width/2, labels)
	xlim(0, xlocations[-1]+width*2)
	title("Poker Hand Ranking Probability")
	gca().get_xaxis().tick_bottom()
	gca().get_yaxis().tick_left()

	show()
	
def log_10_product(x,pos):
	return True
	
def plot_pie_chart():
	"""
		Plot the Pie chart of probability of each rank after
		1000 rounds of shuffling 
	"""
	explode = (0,0.1,0,0,0,0,0,0,0) #only explode the 2nd slice 
	plt.pie(data, explode = explode, labels = labels, colors = colors,
			autopct = '%1.1f%%', shadow = True, startangle = 90)
	#set the aspect ratio to be equal so that pie is drawn as circle
	plt.axis('equal')
	plt.show()

def plot_line_chart():
	"""
		Read data from \t delimiter file and 
		plot number of time each ranking occur 
		during the 10000 time shuffling 
	"""
	sample = list(range(1,11))
	plotshape = ['ro', 'go', 'b^', 'ys','mo','c^','kx', 'b*' ]
	
	print sample
	data = np.genfromtxt('pokerdata.txt', delimiter=',')
	plt.axis([0,11,0,35000])
	plt.title('Poker Simulator, Rank Occurrence')
	plt.ylabel('Num of Times out 70000 poker hands')
	plt.xlabel('Simulation Number')
	for i in range(data.shape[1]):
		plt.plot(sample, data[:,i], plotshape[i], label=labels[i])
		
	plt.legend()
	plt.show()
	
	
def plot_bar_chat_compare():
	width = 0.35
	ind = np.arange(8)
	fig, ax = plt.subplots()
	rect1 = ax.bar(ind, data, width, color='y', yerr = error)
	rect2 = ax.bar(ind+width, data_wiki, width, color='g', yerr = error)
	#add some properties
	ax.set_ylabel('Probability')
	ax.set_title("Probability Histogram of Hand's rank")
	ax.set_xticks(ind + width)
	ax.set_xticklabels(tuple(labels))
	
	ax.legend((rect1[0], rect2[0]), ('Simulator', 'Theoretical'))
	plt.show()
	return True
	
		
	
if __name__ == '__main__':
	#plot_pie_chart()
	#plot_bar_chart()
	#plot_line_chart()
	plot_bar_chat_compare()
	



