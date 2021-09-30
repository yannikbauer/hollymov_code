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
# # Analyze unit info df

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

from djd import hmov_models
from djd import hmov_unit
from l6s import l6s_utils # Layer 6 suppression code repo with utility functions for plotting unit overview

# This import does not seem to work - WHY? works for other DJD modules and functions - circular import?
# from djd.hmov_unit import get_tranges_hmov, _get_xptranges  

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Get unit info df

# %%
# Get unit info df
unit_info = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20201214')
unit_info

# %%
unit_info.keys()

# %% [markdown]
# ## Check OMIs
# NOTES
#  - df has a lot of variants of MAS-mov
#    - these show strong suppression
# TODO
#  - sparse noise exps seem to have OMIs, which should not be possible < fix!
#  - extreme OMIs of 1 or -1 likely due to FR=0 in one condition < fix!
#  - limit valid stimuli to ori/Aori, con, ...

# %%
unit_info['OMI']

# %%
# Show all
unit_info['OMI'].plot.hist(bins=40)

# %%
# Group by experiemnt
unit_info['OMI'].plot.hist(bins=40, by=unit_info['e_name'])  # does not work

# %%
df = unit_info[unit_info['OMI'].notna()][['e_name', 'OMI']]
df.plot.hist(bins=40, by=df['e_name']);  # identical to one above (< nans dropped automatically)

# %%
for i, group in df.groupby('e_name'):
#     ax = group['OMI'].plot.hist(bins=30, label=i, alpha=0.5)
    ax = group['OMI'].plot.hist(bins=30, alpha=0.5)
    ax.set_title(i)
    ax.set_xlabel('OMI')
    ax.set_xlim([-1, 1])
    
    mean = group['OMI'].mean()
    ax.axvline(mean, color='k', label=np.round(mean, 4))
    ax.legend()
    plt.show()

# %% [markdown]
# Next steps:
# - OMI: limit valid stimuli to ori/Aori, con, ...
# - try burst scatter for different stimuli (no group by given, so need to call several times into same axis for diff stimuli)
