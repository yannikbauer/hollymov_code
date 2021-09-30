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
import seaborn as sns

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
unit_info = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')
unit_info

# %%
unit_info.keys()

# %% [markdown]
# ## Check OSI/DSI in opto vs control
# NOTES
# - include all duplicate expts for now

# %%
df = unit_info[unit_info['OSI_ctrl'].notna()][['m', 's', 'u', 'OSI_ctrl', 'OSI_opto', 'DSI_ctrl', 'DSI_opto', 'OMI', 'sbc_zscore']]
df

# %% [markdown]
# ### Check OSI/DSI opto vs control against OMI

# %%

# %%
# Plot OSI/DSI opto vs control + OMIs
fig, axs = plt.subplots(1,2, figsize=(12,6))

# OSI
sns.scatterplot(data=df, x='OSI_ctrl', y='OSI_opto', hue='OMI', palette='coolwarm', hue_norm=(-1,1), ax=axs[0]);
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('OSI')

# DSI
sns.scatterplot(data=df, x='DSI_ctrl', y='DSI_opto', hue='OMI', palette='coolwarm', hue_norm=(-1,1), ax=axs[1]);
axs[1].set_title('DSI')
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1);

# %% [markdown]
# ### Check OSI/DSI opto vs control against SbC scores

# %%
# Plot OSI/DSI opto vs control + SbC scores
fig, axs = plt.subplots(1,2, figsize=(12,6))

# Find normalization range
norm = np.mean(df.sbc_zscore.values) + 3 * np.std(df.sbc_zscore.values)
# OSI
sns.scatterplot(data=df, x='OSI_ctrl', y='OSI_opto', hue='sbc_zscore', palette='coolwarm', hue_norm=(-norm,norm), ax=axs[0]);
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('OSI')

# DSI
sns.scatterplot(data=df, x='DSI_ctrl', y='DSI_opto', hue='sbc_zscore', palette='coolwarm', hue_norm=(-norm,norm), ax=axs[1]);
axs[1].set_title('DSI')
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1);

# %% [markdown]
# ### Check OSI/DSI against chirp type

# %%
chirp_df = unit_info[unit_info['chirp_type'].notna()][['m', 's', 'u', 'chirp_type']]
chirp_df

# %%
# Merge chirp type info
df = df.merge(chirp_df, on=['m','s','u'], how='left')
df

# %%
# Plot OSI/DSI opto vs control + SbC scores
fig, axs = plt.subplots(1,2, figsize=(16,8))

# OSI
df[df['chirp_type']=='ON-sust.'].plot.scatter(x='OSI_ctrl', y='OSI_opto', c='r', ax=axs[0], label='ON-sust.');
df[df['chirp_type']=='OFF-sust.'].plot.scatter(x='OSI_ctrl', y='OSI_opto', c='b', ax=axs[0], label='OFF-sust.');
df[df['chirp_type']=='ON-OFF-trans.'].plot.scatter(x='OSI_ctrl', y='OSI_opto', c='g', ax=axs[0], label='ON-OFF-trans.');
df[df['chirp_type']=='mixed'].plot.scatter(x='OSI_ctrl', y='OSI_opto', c='y', ax=axs[0], label='mixed');
df[df['chirp_type']==np.nan].plot.scatter(x='OSI_ctrl', y='OSI_opto', c='grey', ax=axs[0], label='NaN');
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('OSI')


# # DSI
df[df['chirp_type']=='ON-sust.'].plot.scatter(x='DSI_ctrl', y='DSI_opto', c='r', ax=axs[1], label='ON-sust.');
df[df['chirp_type']=='OFF-sust.'].plot.scatter(x='DSI_ctrl', y='DSI_opto', c='b', ax=axs[1], label='OFF-sust.');
df[df['chirp_type']=='ON-OFF-trans.'].plot.scatter(x='DSI_ctrl', y='DSI_opto', c='g', ax=axs[1], label='ON-OFF-trans.');
df[df['chirp_type']=='mixed'].plot.scatter(x='DSI_ctrl', y='DSI_opto', c='y', ax=axs[1], label='mixed');
df[df['chirp_type']==np.nan].plot.scatter(x='DSI_ctrl', y='DSI_opto', c='grey', ax=axs[1], label='NaN');
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('DSI')

plt.legend();

# %% [markdown]
# ## Check OSI DSI per unit against hmov model prediction quality - are high OSI/DSI cells harder to predict?
# NOTES
# - analysis moved to ana_hmov_X_unit_info
