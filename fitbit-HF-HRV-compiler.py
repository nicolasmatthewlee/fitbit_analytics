#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import datetime
import re
get_ipython().run_line_magic('config', "InlineBackend.figure_format='retina'")
pd.set_option("max_rows",None)


# In[2]:


# get folder
folder=input('What is the address to your MyFitbitData sleep folder?\nex) xxx/MyFitbitData/JohnSmith/Sleep\n')


# In[3]:


# get list of filenames of Heart Rate Variability Details
filenames=os.listdir(folder)
hrv_files=[]
for f in filenames:
    if 'Heart Rate Variability Details' in f:
        hrv_files.append(f)
        
if len(hrv_files) == 0:
    print('Could not find any "Heart Rate Variability Details" files.')
    os._exit(1)
    
# order files
ordered_hrv_files=pd.Series(hrv_files).sort_values()


# In[4]:


# iterate through all hrv detail files and compile data into a .csv
csv_text='date,rmssd_avg,low_frequency_avg,high_frequency_avg\n'

for f in ordered_hrv_files:
    
    # read file
    df=pd.read_csv(os.path.join(folder,f))
    # get date
    date=re.findall('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]',f)[0]

    # convert timestamp to datetime
    df['timestamp']=pd.to_datetime(df['timestamp'])

    # generate previous_timestamp column

    pret=df.apply(lambda x: x['timestamp'],axis=1).shift(1)
    pret[0]=df['timestamp'][0]
    df['previous_timestamp']=pret

    # generate time_diff column
    df['time_diff']=df['timestamp']-df['previous_timestamp']

    # assign groups

    def assign_groups(df):

        # group number
        g=0
        group_list=[]

        for r in df.itertuples():

            # if time diff is greater than 1 hour, data is part of next group
            if r.time_diff > datetime.timedelta(hours=1):
                g+=1

            group_list.append(g)

        df['group']=group_list

    assign_groups(df)

    # delete unneeded cols
    del df['previous_timestamp']
    del df['time_diff']
    
    # add to csv_text
    csv_text+=date+','+str(df[df['group']==0]['rmssd'].mean())+','+str(df[df['group']==0]['low_frequency'].mean())+','+str(df[df['group']==0]['high_frequency'].mean())+'\n'
    
# save data
path=os.path.join(folder,'hrv_compiled.csv')
csv=open(path,'w')
csv.write(csv_text)
csv.close()
print(f'Data saved to: {path}')


# In[ ]:




