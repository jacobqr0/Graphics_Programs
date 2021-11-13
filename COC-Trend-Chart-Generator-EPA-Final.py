# In[ ]:


''' This program generates time-series charts for Chlorobenzene, 
    1,4 Dichlorobenzene, and Benzene concantrations and compiles 
    each figure into a PDF. Two inputs are required. One input is 
    a CSV file giving each well ID, the figure number, and brief 
    location description of the well. The second input is a database 
    export file that contains the contaminant concentration data. The 
    output of this program will generate two PDFs. One PDF will be 
    the time-series trends with the vertical axes in log-scale, and 
    the other will be in natural scale.'''


# In[1]:


'''import modules'''

import pandas as pd
from matplotlib import pyplot as plt 
import numpy as np
import datetime as datetime
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
import matplotlib.backends.backend_pdf


# In[2]:


'''define graphics function - natural scale'''

def graph(df, fig_id, well_id, plume_loc):
    
    #Define analyte data from the master dataframe
    CB = df[df['CHEMICAL_NAME'] == 'Chlorobenzene']
    BZ = df[df['CHEMICAL_NAME'] == 'Benzene']
    DB = df[df['CHEMICAL_NAME'] == '1,4-Dichlorobenzene']
    
    ASB_list = ['BW-02', 'CW-1D', 'CW-1S', 'CW-2D', 'CW-2S',
                'CW-3D', 'CW-3S', 'CW-4D', 'CW-4S', 'CW-5D',
                'CW-5S', 'CW-6D', 'CW-6S', 'CW-7D', 'CW-7S',
                'CW-8D', 'CW-8S', 'MW-10', 'MW-11', 'MW-12', 
                'MW-13', 'MW-14', 'MW-15', 'MW-16', 'PMW-02',
                'PMW-02D', 'PMW-03', 'PMW-03D', 'PMW-04', 'PMW-04D',
                'PMW-05', 'PMW-05D', 'PMW-06', 'PMW-06D', 'PMW-07',
                'PMW-07D', 'PMW-08D', 'PMW-08S', 'PMW-09D', 'PMW-09S',
                'PMW-10D', 'PMW-11D', 'PMW-12D', 'PZ-16R', 'TW-32', 
                'TW-42', 'TW-45', 'TW-46', 'TW-71D', 'TW-71S',
                'TW-73', 'TW-75', 'TW-84', 'TW-44', 'TW-102',
                'TW-29', 'TW-27R', 'TW-28', 'BW-05']
    
    #Define min and max dates of the lab results
    date_range1= np.append( BZ['SAMPLE_DATE'].array, CB['SAMPLE_DATE'].array)
    full_daterange = np.append(date_range1, DB['SAMPLE_DATE'].array)
    try:
        min_date = full_daterange.min()
        if min_date < np.datetime64('2009-01-01'):
            CB = CB[CB['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
            BZ = BZ[BZ['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
            DB = DB[DB['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
    except ValueError:
        pass

    #Create figure and axes objects
    fig = plt.figure(figsize=(14,10))
    ax1 = plt.subplot(1,1,1) #primary axis
    ax2 =ax1.twinx() #secondary axis
    
    #Graph contaminant trends - primary axis
    ax1.plot(DB['SAMPLE_DATE'], DB['REPORT_RESULT_VALUE'], marker = 'D', color = 'blue') #plot 1,4-Dichlorobenzene
    ax1.plot(BZ['SAMPLE_DATE'], BZ['REPORT_RESULT_VALUE'], marker = 's', color = 'green') #plot Benzene
    
    #define font for the legend
    font = font_manager.FontProperties(family='Arial', size=11)
    
    #Add primary axis components to the legend
    ax1.legend(['1,4-Dichlorobenzene', 'Benzene'], loc =(-0.08, -0.15),
               prop=font)
    
    #Graph contaminant trends - secondary axis    
    ax2.plot(CB['SAMPLE_DATE'], CB['REPORT_RESULT_VALUE'], marker = '^', color = 'orange') #plot Chlorobenzene
    
    #Graph AS/B Long-Term Operations Start - secondary axis (if applicable)
    if well_id in ASB_list:
        ax2.axvline( x =datetime.datetime(2018,5,20), color = 'brown')
        legend2 = ax2.legend(['Chlorobenzene', 'AS/B Long-Term Operations Start'], loc =(0.14, -0.15), #plot legend
                         prop=font)
        plt.gca().add_artist(legend2)
    else:
        legend2 = ax2.legend(['Chlorobenzene'], loc =(0.14, -0.15), #plot legend
                         prop=font)
        plt.gca().add_artist(legend2)
    
    #Label x-axis
    ax1.set_xlabel('Sampling Date', fontsize=14, 
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #Label y-axis - primary
    ax1.set_ylabel('1,4-Dichlorobenzene and Benzene Concentration (µg/L)', fontsize =14,
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #Label y-axis - secondary
    ax2.set_ylabel('Chlorobenzene Concentration (µg/L) ', fontsize =14,
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #edit x-axis format
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    
    #Add title
    plt.title("Figure B-" + str(fig_id) + "\n" + str(well_id) +" " + str(plume_loc) + " Concentration vs. Time",
             fontsize =14, fontweight = 'semibold', fontfamily = 'Arial')
    
    #Annotate with the MCLs    
    ax2.annotate( r"$\bf{"+ "MCLs:"+ "}$" + '\nChlorobenzene = 100 µg/L\nBenzene = 5 µg/L\n1,4-Dichlorobenzene = 75 µg/L', 
                 (700,10), xycoords = 'figure points', fontsize=10)
           
    #Adjust x axis tick label orientation and size
    for tick in ax1.get_xticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")
        tick.set_rotation(20)
    
    #Set font properties for y axis ticks - primary axis
    for tick in ax1.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")
        
    #Set font properties for y axis ticks - secondary axis
    for tick in ax2.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")

    #Add Horizontal Gridlines
    ax1.grid(axis = 'y', which='major', color='black')
    
    try:
        #Define maximum results to set the upper y-axis limit
        ax1_max = (np.append(DB['REPORT_RESULT_VALUE'].array, BZ['REPORT_RESULT_VALUE'].array).max())
        ax2_max = CB['REPORT_RESULT_VALUE'].max()

        #set axes scale
        ax1.set_ylim([0, ax1_max +(ax1_max*0.05)])
        ax2.set_ylim([0, ax2_max + (ax2_max*0.05)])
    except ValueError:
        pass
    
    return fig


# In[3]:


'''define graphics function - log scale'''

def graph_log_scale(df, fig_id, well_id, plume_loc):
    
    #Define analyte data from the master dataframe
    CB = df[df['CHEMICAL_NAME'] == 'Chlorobenzene']
    BZ = df[df['CHEMICAL_NAME'] == 'Benzene']
    DB = df[df['CHEMICAL_NAME'] == '1,4-Dichlorobenzene']
    
    ASB_list = ['BW-02', 'CW-1D', 'CW-1S', 'CW-2D', 'CW-2S',
                'CW-3D', 'CW-3S', 'CW-4D', 'CW-4S', 'CW-5D',
                'CW-5S', 'CW-6D', 'CW-6S', 'CW-7D', 'CW-7S',
                'CW-8D', 'CW-8S', 'MW-10', 'MW-11', 'MW-12', 
                'MW-13', 'MW-14', 'MW-15', 'MW-16', 'PMW-02',
                'PMW-02D', 'PMW-03', 'PMW-03D', 'PMW-04', 'PMW-04D',
                'PMW-05', 'PMW-05D', 'PMW-06', 'PMW-06D', 'PMW-07',
                'PMW-07D', 'PMW-08D', 'PMW-08S', 'PMW-09D', 'PMW-09S',
                'PMW-10D', 'PMW-11D', 'PMW-12D', 'PZ-16R', 'TW-32', 
                'TW-42', 'TW-45', 'TW-46', 'TW-71D', 'TW-71S',
                'TW-73', 'TW-75', 'TW-84', 'TW-44', 'TW-102',
                'TW-29', 'TW-27R', 'TW-28', 'BW-05']
    
    #Define min and max dates of the lab results
    date_range1= np.append( BZ['SAMPLE_DATE'].array, CB['SAMPLE_DATE'].array)
    full_daterange = np.append(date_range1, DB['SAMPLE_DATE'].array)
    try:
        min_date = full_daterange.min()
        if min_date < np.datetime64('2009-01-01'):
            CB = CB[CB['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
            BZ = BZ[BZ['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
            DB = DB[DB['SAMPLE_DATE'] >= datetime.datetime(2009,1,1)]
    except ValueError:
        pass

    #Create figure and axes objects
    fig = plt.figure(figsize=(14,10))
    ax1 = plt.subplot(1,1,1) #primary axis
    ax2 =ax1.twinx() #secondary axis
    
    #Graph contaminant trends - primary axis
    ax1.plot(DB['SAMPLE_DATE'], DB['REPORT_RESULT_VALUE'], marker = 'D', color = 'blue') #plot 1,4-Dichlorobenzene
    ax1.plot(BZ['SAMPLE_DATE'], BZ['REPORT_RESULT_VALUE'], marker = 's', color = 'green') #plot Benzene
    
    #define font for the legend
    font = font_manager.FontProperties(family='Arial', size=11)
    
    #Add primary axis components to the legend
    ax1.legend(['1,4-Dichlorobenzene', 'Benzene'], loc =(-0.08, -0.15),
               prop=font)
    
    #Graph contaminant trends - secondary axis    
    ax2.plot(CB['SAMPLE_DATE'], CB['REPORT_RESULT_VALUE'], marker = '^', color = 'orange') #plot Chlorobenzene

    #Graph AS/B Long-Term Operations Start - secondary axis
    if well_id in ASB_list:
        ax2.axvline( x =datetime.datetime(2018,5,20), color = 'brown')
        legend2 = ax2.legend(['Chlorobenzene', 'AS/B Long-Term Operations Start'], loc =(0.14, -0.15),
                         prop=font)
        plt.gca().add_artist(legend2)
    else:
        legend2 = ax2.legend(['Chlorobenzene'], loc =(0.14, -0.15),
                         prop=font)
        plt.gca().add_artist(legend2)
                              
    #Label x-axis
    ax1.set_xlabel('Sampling Date', fontsize=14, 
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #Label y-axis - primary
    ax1.set_ylabel('1,4-Dichlorobenzene and Benzene Concentration (µg/L)', fontsize =14,
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #Label y-axis - secondary
    ax2.set_ylabel('Chlorobenzene Concentration (µg/L) ', fontsize =14,
                   fontweight = 'semibold', fontfamily = 'Arial')
    
    #edit x-axis format
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    
    #Apply log scale to primary and secondary axes
    ax1.set_yscale('log')
    ax2.set_yscale('log')
    
    #Add title
    plt.title("Figure B-" + str(fig_id) + " Log Scale\n" + str(well_id) +" " + str(plume_loc) + " Concentration vs. Time",
             fontsize =14, fontweight = 'semibold', fontfamily = 'Arial')
        

    #Annotate with the MCLs    
    ax2.annotate( r"$\bf{"+ "MCLs:"+ "}$" + '\nChlorobenzene = 100 µg/L\nBenzene = 5 µg/L\n1,4-Dichlorobenzene = 75 µg/L', 
                 (700,10), xycoords = 'figure points', fontsize=10)
           
    #Adjust x axis tick label orientation and size
    for tick in ax1.get_xticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")
        tick.set_rotation(20)
    
    #Set font properties for y axis ticks - primary axis
    for tick in ax1.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")
        
    #Set font properties for y axis ticks - secondary axis
    for tick in ax2.get_yticklabels():
        tick.set_fontsize(12)
        tick.set_fontfamily("Arial")
        tick.set_fontweight("semibold")

    #Add Horizontal Gridlines
    ax1.grid(axis = 'y', which='major', color='black')
    
    #Define maximum results to set the upper y-axis limit
    try:
        ax1_max = (np.append(DB['REPORT_RESULT_VALUE'].array, BZ['REPORT_RESULT_VALUE'].array).max())
        ax2_max = CB['REPORT_RESULT_VALUE'].max()
        #set axes scale
        ax1.set_ylim([0.1, ax1_max +(ax1_max*0.1)])
        ax2.set_ylim([0.1, ax2_max + (ax2_max*0.1)])
    except ValueError:
        pass
    
    return fig


# In[4]:


'''read input files'''

figure_labels = pd.read_csv('Figure-Names-Trend-Graphs_ASB_update.csv')
res_a = pd.read_csv('res_a.csv')
res_b = pd.read_csv('res_b.csv')

df = res_a.append(res_b)
df.head()


# In[5]:


df['SAMPLE_DATE'] = pd.to_datetime(df['SAMPLE_DATE'])


# In[6]:


'''Make Lists of Figure Elements'''

loc_ids = [loc for loc in figure_labels['LOCID']]
fig_nums = [fig_num for fig_num in figure_labels['FIGURE_NUMBER']]
locs = [location for location in figure_labels['LOCATION']]


# In[7]:


'''Get all unique wells in the database export'''

wells_in_file = df['LOC_NAME'].unique()


# In[8]:


''' Build Graphics PDF - Normal Scale '''

pdf_normal_scale = matplotlib.backends.backend_pdf.PdfPages("C1_to_C555_2021_draft_NORMAL.pdf")


# In[9]:


''' Build Graphics PDF - Log Scale '''

pdf_log_scale = matplotlib.backends.backend_pdf.PdfPages("C1_to_C555_2021_draft_LOG.pdf")


# In[10]:


'''loop over each element in the list and make a graph for each LOC ID, log scale'''

for i, well_id in enumerate(loc_ids):
    if well_id not in wells_in_file:
        continue
    current_well = df[df["LOC_NAME"] == well_id]
    fig_log = graph_log_scale(current_well, fig_nums[i], well_id, locs[i])
    pdf_log_scale.savefig(fig_log)
    
'''close PDFs'''    

pdf_log_scale.close()


# In[11]:


'''loop over each element in the list and make a graph for each LOC ID, normal scale'''

for i, well_id in enumerate(loc_ids):
    if well_id not in wells_in_file:
        continue
    current_well = df[df["LOC_NAME"] == well_id]
    fig_norm = graph(current_well, fig_nums[i], well_id, locs[i])
    pdf_normal_scale.savefig(fig_norm)
    
'''close PDFs'''    
    
pdf_normal_scale.close()





