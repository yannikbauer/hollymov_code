# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # run_get_all_unitexp_info: 
# Convenience JNB to show how to use and to test get_all_unitexp_info()

# %% [markdown]
# ## TODO

# %% [markdown]
# ## Setup

# %% [markdown]
# ### Start DJD
# Run main.py as interactive (-i) module (-m) and remotely (-r)\
# NOTE: any code inside the DJD-executing cell other than the executing line is not allowed

# %%
run -im djd.main -- --dbname=dj_hmov --user=write

# %%
# Import standard libraries/modules
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import rcParams
import matplotlib.gridspec as gridspec
# %matplotlib inline

# Import custom modules
# NOTE: os.path.dirname(__file__) = '/Users/Yannik/code/djd/djd'
from djd import util, signal, plot # DJD modules
from .plot import plot_opto_titration

from l6s import l6s_utils

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Test unit info functions

# %%
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')
unit_info_df

# %%
df = unit_info_df.copy()
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & ((df.e_name.str.contains('SparseNoise')) | (df.e_name.str.contains('chirp')) | (df.e_name.str.contains('oriTun')) | (df.e_name.str.contains('conTun')))]
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & ((df.e_name.str.contains('SparseNoise')) | (df.e_name.str.contains('oriTun12')))]
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & (df.e_name.str.contains('oriTun8') | df.e_name.str.contains('oriTun12') | df.e_name.str.contains('chirp'))]
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & (df.e_name.str.contains('oriTun8'))]
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & (df.e_name.str.contains('Sparse'))]
# df = df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3)]
df = df[(df.m=='Ntsr1Cre_2020_0002') & (df.s==3)]
df

# %%
df2 = df[['m','s','e','u']]#, 'e_name', 's_region']]
df2

# %%
df3 = l6s_utils.get_unitexp_fr(df2, load_df_name=False)
df3

# %%
df3.columns

# %%
df3 = l6s_utils.get_all_unitexp_info(mseu_df=df2)
df3

# %% [markdown]
# ## Run get_all_unitexp_info()
# check get_psth() and include splitbytrial kwarg option

# %%
mseu_df = l6s_utils.get_all_unitexp_info(load_fr_df=False, save_df_name='default')
mseu_df

# %%

# %%
mseu_df = l6s_utils.get_all_unitexp_info(load_fr_df=False, save_df_name='default')
mseu_df
