#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''This is an automated graphics program
   for streamlining NAPL mobility analyses. 
   The inputs are a well data CSV files containing 
   the amount of NAPL pumped from a well, and 
   transmissivity data for that well. The outputs are 
   a series of report-ready graphics in JPEG format.


# In[2]:


import pandas as pd
from matplotlib import pyplot as plt 
import numpy as np


# In[3]:


#Import data 
df = pd.read_csv('RW4-2_Data.csv')#Put RW4-2 Data here 
df2 = pd.read_csv("NAPL_Pumped_Data.csv") #Put Merged RW4-2 and NAPL Pumped Data Here
df3 = pd.read_csv('trans_analysis.csv') #Put Transmissivity Data Here


# In[4]:


#Cell 3 - Create Figure 1

#create year column 
df['Year'] = pd.DatetimeIndex(df['Date']).year

#Create subset of the dataframe by year to produce the graphs
df2017 = df[df['Year'] == 2017]
df2018 = df[df['Year'] == 2018]
df2019 = df[df['Year'] == 2019]
df2020 = df[df['Year'] == 2020]
df2021 = df[df['Year'] == 2021]

#Make subplot - by year
fig = plt.figure(figsize = (30, 20))

#2017 Data
ax1 = plt.subplot(3, 2, 1)
plt.scatter(df2017['Date'], df2017['NAPL Thickness'])
plt.plot(df2017['Date'], df2017['NAPL Thickness'])
plt.title('2017', fontsize = 16)
plt.xlabel('Date', fontsize = 14)
plt.xticks(rotation = 90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.ylabel('NAPL Thickness', fontsize = 14)
plt.ylim([6, 18])

#2018 Data
ax2 = plt.subplot(3, 2, 2)
plt.scatter(df2018['Date'], df2018['NAPL Thickness'])
plt.plot(df2018['Date'], df2018['NAPL Thickness'])
plt.title('2018', fontsize = 16)
plt.xlabel('Date', fontsize = 14)
plt.xticks(rotation = 90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.ylabel('NAPL Thickness', fontsize = 14)
plt.ylim([6, 18])
plt.xticks(np.arange(0, len(df2018['Date'])+1, 5))

#2019 Data
ax3 = plt.subplot(3, 2, 3)
plt.scatter(df2019['Date'], df2019['NAPL Thickness'])
plt.plot(df2019['Date'], df2019['NAPL Thickness'])
plt.title('2019', fontsize = 16)
plt.xlabel('Date', fontsize = 14)
plt.xticks(rotation = 90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.ylabel('NAPL Thickness', fontsize = 14)
plt.ylim([6, 18])
plt.subplots_adjust(hspace = 0.8)
plt.xticks(np.arange(0, len(df2019['Date'])+1, 5))

#2020 Data
ax4 = plt.subplot(3, 2, 4)
plt.scatter(df2020['Date'], df2020['NAPL Thickness'])
plt.plot(df2020['Date'], df2020['NAPL Thickness'])
plt.title('2020', fontsize = 16)
plt.xlabel('Date', fontsize = 14)
plt.xticks(rotation = 90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.ylabel('NAPL Thickness', fontsize = 14)
plt.ylim([6, 18])
plt.xticks(np.arange(0, len(df2020['Date'])+1, 5))

#2021 Data
ax5 = plt.subplot(3, 2, 5)
plt.scatter(df2021['Date'], df2021['NAPL Thickness'])
plt.plot(df2021['Date'], df2021['NAPL Thickness'])
plt.title('2021', fontsize = 16)
plt.xlabel('Date', fontsize = 14)
plt.xticks(rotation = 90, fontsize = 14)
plt.yticks(fontsize = 14)
plt.ylabel('NAPL Thickness', fontsize = 14)
plt.ylim([6, 18])
plt.subplots_adjust(hspace = 0.8)
plt.xticks(np.arange(0, len(df2021['Date'])+1, 5))

#Save figure to file
plt.savefig('figure-1_NAPL-Thickness_subplot.jpeg')


# In[5]:


#Cell 4 - Create Figure 2

#Make NAPL Thickness and DTW Figure WRT Date

#Create figure and set size
fig2 = plt.figure(figsize = (15, 4))

#Create Axes objects
ax6 = plt.subplot(1, 1, 1)
ax7 = ax6.twinx()

#Plot NAPL Thickness Data - Left Vertical Axis
ax6.scatter(df['Date'], df['NAPL Thickness'])
ax6.plot(df['Date'], df['NAPL Thickness'])

#Plot DTW Data - Right Vertical Axis
ax7.scatter(df['Date'], df['DTW'], color = 'red')
ax7.plot(df['Date'], df['DTW'], color = 'red')

#Set Y Axis Labels
ax6.set_ylabel('NAPL Thickness', fontsize = 14)
ax7.set_ylabel('DTW', fontsize = 14)

#Adjust the tick locations for date on the x axis
ax6.set_xticks(np.arange(0, len(df['Date'])+1, 10))
ax7.set_xticks(np.arange(0, len(df['Date'])+1, 10))

#Adjust x axis tick label orientation and size
for tick in ax6.get_xticklabels():
    tick.set_rotation(90)
    tick.set_fontsize(14)
for tick in ax7.get_xticklabels():
    tick.set_rotation(90)
    tick.set_fontsize(14)

#Set Font size for y axis ticks
for tick in ax6.get_yticklabels():
    tick.set_fontsize(14)
for tick in ax7.get_yticklabels():
    tick.set_fontsize(14)
    
#Label x axis 
ax6.set_xlabel('Date', fontsize = 14)

#Set extents for the x axis
ax6.set_ylim([0, 18])
ax7.set_ylim([0,18])

#Save figure to file
plt.savefig('figure-2_NAPL-Thickness_DTW.jpeg')


# In[4]:


#Cell 5 - Create Figure 3 
#Cumulative Gallons Pumped figure

#delete empty date records to produce graph
df2 = df2.dropna(subset = ['Date'])

#create figure and axes objects
fig3 = plt.figure(figsize = (10,8))
axa = plt.subplot(1,1,1)

#Plot points and draw line
plt.scatter(df2['Date'], df2['cum_pumped'])
plt.plot(df2['Date'], df2['cum_pumped'])

#Erase the hashtag on code below to see the Daily NAPL pumped on the figure.
#plt.plot(df2['Date'], df2['NAPL_PUMPED'], color ='red')

#plt.legend(['Cumulative NAPL Pumped', 'Daily NAPL Pumped'])

#Set axes labels
plt.xlabel('Date', fontsize= 14)
plt.ylabel('Cumulative NAPL Pumped (gal)', fontsize = 14)

#generate a regular interval of x-tick labels
axa.set_xticks(np.arange(0, len(df2['Date'])+1, 20))

#edit x and y tick label size and rotation
for tick in axa.get_xticklabels():
    tick.set_rotation(90)
    tick.set_fontsize(14)
for tick in axa.get_yticklabels():
    tick.set_fontsize(14)

#Save figure to file
plt.savefig('figure-3_Cumulative-NAPL-Pumped.jpeg')


# In[7]:


#Cell 6 - Create Figure 4
#Create Cumulative Napl pumped Vs Transmissivity Figure 

#create figure and axes objects
fig4 = plt.figure(figsize=(10, 5))
ax10 = plt.subplot(1,1,1)

#Transmissivity Data
ax10.scatter(df3['Cum_gal_pumped'], df3['AVG_TRANS'])

#ITRC line
ax10.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*0)+0.8, 'g--')
plt.annotate("IRTC Trans. 0.8 ft^2/day", (900, 1.2), fontsize=12, color ='green')

#Set x and y axes labels
ax10.set_xlabel('Cumulative Gallons Pumped', fontsize =14 )
ax10.set_ylabel("Average LNAPL Transmissivity (ft^2/day)", fontsize =14)

#Save figure to file
plt.savefig('figure-4_Avg-Trans_Cumulative-NAPL-Pumped.jpeg')


# In[6]:


'''Define slopes and intercepts for the Decline Curve Figure'''

#Define x values
x = df3['Cum_gal_pumped'].dropna().array

#Theim Transmissivity
df_thiem = df3[['Cum_gal_pumped', 'Theim_TRANS']].dropna(subset=['Theim_TRANS'],how='all')
x_thiem = df_thiem['Cum_gal_pumped'].array
y_thiem = df3['Theim_TRANS'].dropna().array
m_thiem, b_thiem = np.polyfit(x_thiem, y_thiem, 1)

#B&R Transmissivity
df_BR = df3[['Cum_gal_pumped', 'BR_TRANS']].dropna(subset=['BR_TRANS'],how='all')
x_BR = df_BR['Cum_gal_pumped'].array
y_BR = df_BR['BR_TRANS'].dropna().array
m_BR, b_BR = np.polyfit(x_BR, y_BR, 1)

#C&J Transmissivity 
df_CJ = df3[['Cum_gal_pumped', 'CJ_TRANS']].dropna(subset=['CJ_TRANS'],how='all')
x_CJ = df_CJ['Cum_gal_pumped'].array
y_CJ = df3['CJ_TRANS'].dropna().array
m_CJ, b_CJ = np.polyfit(x_CJ, y_CJ, 1)

#Cooper Transmissivity
df_cooper = df3[['Cum_gal_pumped', 'COOPER_TRANS']].dropna(subset=['COOPER_TRANS'],how='all')
x_cooper = df_cooper['Cum_gal_pumped'].array
y_cooper = df3['COOPER_TRANS'].dropna().array
m_cooper, b_cooper = np.polyfit(x_cooper, y_cooper, 1)


# In[8]:


#Cell 8 - Create Figure 5
#Create Decline Curve Figure 

#create figure and axes objects
fig5 = plt.figure(figsize=(18, 6))
ax11 = plt.subplot(1,1,1)

#Transmissivity Data
ax11.scatter(df3['Cum_gal_pumped'], df3['Theim_TRANS'], color ='blue') 
ax11.scatter(df3['Cum_gal_pumped'], df3['BR_TRANS'], color = 'red')
ax11.scatter(df3['Cum_gal_pumped'], df3['CJ_TRANS'], color = 'green')
ax11.scatter(df3['Cum_gal_pumped'], df3['COOPER_TRANS'], color ='purple')

legend1 = ax11.legend(["Transmissivity (Theim- ft^2/day)","Transmissivity (B&R- ft^2/day)", "Transmissivity (C&J- ft^2/day)",
            "Transmissivity (Cooper- ft^2/day)"], ncol =4, loc='lower center', fontsize= 12, bbox_to_anchor=(0., 1.02, 1., .102),
           mode="expand", borderaxespad=0.)
plt.gca().add_artist(legend1)

#Plot Lines of Best Fit
ax11.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*m_thiem) +b_thiem, 'g:', color='blue') #Thiem
ax11.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*m_BR) +b_BR, 'g:', color='red') #B&R
ax11.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*m_CJ) +b_CJ, 'g:', color='green')#C&J
ax11.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*m_cooper) +b_cooper, 'g:', color='purple') #Cooper
legend2 = ax11.legend(["Transmissivity (Theim- ft^2/day)","Transmissivity (B&R- ft^2/day)", "Transmissivity (C&J- ft^2/day)",
            "Transmissivity (Cooper- ft^2/day)"], ncol =4, loc='upper center', fontsize= 12 )
plt.gca().add_artist(legend2)

#ITRC line
ax11.plot(df3['Cum_gal_pumped'], (df3['Cum_gal_pumped']*0)+0.8, 'g--', color='black')
plt.annotate("IRTC Trans. 0.8 ft^2/day", (900, 0.9), fontsize=12)
             
#Set x and y axes labels
ax11.set_xlabel('Cumulative Gallons Pumped', fontsize =14 )
ax11.set_ylabel("LNAPL Transmissivity (ft^2/day)", fontsize =14)
ax11.set_xlim(0,6000)

#Set y axis format
ax11.set_yscale('log')
ax11.set_yticks([0.1, 1, 10, 100])

#Format axes tick labels
for tick in ax11.get_xticklabels():
    tick.set_fontsize(12)
for tick in ax11.get_yticklabels():
    tick.set_fontsize(12)

#Save figure to file
plt.savefig('figure-5_Decline-Curve.jpeg')


# In[ ]:




