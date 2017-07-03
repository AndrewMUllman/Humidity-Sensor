import pandas as pd
from pandas import Series, DataFrame
from matplotlib import pyplot as plt
from pandas.tools.plotting import table


def plotter(title, data):

	"This function plots the x-data 'Elapsed Time' and y-data Reflection(Percent reflection) \
	in a dataframe == data. Give the figure a title with the string 'title'"
    
	#extract the data from the dataframe 'data'
	x = data['Elapsed Time']
	y = data['Reflection(Percent reflection)']
    
	#set up the axis subplot in the figure
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(x, y, color ='b')
    
	#customizing the figure 
	ax.tick_params(axis='both', labelsize=16, length = 12, width = 1)
	ax.tick_params(axis = 'both', which = 'minor', length = 6, width = 1)
	ax.set_title(title, fontsize = 18, fontname = 'Arial')
	ax.set_xlabel("Time (s)", fontname = 'Arial', fontsize = 18)
	ax.set_ylabel("%R at 525 nm", fontsize = 18, fontname = 'Arial')
	plt.minorticks_on()
	plt.xticks(fontname = 'Arial', fontsize = 18)
	plt.yticks(fontname = 'Arial', fontsize = 18)
	plt.tight_layout()
	#show the plot
	plt.show()

def growth_extract(dataframe, start, length, delta, n):
	'''This function extracts the rise portion of the data(dataframe), starting from time == 'start', with a \
	lenght == 'lenght' and period == delta. n is a factor for naming the keys of the dictionary. Returns a \
	a dictionary of dataframes with a just the rise portion of the data.'''
	
	NewDataFrameNames = [str(_) + '% RH' for _ in range(10, n*10, 10)]+['10% RH_repeat']
	DFD = {elem : pd.DataFrame for elem in NewDataFrameNames}
	for key in DFD.keys():
		DFD[key] = dataframe[(dataframe['Elapsed Time']>=start) & (dataframe['Elapsed Time']<=(start+length))]
		start += delta
	return DFD
             

def normalize(datadict):
    '''Takes a dictionary of dataframes with x axis in seconds and normalizes them to all start \ 
    at time == 0. Returns a dictionary of normalized dataframes. Keys are the same as the oringinal \
    dictionary of dataframes.'''
	
    #set x-axis with normalized value
    key_list = list(datadict.keys())
    # a list of the first x value in the 'Elapsed Time' Column for each dataframe in 
    # the dataframe dictionary, datadict
    normalized_starts = [datadict[key].iloc[0,1] for key in key_list]
    x_normvalues = zip(key_list, normalized_starts)
    x_list = [datadict[x]['Elapsed Time'] - y for x,y in x_normvalues]
    
    # set y data with list of Elapsed Time from dataframedict
    y_list = [y_data['Reflection(Percent reflection)'] for y_data in datadict.values()]
    data = zip(x_list, y_list)
    newDFL = [pd.concat([x,y], axis =1) for x,y in data]

    #zip up keys and the normalized data list
    key_DF = zip(datadict.keys(), newDFL)
    normalized_DFD = {x: y for x,y in key_DF}
    return normalized_DFD

def combined_plotter(datadict, title):
	
    #make a single axes in a figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    #iterate through dataframe dictionary to get the desired data and labeling it
    for key in datadict.keys():
	    ax.plot(datadict[key]['Elapsed Time'], datadict[key]['Reflection(Percent reflection)'], label= key)
        
    
    #customizing the figure 
    ax.set_xlim(-10, 310)
    ax.tick_params(axis='both', labelsize=16, length = 12, width = 1)
    ax.tick_params(axis = 'both', which = 'minor', length = 6, width = 1)
    ax.set_title(title, fontsize = 18, fontname = 'Arial')
    ax.set_xlabel("Time (s)", fontname = 'Arial', fontsize = 18)
    ax.set_ylabel("%R at 525 nm",fontsize = 18, fontname = 'Arial')
    plt.minorticks_on()
    plt.xticks(fontname = 'Arial', fontsize = 18)
    plt.yticks(fontname = 'Arial', fontsize = 18)
    plt.legend(loc='best')
    #still need to change the font of the legend to Arial
    plt.tight_layout()
	#show the plot
    plt.show()
        
def halfsat_valueandtime(dataframedict):
    # set y data with list of Elapsed Time from dataframedict
    y_list = [df['Reflection(Percent reflection)'] for df in dataframedict.values()]

    # create a list of all the half saturation points for all calculate the 
    half_sat  = [(y[-300:].mean() + float(y.values[0]))/2 for y in y_list]
    
    
	# zip together keys and half sat list to put into a new dictionary
    blah = zip(dataframedict.keys(), half_sat)
    half_sat_dict = {x:y for x,y in blah}
    

    # creating a list of the seven closest 
    list_of_closevalues = [dataframedict[key].iloc[(dataframedict[key]['Reflection(Percent reflection)']-half_sat_dict[key]).abs().argsort()[:7]] for key in dataframedict.keys()]
    
    
    half_sat_time = [list_of_closevalues[x]['Elapsed Time'].mean() for x in range(len(list_of_closevalues))]
   
    half_sat_time_std = [list_of_closevalues[x]['Elapsed Time'].std() for x in range(len(list_of_closevalues))]

    results = DataFrame({'Half Saturation Value (%R)': half_sat, 'Half Saturation Time (s)': half_sat_time, 'Half Saturation Time Std (s)': half_sat_time_std}, columns = ['Half Saturation Value (%R)', 'Half Saturation Time (s)', 'Half Saturation Time Std (s)'],index = list(dataframedict.keys()))
    return results

def maketable(df):
	fig, ax = plt.subplots(figsize=(12, 2)) # set size frame
	ax.xaxis.set_visible(False)  # hide the x axis
	ax.yaxis.set_visible(False)  # hide the y axis
	ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
	tabla = table(ax, df, loc='upper right', colWidths=[0.17]*len(df.columns))  # where df is your data frame
	tabla.auto_set_font_size(False) # Activate set fontsize manually
	tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
	tabla.scale(1.2, 1.2) # change size table
	#plt.savefig('table.png', transparent=True)
	plt.show()
	plt.tight_layout()
	#plt.savefig('table.png', transparent=True)


Location = 'Stepping from 10-20-30-40-50-60-10 RH 7 min on 15 min off.TimeSeries'
df = pd.read_csv(Location, sep = '\t', header = 4)
df.info()
df.head()

plotter('Full Data', df)
DFD = growth_extract(df, 120, 420, 1920, 7)
normalizedDFD = normalize(DFD)
combined_plotter(normalizedDFD, 'Normalized Rise Data')
results = halfsat_valueandtime(normalizedDFD)
print(results)

maketable(results)
