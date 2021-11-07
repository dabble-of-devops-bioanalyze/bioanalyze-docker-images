#!/usr/bin/env python
# coding: utf-8

# ## Run MLFlow
# 
# This is just a quick notebook no how to run MLFlow through jupyterhub

# Run this from a terminal -  
# 
# ```
# conda install -y jupyter-server-proxy mlflow gunicorn
# ```

# In[1]:


import shutil
import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts


# In[2]:


get_ipython().system(' conda install -y -c conda-forge jupyter-server-proxy mlflow gunicorn')


# In[3]:


get_ipython().system(' which mlflow')

# If you've run conda install -y jupyter-server-proxy mlflow gunicorn
# this should be /srv/conda/envs/notebook/bin/mlflow


# In[4]:


dirs = ['outputs', 'mlruns']

for d in dirs:
    if os.path.exists(d):
        shutil.rmtree(d)


# This example comes from the ML Flow Tutorial
# 
# https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html

# In[5]:


import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts

if __name__ == "__main__":
    # Log a parameter (key-value pair)
    log_param("param1", randint(0, 100))

    # Log a metric; metrics can be updated throughout the run
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    # Log an artifact (output file)
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/test.txt", "w") as f:
        f.write("hello world!")
    log_artifacts("outputs")


# ## View Any Server in a Browser
# 
# Anything running on a port can be accessed in the browser. If you are running this through the jupyterhub interface it will be proxied for you automatically and available at:
# 
# ```
# http://{{your_url}}/user/{{username}}/proxy/{{port}}/
# ```

# In[6]:


get_ipython().system(' mlflow server -w 1')


# Now check it out at: 
# 
# https://ds.stemawayaws.com/user/admin/proxy/5000/

# You can also access the server through an iframe.

# In[7]:


#from IPython.display import HTML

#HTML('<iframe width="560" height="315" src="https://YOUR_URL/user/USERNAME/proxy/5000/" frameborder="0" allowfullscreen></iframe>')

