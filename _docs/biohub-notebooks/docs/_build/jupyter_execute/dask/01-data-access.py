#!/usr/bin/env python
# coding: utf-8

# # Dask Example Notebook
# 
# This example comes from - https://github.com/dask/dask-examples/blob/master/dataframes/01-data-access.ipynb

# # DataFrames: Read and Write Data
#      
# Dask Dataframes can read and store data in many of the same formats as Pandas dataframes.  In this example we read and write data with the popular CSV and Parquet formats, and discuss best practices when using these formats.

# In[1]:


from IPython.display import HTML

HTML('<iframe width="560" height="315" src="https://www.youtube.com/embed/0eEsIA0O1iE?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>')


# ## Start Dask Client for Dashboard
# 
# Starting the Dask Client is optional.  It will provide a dashboard which 
# is useful to gain insight on the computation.  
# 
# The link to the dashboard will become visible when you create the client below.  We recommend having it open on one side of your screen while using your notebook on the other side.  This can take some effort to arrange your windows, but seeing them both at the same is very useful when learning.

# In[2]:


from dask.distributed import Client
client = Client(n_workers=1, threads_per_worker=4, processes=False, memory_limit='2GB')
client


# ## Create artificial dataset
# 
# First we create an artificial dataset and write it to many CSV files.
# 
# You don't need to understand this section, we're just creating a dataset for the rest of the notebook.

# In[3]:


import dask
df = dask.datasets.timeseries()
df


# In[4]:


import os
import datetime

if not os.path.exists('data'):
    os.mkdir('data')

def name(i):
    """ Provide date for filename given index
    
    Examples
    --------
    >>> name(0)
    '2000-01-01'
    >>> name(10)
    '2000-01-11'
    """
    return str(datetime.date(2000, 1, 1) + i * datetime.timedelta(days=1))
    
df.to_csv('data/*.csv', name_function=name);


# ## Read CSV files
# 
# We now have many CSV files in our data directory, one for each day in the month of January 2000.  Each CSV file holds timeseries data for that day.  We can read all of them as one logical dataframe using the `dd.read_csv` function with a glob string.

# In[5]:


get_ipython().system('ls data/*.csv | head')


# In[6]:


get_ipython().system('head data/2000-01-01.csv')


# In[7]:


get_ipython().system('head data/2000-01-30.csv')


# We can read one file with `pandas.read_csv` or many files with `dask.dataframe.read_csv`

# In[8]:


import pandas as pd

df = pd.read_csv('data/2000-01-01.csv')
df.head()


# In[9]:


import dask.dataframe as dd

df = dd.read_csv('data/2000-*-*.csv')
df


# In[10]:


df.head()


# ## Tuning read_csv
# 
# The Pandas `read_csv` function has *many* options to help you parse files.  The Dask version uses the Pandas function internally, and so supports many of the same options.  You can use the `?` operator to see the full documentation string.

# In[11]:


get_ipython().run_line_magic('pinfo', 'pd.read_csv')


# In[12]:


get_ipython().run_line_magic('pinfo', 'dd.read_csv')


# In this case we use the `parse_dates` keyword to parse the timestamp column to be a datetime.  This will make things more efficient in the future.  Notice that the dtype of the timestamp column has changed from `object` to `datetime64[ns]`.

# In[13]:


df = dd.read_csv('data/2000-*-*.csv', parse_dates=['timestamp'])
df


# ## Do a simple computation
# 
# Whenever we operate on our dataframe we read through all of our CSV data so that we don't fill up RAM.  This is very efficient for memory use, but reading through all of the CSV files every time can be slow.

# In[14]:


get_ipython().run_line_magic('time', "df.groupby('name').x.mean().compute()")


# In[ ]:





# ## Write to Parquet
# 
# Instead, we'll store our data in Parquet, a format that is more efficient for computers to read and write.

# In[15]:


df.to_parquet('data/2000-01.parquet', engine='pyarrow')


# In[16]:


get_ipython().system('ls data/2000-01.parquet/')


# ## Read from Parquet

# In[17]:


df = dd.read_parquet('data/2000-01.parquet', engine='pyarrow')
df


# In[18]:


get_ipython().run_line_magic('time', "df.groupby('name').x.mean().compute()")


# ## Select only the columns that you plan to use
# 
# Parquet is a column-store, which means that it can efficiently pull out only a few columns from your dataset.  This is good because it helps to avoid unnecessary data loading.

# In[19]:


get_ipython().run_cell_magic('time', '', "df = dd.read_parquet('data/2000-01.parquet', columns=['name', 'x'], engine='pyarrow')\ndf.groupby('name').x.mean().compute()")


# Here the difference is not that large, but with larger datasets this can save a great deal of time.

# ## Learn more
# 
# http://dask.pydata.org/en/latest/dataframe-create.html
