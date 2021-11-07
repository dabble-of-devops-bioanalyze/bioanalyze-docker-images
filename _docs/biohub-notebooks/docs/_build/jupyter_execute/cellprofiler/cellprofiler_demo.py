#!/usr/bin/env python
# coding: utf-8

# # CellProfiler Example Notebook
# 
# The cellprofiler example notebook came from the [CellProfiler notebooks repo](https://github.com/CellProfiler/notebooks/blob/master/cellprofiler_demo.ipynb) with thanks. The only changes that were made were fix some import errors for CellProfiler v4.
# 
# Data comes from the [CellProfiler notebook repo](https://github.com/CellProfiler/notebooks/tree/master/data).

# In[1]:


import os

import cellprofiler
import cellprofiler_core
import cellprofiler_core.pipeline
from cellprofiler_core.preferences import set_headless

import cellprofiler_core.image
import cellprofiler_core.measurement

import cellprofiler.modules.maskimage
import cellprofiler_core.pipeline
import cellprofiler_core.workspace

import numpy as np
import pandas as pd
import skimage.io


# In[2]:


def run_pipeline(pipeline_filename, image_dict):
    set_headless()
    
    # Create and load the pipeline
    pipeline = cellprofiler_core.pipeline.Pipeline()
    pipeline.load(pipeline_filename)
    
    # Create the image set, and add the image data
    image_set_list = cellprofiler_core.image.ImageSetList()
    image_set = image_set_list.get_image_set(0)
    for image_name, input_pixels in image_dict.items():
        image_set.add(image_name, cellprofiler_core.image.Image(input_pixels))
        
    # Persist the object set here (for now, see workspace TODO)
    object_set = cellprofiler_core.object.ObjectSet()

    # We can only run one group -- set the group index to 1.
    measurements = cellprofiler_core.measurement.Measurements()
    measurements.group_index = 1

    # Run the modules!
    for module in pipeline.modules():
        # Yes, we really do have to create a new workspace for each module
        # because the module attribute is required. Go team.
        workspace = cellprofiler_core.workspace.Workspace(
            image_set=image_set,
            image_set_list=image_set_list,
            measurements=measurements, 
            module=module,
            object_set=object_set, 
            pipeline=pipeline
        )
        
        module.prepare_run(workspace)
        module.run(workspace)
        module.post_run(workspace)
    
    # The workspace object has access to the measurements
    # and the image set/image set list which can be used
    # to use/view/store/whatever output data.
    return workspace


# In[3]:


def objects2df(measurements, objects_name):
    features = measurements.get_feature_names(objects_name)
    
    n_features = len(features)
    n_objects = int(measurements.get_measurement("Image", "Count_{}".format(objects_name)))
    
    data = np.empty((n_objects, n_features))
    
    for feature_idx, feature in enumerate(features):
        data[:, feature_idx] = measurements.get_measurement(objects_name, feature)
    
    return pd.DataFrame(
        data=data,
        index=np.arange(1, n_objects + 1),
        columns=features
    )


# In[4]:


os.getcwd()


# In[5]:


# This should match what NamesAndTypes would produce.
data_dir = os.path.join(os.getcwd(), "data")


images = {
    "OrigBlue": skimage.io.imread(os.path.join(data_dir, "images/01_POS002_D.TIF")),
    "OrigGreen": skimage.io.imread(os.path.join(data_dir, "images/01_POS002_F.TIF")),
    "OrigRed": skimage.io.imread(os.path.join(data_dir, "images/01_POS002_R.TIF"))
}

pipeline_filename = os.path.join(data_dir , "ExampleFly.cppipe")


# In[6]:


workspace = run_pipeline(pipeline_filename, images)


# In[7]:


# Get the "Nuclei" object measurements, as a pandas DataFrame
df = objects2df(workspace.measurements, "Nuclei")
df.head()


# In[8]:


# Display the "RGBImage" image, created by GrayToColor

from pylab import rcParams
rcParams['figure.figsize'] = 10, 15

rgb_image = workspace.image_set.get_image("RGBImage")
skimage.io.imshow(rgb_image.pixel_data)


# ## Get Help
# 
# ```python
# help(workspace.measurements)
# ```

# ## Additional Considerations
# 
# ### Saving Data Frames
# 
# Generally,  you run an experiment, and then you want to save your data. CellProfiler creates CSVs, which play nicely with the rest of the PyData And RTidyVerse ecosystem.
# 
# #### Save as a CSV
# 
# You can always just save your experiment outputs as CSVs.
# 
# ```python
# df.to_csv('experiment-plate.csv')
# ```
# 
# #### Save as a Parquet
# 
# My favorite way to save data, particularly if it is scientific data, is as a [Parquet File](https://parquet.apache.org/). A parquet file is a dataframe in machine readable format, which will save you quite a bit on both performance.
# 
# ```python
# df.to_parquet('experiment-plate.parquet')
# ```
# 
# #### Save to S3
# 
# You can save to S3 instead of local storage using [S3FS](https://s3fs.readthedocs.io/en/latest/#integration):
# 
# ```python
# df.to_parquet("s3://bucket/path/experiment-plate.parquet", storage_options={"anon": True})
# ```
# 

# In[ ]:




