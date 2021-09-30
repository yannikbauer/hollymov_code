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
# # Analyze unit info burst ratios

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
unit_info = l6s_utils.get_all_unitexp_info(load_df_name='default')
unit_info

# %%
unit_info.keys()

# %%
# OLD
unit_info.keys()

# %% [markdown]
# ## Check burst ratios in opto vs control
# NOTES
# - include all duplicate expts for now

# %%
df = unit_info[unit_info['burst_ratio_ctrl'].notna()][['m', 's', 'u', 'burst_ratio_ctrl', 'burst_ratio_opto', 'omi_stim', 'sbc_zscore', 'e_name']]
df

# %% [markdown]
# ### Check burst ratio opto vs control against OMI

# %%
# Plot burst ratio opto vs control + OMIs
fig, axs = plt.subplots(1,2, figsize=(16,6))

vminmax = np.max(np.absolute(df.omi_stim.values))  # too much grey at 1
vminmax = 0.5
df.plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='omi_stim', colormap='coolwarm', vmin=-vminmax, vmax=vminmax, alpha=1, ax=axs[0]);
axs[0].set_aspect('equal')
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('Burst ratio opto vs control and OMI')

sc = df.plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='omi_stim', colormap='coolwarm', vmin=-vminmax, vmax=vminmax,
                marker='$\u25EF$', s=45, alpha=0.75, ax=axs[1]); # facecolors='none',
# sc.set_facecolor("none")
axs[1].set_aspect('equal')
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('Burst ratio opto vs control and OMI - circle markers')

# %% [markdown]
# ### Check burst ratio opto vs control against SbC scores

# %%
# Plot burst ratio opto vs control + SbC scores
fig, axs = plt.subplots(1,3, figsize=(18,6), constrained_layout=True)
axs[0].set_aspect('equal')

vminmax = np.nanmax(np.absolute(df.sbc_zscore.values))  # too high at 76
vminmax = 10

df.plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='sbc_zscore', colormap='coolwarm', vmin=-vminmax, vmax=vminmax, ax=axs[0]);
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('Burst ratio opto vs control and SbC score')

df.plot.scatter(x='burst_ratio_ctrl', y='sbc_zscore', colormap='coolwarm', ax=axs[1]);
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('Burst ratio control vs SbC score')

df.plot.scatter(x='burst_ratio_opto', y='sbc_zscore', colormap='coolwarm', ax=axs[2]);
axs[2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2].transAxes, zorder=-1)
axs[2].set_title('Burst ratio control vs SbC score')

# %% [markdown]
# ### Check burst ratio opto vs control grouped by stimulus type

# %%
np.unique(df['e_name'])

# %%
# Plot OSI/DSI opto vs control + SbC scores
fig, axs = plt.subplots(1,1, figsize=(8,8))
axs.set_aspect('equal')

# OSI
df[df.e_name.str.contains('ori')].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='r', ax=axs, label='ori');
df[df.e_name.str.contains('con')].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='b', ax=axs, label='con');
df[df.e_name.str.contains('chirp')].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='g', ax=axs, label='chirp');
axs.plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs.transAxes, zorder=-1)
axs.set_title('Burst ratios grouped by stimulus')

plt.legend();

# %% [markdown]
# ### Check burst ratio against chirp type

# %%
chirp_df = unit_info[unit_info['chirp_type'].notna()][['m', 's', 'u', 'chirp_type']]
chirp_df

# %%
# Merge chirp type info
df = df.merge(chirp_df, on=['m','s','u'], how='left')
df

# %%
# Plot OSI/DSI opto vs control + SbC scores
fig, axs = plt.subplots(1,1, figsize=(8,8))
axs.set_aspect('equal')

# OSI
df[df['chirp_type']=='ON-sust.'].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='r', ax=axs, label='ON-sust.');
df[df['chirp_type']=='OFF-sust.'].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='b', ax=axs, label='OFF-sust.');
df[df['chirp_type']=='ON-OFF-trans.'].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='g', ax=axs, label='ON-OFF-trans.');
df[df['chirp_type']=='mixed'].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='y', ax=axs, label='mixed');
df[df['chirp_type']==np.nan].plot.scatter(x='burst_ratio_ctrl', y='burst_ratio_opto', c='grey', ax=axs, label='NaN');
axs.plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs.transAxes, zorder=-1)
axs.set_title('Burst ratios grouped by chirp type')

plt.legend();
