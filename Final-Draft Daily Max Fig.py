#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''This is a custom graphics program for visualizing 
   temperature data at a number of monitoring locations. 
   This program is designed to run as a script in Microsoft 
   Power BI. The input is a CSV that contains 5-minute interval 
   temperature data and the locations that the data was collected.
   The output is a figure showing the daily temperature maximum 
   at each of the monitoring locations.'''


# In[1]:


import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

#convert to datetime
dataset['date'] = pd.to_datetime(dataset['date'], format = '%Y-%m-%d')

#subset by location
dconf = dataset[dataset['Location']== 'Downstream Confluence']
uptrib = dataset[dataset['Location'] == 'Upstream Tributary']
ppg_out = dataset[dataset['Location'] == 'PPG Outfall']
ppg_up = dataset[dataset['Location'] == 'PPG Outfall Upstream']
uptrib_up = dataset[dataset['Location'] == 'Upstream Tributary, Upstream']

#create the subplot
fig = plt.figure(figsize=(12,8))
ax = plt.subplot(1,1,1)

#map the variables
ax.scatter(dconf['date'], dconf['Temp'], color = 'cyan', label ='Downstream Confluence' )
ax.scatter(uptrib['date'], uptrib['Temp'], color = 'purple', label ='Upstream Tributary')
ax.scatter(ppg_out['date'], ppg_out['Temp'], color = 'blue', label ='PPG Outfall')
ax.scatter(ppg_up['date'], ppg_up['Temp'], color = 'orange', label ='PPG Outfall Upstream')
ax.scatter(uptrib_up['date'], uptrib_up['Temp'], color = 'magenta', label ='Upstream Tributary, Upstream')
ax.plot(dataset['date'], dataset['daily_max_limit'], label ='Daily Temperature Maxiumum')

#set x-axis to preferred date format
fmt_half_year = mdates.MonthLocator(interval=6)
ax.xaxis.set_major_locator(fmt_half_year)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

#draw legend
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol = 6)

#make axes labels
plt.xlabel('Date', fontsize = 14)
plt.ylabel('Temperature, °F', fontsize= 14)
plt.title('Daily Maximum Temperature', fontsize =14)

plt.show()

