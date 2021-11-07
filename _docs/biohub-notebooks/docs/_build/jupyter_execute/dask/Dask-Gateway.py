#!/usr/bin/env python
# coding: utf-8

# # Dask Gateway Connection Example

# In[1]:


from dask_gateway import Gateway, GatewayCluster
from dask.distributed import Client
from dask import delayed
import os


# 
# ```python
# gateway = Gateway()  # connect to Gateway
# 
# cluster = gateway.new_cluster()  # create cluster
# cluster.scale(...)  # scale cluster
# 
# client = Client(cluster)  # connect Client to Cluster
# ```

# In[2]:


e = os.environ
for k in e.keys():
    if 'DASK' in k:
        print('{} {}'.format(k, e[k]))


# In[3]:


os.environ['JUPYTER_IMAGE_SPEC']


# In[4]:


dask_gateway_address = os.environ.get('DASK_GATEWAY__ADDRESS')
dask_gateway_address


# In[5]:


#gateway = Gateway(dask_gateway_address, auth="jupyterhub")
gateway = Gateway()


# In[6]:


#help(gateway)


# In[7]:


gateway.list_clusters()


# In[8]:


cluster = gateway.new_cluster()  # create cluster

cluster.adapt(minimum=2, maximum=10)
client = Client(cluster)  # connect Client to Cluster


# In[9]:


client


# In[10]:


#client.get_versions(check=True)


# In[11]:


options = gateway.cluster_options()
options


# In[12]:


cluster


# In[13]:


import dask.array as da
a = da.random.normal(size=(10000, 10000), chunks=(500, 500))
a.mean().compute()


# In[ ]:





# In[14]:


# Optional - Shut down your cluster. 
# The Dask Cluster will also be shutdown when you logout
#clusters = gateway.list_clusters()
#for cluster in clusters:
#    gateway.stop_cluster(cluster.name)


# In[15]:


#gateway.list_clusters()


# In[ ]:




