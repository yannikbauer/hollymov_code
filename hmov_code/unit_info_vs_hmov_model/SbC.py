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
# # Analyze unit info df: SbCs

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
unit_info = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20210129')
unit_info

# %% [markdown]
# ## Check SbC wave shapes and autocorrellograms

# %%
unit_info.keys()

# %%
# Check how many experiments identified SbCs (includes duplicate expts per unit!)
print(f'SbC proportion estimate: {len(unit_info[unit_info.sbc==True])}/{(len(unit_info[unit_info.sbc==True]) + len(unit_info[unit_info.sbc==False]))}',
      f'({np.round(len(unit_info[unit_info.sbc==True]) / (len(unit_info[unit_info.sbc==True]) + len(unit_info[unit_info.sbc==False])), 3)*100} %)')

# %%
df = unit_info[unit_info['e_name']=='conTun12_opto']

# %%
df = df[df['sbc_zscore'].notna()]

# %%
df.sort_values('sbc_zscore')['sbc_zscore']

# %%
for i, row in df.sort_values('sbc_zscore', ascending=True).head(n=10).iterrows():
    ukey = row.to_dict()
#     print(ukey)
    ukey = {key: value for key, value in ukey.items() if key in ['m','s','e','u','sbc_zscore']}
    print(ukey)
    l6s_utils.plot_ori_con_raster_tun(ukey, stim='conTun')
#     plt.show()

# %%
df = unit_info[unit_info['e_name']=='oriTun12_opto']

# %%
df = df[df['sbc_zscore'].notna()]

# %%
df.sort_values('sbc_zscore')['sbc_zscore']

# %%
for i, row in df.sort_values('sbc_zscore', ascending=True).head(n=10).iterrows():
    ukey = row.to_dict()
#     print(ukey)
    ukey = {key: value for key, value in ukey.items() if key in ['m','s','e','u','sbc_zscore']}
    print(ukey)
    l6s_utils.plot_ori_con_raster_tun(ukey, stim='oriTun')
#     plt.show()

# %%
for i, row in df.sort_values('sbc_zscore', ascending=False).head(n=5).iterrows():
    ukey = row.to_dict()
#     print(ukey)
    ukey = {key: value for key, value in ukey.items() if key in ['m','s','e','u','sbc_zscore']}
    print(ukey)
    l6s_utils.plot_ori_con_raster_tun(ukey, stim='oriTun')
#     plt.show()

# %%
for i, row in df.sort_values('sbc_zscore', ascending=False).head(n=10).iterrows():
    ukey = row.to_dict()
    fig, axs = plt.subplots(1,2)
    (Unit.Properties() & ukey).acorr(ax=axs[0])
    (Unit.Properties() & ukey).plot_wave(ax=axs[1], title=False)
    axs[1].set_title(f'sbc_zcsore: {np.round(ukey["sbc_zscore"], 3)}')
    plt.show()

# %%
for i, row in df.sort_values('sbc_zscore', ascending=True).head(n=10).iterrows():
    ukey = row.to_dict()
    fig, axs = plt.subplots(1,2)
    (Unit.Properties() & ukey).acorr(ax=axs[0])
    (Unit.Properties() & ukey).plot_wave(ax=axs[1], title=False)
    axs[1].set_title(f'sbc_zcsore: {np.round(ukey["sbc_zscore"], 3)}')
    plt.show()

# %%
sbcs = df.sort_values('sbc_zscore', ascending=True).head(n=10)[['m','s','e','u']]
non_sbcs = df.sort_values('sbc_zscore', ascending=False).head(n=10)[['m','s','e','u']]

fig, axs = plt.subplots(1,2, figsize=(12,6))

(Unit.Properties() & sbcs).acorr(ax=axs[0], color='r', alpha=0.05, title=False);
(Unit.Properties() & non_sbcs).acorr(ax=axs[0], color='k', alpha=0.05, title=False);

(Unit.Properties() & sbcs).plot_wave(ax=axs[1], color='r', alpha=0.25, title=False);
(Unit.Properties() & non_sbcs).plot_wave(ax=axs[1], color='k', alpha=0.25, title=False);


# %%
sbcs = df.sort_values('sbc_zscore', ascending=True).head(n=10)[['m','s','e','u']]
non_sbcs = df.sort_values('sbc_zscore', ascending=False).head(n=10)[['m','s','e','u']]

fig, axs = plt.subplots(1,2, figsize=(12,6))

(Unit.Properties() & sbcs).acorr(ax=axs[0], color='r', alpha=0.05, title=False);
(Unit.Properties() & non_sbcs).acorr(ax=axs[1], color='k', alpha=0.05, title=False);
axs[0].set_title('SbC (top 10 by zscore)')
axs[1].set_title('non-SbC (top 10 by zscore)')

# %%
sbcs = df.sort_values('sbc_zscore', ascending=True).head(n=20)[['m','s','e','u']]
non_sbcs = df.sort_values('sbc_zscore', ascending=False).head(n=20)[['m','s','e','u']]

fig, axs = plt.subplots(1,2, figsize=(12,6))

(Unit.Properties() & sbcs).acorr(ax=axs[0], color='r', alpha=0.05, title=False);
(Unit.Properties() & non_sbcs).acorr(ax=axs[1], color='k', alpha=0.05, title=False);
axs[0].set_title('SbC (top 20 by zscore)')
axs[1].set_title('non-SbC (top 20 by zscore)')

# %%
sbcs = df.sort_values('sbc_zscore', ascending=True).head(n=20)[['m','s','e','u']]
non_sbcs = df.sort_values('sbc_zscore', ascending=False).head(n=20)[['m','s','e','u']]

fig, axs = plt.subplots(1, figsize=(8,8))

(Unit.Properties() & sbcs).plot_wave(ax=axs, color='r', alpha=0.2, title=False);
(Unit.Properties() & non_sbcs).plot_wave(ax=axs, color='k', alpha=0.2, title=False);
axs.set_title('red: SbC, black: non-SbC (top 20 by zscore)');

# %%

# %%
