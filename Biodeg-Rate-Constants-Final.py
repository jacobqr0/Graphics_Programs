#!/usr/bin/env python
# coding: utf-8

# In[ ]:


''' This program calculates the biodegredation constants 
    for contaminants of concern (COC) at a remedial action site
    with active vertical and horizontal airsparge systems. 
    The progam also generates time series figures to help
    estimate a time-to-clean up for the COC. The inputs are two
    CSV files. One CSV should list the well IDs for impacted
    locations and their distance from the airsparge systems. 
    The other CSV contains contaminant concentration data 
    for each of the well IDs in the analysis. There are two outputs.
    One is a table of rate constants and their goodness of fit 
    (r-squared) for each well. The second output is a PDF of the 
    contaminant concentration time series charts.'''


# In[1]:


'''import modules'''

import pandas as pd
from matplotlib import pyplot as plt 
import numpy as np
import datetime as datetime
import matplotlib.backends.backend_pdf


# In[2]:


'''define functions'''

'''define function to make days column in df'''

def column_days(df):
    
    #Make a list of the dates 
    df = df.sort_values(['Date'], ascending = True)
    dates = []
    for date in df['Date']:
        dates.append(date)
    
    
    #make the timedelta list for difference between dates
    subtract = df['Date'].min()
    days = []
    index_tracker = 0
    for date in dates:
        diff = (date - subtract)
        days.append(diff)
        subtract = dates[index_tracker]
        index_tracker = index_tracker + 1
    
    
    #create the dates dataframe
    data = {"Date": dates, "Days": days}
    dates_df = pd.DataFrame(data)
    
    
    #transform the days column from timedelta to number of days
    dates_df['Days'] = dates_df['Days'].dt.days
    
    
    #make the days_total list from dates_df
    days_min = dates_df['Days'].min()
    days_total =[]
    for days in dates_df['Days']:
        total = days + days_min
        days_total.append(total)
        days_min = total
    
    #drop the Days column
    dates_df = dates_df.drop(columns='Days')
        
    
    #add the days_total list to the dates_df 
    dates_df['days'] = days_total
    
    
    #merge the days_total to the df. 
    df_1 = pd.merge(df, dates_df, on='Date')
    
    
    return df_1


# In[3]:


'''define function to get C0 and add calculated Ln(C/C0) column '''

def get_C0_column(df):
    
    
    #find the CB concentration associated with day 0
    C0 = df.loc[df['days'] == 0]['REPORT_RESULT_VALUE'].values[0]
    
    
    #Calculate the Ln(C/C0) column in df_1
    df['Ln_conc_c0'] = np.log((df['REPORT_RESULT_VALUE']/C0))
    
    return df


# In[4]:


'''define a function to consolidate the concentration data'''

def consolidate(df):
    
    df= df[['LOC_NAME', 'Date', 'REPORT_RESULT_VALUE', 'REPORT_RESULT_UNIT', 'days', 'Ln_conc_c0']]
    
    df= df.rename(columns= {'LOC_NAME': 'Well_ID', 'REPORT_RESULT_VALUE': 'Chlorobenzene_Concentration', 
                            'REPORT_RESULT_UNIT': 'Concentration_Units', 'days':'Time_in_Days',})
    
    return df


# In[5]:


''' define r-squared function, r_sqd()'''

def r_sqd(df):
    corr_matrix = np.corrcoef(df['days'], df['Ln_conc_c0'])
    corr_xy = corr_matrix[0,1]
    rsqd = corr_xy**2
    return rsqd


# In[6]:


'''define slope and intercept function, solve()'''

def solve(df):
    x_days = df['days'].array
    y_conc = df['Ln_conc_c0'].array
    m, b = np.polyfit(x_days, y_conc, 1)
    return m, b


# In[7]:


'''define graphics function'''

def graph(df, well_id, airsparge_dist, m, b, r_sqd):
    
    
    #Create figure and axes objects
    fig = plt.figure(figsize=(8,6))
    ax1 = plt.subplot(1,1,1)
    
    
    #Make a scatter of the data
    ax1.scatter(df['days'], df['Ln_conc_c0'],
                 marker='D', color='blue')
    
    
    #Add trendline 
    ax1.plot(df['days'], (df['days']*m + b), color = 'black')

    
    #Label axes
    ax1.set_xlabel('Time (days)', fontsize=15)
    ax1.set_ylabel('$\mathrm{Ln(C/C_0)}$', fontsize =14)
    
    
    #Annotate the figure 
    if b <0:
        ax1.annotate("y = {0:.4f}x - {1:.4f}\n$R^{2}$ = {3:.4f}".format(m, np.absolute(b), 2, r_squared), xy=(0.4, 0.75),
                        xycoords='figure fraction',
                        xytext=(0.135,0.85), textcoords='offset points',fontsize =14,
                        color='black')
    else:
        ax1.annotate("y = {0:.4f}x + {1:.4f}\n$R^{2}$ = {3:.4f}".format(m, np.absolute(b), 2, r_squared), xy=(0.4, 0.75),
                        xycoords='figure fraction',
                        xytext=(0.135,0.85), textcoords='offset points',fontsize =14,
                        color='black')

    
    #Add title
    if airsparge_dist == 'Upgradient ':
        plt.title(well_id+' -- ' + 'Upgradient from the Airsparge Line', fontsize =18)
    elif airsparge_dist == 'Within System Area':
        plt.title(well_id+' -- ' + 'Within Airsparge System Area', fontsize =18)
    else:
        plt.title(well_id+' -- '+ str(airsparge_dist) + " ft downgradient from the Airsparge Line", fontsize =18)
        

    #Adjust x axis tick label orientation and size
    for tick in ax1.get_xticklabels():
        tick.set_fontsize(14)
    
    #Set Font size for y axis ticks
    for tick in ax1.get_yticklabels():
        tick.set_fontsize(14)

    return fig


# In[8]:


'''load in data'''

res_a = pd.read_csv('res_a.csv')
res_b = pd.read_csv('res_b.csv')
air_df = pd.read_csv('airparge_dist.csv')


#append the two result tables a and b
df = res_a.append(res_b)


# In[9]:


'''prepare data for analysis'''


#Convert to datetime
df['Date'] = pd.to_datetime(df['SAMPLE_DATE'])


#Select COC of interest
out = df[df['CHEMICAL_NAME']=='Chlorobenzene']


#select qualifiers
out['INTERPRETED_QUALIFIERS'] = out['INTERPRETED_QUALIFIERS'].fillna('No Qualifier')
out1=out[(out['INTERPRETED_QUALIFIERS']=='No Qualifier') | (out['INTERPRETED_QUALIFIERS'] == 'ND') | (out['INTERPRETED_QUALIFIERS'] == 'J')]


#Create a year column for selecting all results after 2017
out1['Year'] = pd.DatetimeIndex(out1['SAMPLE_DATE']).year



#This is the master table referenced by the loop
out17 = out1[out1['Year'] >= 2017]


# In[10]:


'''get wells in AS study area and their distances from the AS system'''

#blank lists for distances and well IDs
airsparge_dist = []
well_list = []


#add data in sequential order to each list
for well in air_df['well_id']:
    well_list.append(well)
for dist in air_df['airsparge_dist']:
    airsparge_dist.append(dist)
    


# In[11]:


'''edit well IDs to match wells IDs in the results dataframe'''

#blank list for each well
well_list = []

#view result
print(well_list)


# In[12]:


#view result
print(airsparge_dist)


# In[13]:


slopes = []                                                  #accumulate the slopes of Ln(C/C0) vs. Time for each well in well list
r_squared_values = []                                        #accumulate the r-squared values of Ln(C/C0) vs. Time for each well in well list

calculated_df = pd.DataFrame()                               #blank dataframe for the calculated values for each well


index_tracker = 0                                            #track index


pdf = matplotlib.backends.backend_pdf.PdfPages("Biodeg_Charts_CB_Post2017.pdf") #make the pdf for the graphics


for well in well_list:
    df = out17[out17['LOC_NAME'] == well]                     #define subset of master table that is the current well
    df = column_days(df)                                      #make the days column
    df = get_C0_column(df)                                    #make the Ln(C/C0) column
    m, b = solve(df)                                          #solve for slope and y-intercept
    consolidated_df = consolidate(df)                          #clean up the dataframe
    calculated_df = calculated_df.append(consolidated_df)     #append the cleaned calculated dataframe to the master df
    r_squared = r_sqd(df)                                     #solve for R-squared
    air_dist = airsparge_dist[index_tracker]                  #solve for R-squared
    graphic = graph(df, well, air_dist, m, b, r_squared)      #render graphic
    pdf.savefig(graphic)                                      #save the graphic to the pdf
    slopes.append(m)                                          #append the slopes value 
    r_squared_values.append(r_squared)                        #append the r_squared value 
    index_tracker = index_tracker + 1                         #move to the next index position for airsparge_dist

pdf.close()
    


# In[14]:


slope_data = {'Well_ID':well_list, 'Airsparge_Distance': airsparge_dist,       #define a dictonary of the data for slope_data_df
                 'Slope': slopes, 'R-Squared': r_squared_values}

slope_data_df = pd.DataFrame(slope_data)                                       #make the dataframe


# In[15]:


calculated_df.to_csv('Biodeg_Calc_Table_Master.csv')         #write the calculated df to csv
slope_data_df.to_csv('Rate_Constants_Table.csv')             #write the slope_data_df to csv with other data


