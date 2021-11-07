#!/usr/bin/env python
# coding: utf-8

# # Launch CellXGene
# 
# Run cellxgene from a Jupyter cell:
# 
# ```
# ! cellxgene launch --host 0.0.0.0 https://cellxgene-example-data.czi.technology/pbmc3k.h5ad
# ```
# 
# Or directly from the terminal:
# 
# ```
# cellxgene launch --host 0.0.0.0 https://cellxgene-example-data.czi.technology/pbmc3k.h5ad
# ```
# 
# Eitehr way you should see similar output:
# 
# ```
# [cellxgene] Starting the CLI...
# [cellxgene] Loading data from pbmc3k.h5ad.
# [cellxgene] Warning: Moving element from .uns['neighbors']['distances'] to .obsp['distances'].
# 
# This is where adjacency matrices should go now. 
# [cellxgene] Warning: Moving element from .uns['neighbors']['connectivities'] to .obsp['connectivities'].
# 
# This is where adjacency matrices should go now. 
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# WARNING:root:Type float64 will be converted to 32 bit float and may lose precision.
# [cellxgene] Launching! Please go to http://0.0.0.0:5005 in your browser.
# [cellxgene] Type CTRL-C at any time to exit.
# ```
# 
# **Don't forget to make the host 0.0.0.0**

# In[1]:


#! cellxgene launch --host 0.0.0.0 https://cellxgene-example-data.czi.technology/pbmc3k.h5ad

