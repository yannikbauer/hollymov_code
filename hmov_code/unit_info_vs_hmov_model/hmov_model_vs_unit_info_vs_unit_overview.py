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
# # Hmov units: Compare unit overview plot, unit info and Hmov RF models

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
import matplotlib.pyplot as plt

from djd import glms
from djd import hmov_unit
from l6s import l6s_utils # Layer 6 suppression code repo with utility functions for plotting unit overview

# This import does not seem to work - WHY? works for other DJD modules and functions - circular import?
# from djd.hmov_unit import get_tranges_hmov, _get_xptranges  

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Show example unit plot_unit_overview() + unit info + model RFs

# %% jupyter={"outputs_hidden": true}
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}

# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Plot unit overview
fig, axs = l6s_utils.plot_unit_overview(ukey, save=False, unit_info_df=unit_info_df)

# Plot SplineLNP RF
# hmov_models._plot_RF(ukey, scale=True)

# %% [markdown]
# ## Show plot_unit_overview() + unit info + model RFs

# %%
Mouse()

# %% [markdown]
# ## Ntsr1Cre_2020_0004: 50x dilution good dLGN opto effects online

# %%
ukeys = pd.DataFrame((Unit.Properties & HmovUnit() & {'m': 'Ntsr1Cre_2020_0004'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()

# %%

# %%

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()

# %% [markdown]
# ## Ntsr1Cre_2020_0002: 10x dilution w mediocre dLGN opto effects online

# %%
ukeys = pd.DataFrame((Unit.Properties & HmovUnit() & {'m': 'Ntsr1Cre_2020_0002'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()

# %% [markdown]
# ## Ntsr1Cre_2019_0008

# %%
ukeys = pd.DataFrame((Unit.Properties & HmovUnit() & {'m': 'Ntsr1Cre_2019_0008'}).fetch(dj.key))
ukeys

# %%
plt.close('all')

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2019_0007

# %%
ukeys = pd.DataFrame((Unit.Properties & HmovUnit() & {'m': 'Ntsr1Cre_2019_0007'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2020_0001: control mouse with beatiful responses

# %%
ukeys = pd.DataFrame((Unit.Properties & HmovUnit() & {'m': 'Ntsr1Cre_2020_0001'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2020_0003: 100x dilution and strong V1 effects (but none in dLGN)
# - hollymov not parsed by DJD - check why
# - most V1 responses actually not so nice

# %%
ukeys = pd.DataFrame((Unit.Properties() & {'m': 'Ntsr1Cre_2020_0003'}).fetch(dj.key)) # HmovUnit not populated for this series - fix!
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2019_0002: no dilution, nohmov, and actually some opto effects (so effects in 2019_0007 and 2019_0008 not so surprising)

# %%
ukeys = pd.DataFrame((Unit.Properties() & {'m': 'Ntsr1Cre_2019_0002'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2019_0003: no dilution, no hmov_03, no opto effects

# %%
ukeys = pd.DataFrame((Unit.Properties() & {'m': 'Ntsr1Cre_2019_0003'}).fetch(dj.key))
ukeys

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %% [markdown]
# ## Ntsr1Cre_2019_0002: strong V1 opto effects

# %%
ukeys = pd.DataFrame([{'m': 'Ntsr1Cre_2020_0002', 's': 2, 'u': 120}, {'m': 'Ntsr1Cre_2020_0002', 's': 2, 'u': 128}, {'m': 'Ntsr1Cre_2020_0002', 's': 2, 'u': 129}])

# %%
build({'m': 'Ntsr1Cre_2020_0002'})

# %%
# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='default')

# Go through each unit and plot overview, hmov model and print unit infos
# for idx, ukey in ukeys.head(n=2).iterrows():
for idx, ukey in ukeys.iterrows():
    ukey = ukey.to_dict()
    
    # Plot unit overview
    fig, axs = l6s_utils.plot_unit_overview(ukey, save=True, unit_info_df=unit_info_df)
    plt.show()    

# %%
