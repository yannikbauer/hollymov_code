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
# # Analyze hmov model parameters against unit info

# %% [markdown]
# ## TODO

# %% [markdown]
# ## Setup

# %% [markdown]
# ### Start DJD
# Run main.py as interactive (-i) module (-m) ( optionally and remotely (-r))\
# NOTE: any code inside the DJD-executing cell other than the executing line is not allowed

# %%
run -im djd.main -- --dbname=dj_hmov --user=write

# %%
import matplotlib.pyplot as plt
import seaborn as sns

from djd import hmov_models
from djd import hmov_unit
from l6s import l6s_utils # Layer 6 suppression code repo with utility functions for plotting unit overview 

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Check hmov unit model scores against each other

# %%
hmov_df = pd.DataFrame((SplineLNP.Eval() * HmovUnit()).fetch(as_dict=True))
hmov_df

# %%
# Plot scatter plots
fig, axs = plt.subplots(2,3, figsize=(18,10))

hmov_df[hmov_df['spl_paramset']==7].plot.scatter(x='spl_r_train', y='spl_r_test_mean', ax=axs[0,0], label='paramset 7');
hmov_df[hmov_df['spl_paramset']==8].plot.scatter(x='spl_r_train', y='spl_r_test_mean', ax=axs[0,0], label='paramset 8', c='k');
axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('SLNP Test vs Train prediction scores')

hmov_df[(hmov_df['spl_fev'] < 200) & (hmov_df['spl_fev'] > -40) & (hmov_df['spl_paramset']==7)].plot.scatter(x='spl_r_test_mean', y='spl_fev', ax=axs[0,1], label='paramset 7');
hmov_df[(hmov_df['spl_fev'] < 200) & (hmov_df['spl_fev'] > -40) & (hmov_df['spl_paramset']==8)].plot.scatter(x='spl_r_test_mean', y='spl_fev', ax=axs[0,1], label='paramset 8', c='k');
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('SLNP Test prediction vs FEV scores')

hmov_df[hmov_df['spl_paramset']==7].plot.scatter(x='spl_rf_area', y='spl_rf_qi', ax=axs[0,2], label='paramset 7');
hmov_df[hmov_df['spl_paramset']==8].plot.scatter(x='spl_rf_area', y='spl_rf_qi', ax=axs[0,2], label='paramset 8', c='k');
axs[0,2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,2].transAxes, zorder=-1)
axs[0,2].set_title('SLNP area vs RF QI')

hmov_df[hmov_df['spl_paramset']==7].plot.scatter(x='spl_rf_area', y='spl_r_test_mean', ax=axs[1,0], label='paramset 7');
hmov_df[hmov_df['spl_paramset']==8].plot.scatter(x='spl_rf_area', y='spl_r_test_mean', ax=axs[1,0], label='paramset 8', c='k');
axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1)
axs[1,0].set_title('SLNP area vs test prediction scores');

hmov_df[hmov_df['spl_paramset']==7].plot.scatter(x='spl_r_test_mean', y='spl_rf_qi', ax=axs[1,1], label='paramset 7');
hmov_df[hmov_df['spl_paramset']==8].plot.scatter(x='spl_r_test_mean', y='spl_rf_qi', ax=axs[1,1], label='paramset 8', c='k');
axs[1,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,1].transAxes, zorder=-1)
axs[1,1].set_title('SLNP test prediction scores vs RF QI');

hmov_df[hmov_df['spl_paramset']==7].plot.scatter(x='hmu_fr_mean_e', y='spl_r_test_mean', ax=axs[1,2], label='paramset 7');
hmov_df[hmov_df['spl_paramset']==8].plot.scatter(x='hmu_fr_mean_e', y='spl_r_test_mean', ax=axs[1,2], label='paramset 8', c='k');
axs[1,2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,2].transAxes, zorder=-1)
axs[1,2].set_title('SLNP test prediction scores vs mean FRs (exp)');


# axs[1,2].set_axis_off()

plt.legend();

# %% [markdown]
# ## Check hmov unit parameters

# %%
hmov_df.keys()

# %%
# Plot hmov unit parameters
fig, axs = plt.subplots(3,4, figsize=(24,18))

# axs[0,0].set(xscale='log', yscale='log')
sns.scatterplot(data=hmov_df, x='hmu_fr_mean_e', y='hmu_fr_var_e', hue='hmu_omi_e', ax=axs[0,0])
axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('Mean exp FR vs mean exp var')

sns.scatterplot(data=hmov_df, x='hmu_fr_mean_stim_ctrl', y='hmu_fr_mean_stim_opto', hue='hmu_omi_stim', ax=axs[0,1])
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('Mean stim FR control vs mean stim FR opto')

sns.scatterplot(data=hmov_df, x='hmu_fr_mean_spont_ctrl', y='hmu_fr_mean_spont_opto', hue='hmu_omi_spont', ax=axs[0,2])
axs[0,2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,2].transAxes, zorder=-1)
axs[0,2].set_title('Mean spont FR control vs mean spont FR opto')

sns.scatterplot(data=hmov_df[hmov_df.hmu_fr_var_spont_ctrl <= 50], x='hmu_fr_var_spont_ctrl', y='hmu_fr_var_spont_opto', hue='hmu_omi_spont', ax=axs[0,3])
axs[0,3].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,3].transAxes, zorder=-1)
axs[0,3].set_title('spont FR var control vs spont FR var opto')



sns.scatterplot(data=hmov_df, x='hmu_fr_mean_stim_ctrl', y='hmu_fr_mean_spont_ctrl', hue='hmu_omi_spont', ax=axs[1,0])
axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1)
axs[1,0].set_title('Mean stim FR control vs mean spont FR ctrl')

sns.scatterplot(data=hmov_df, x='hmu_fr_mean_stim_opto', y='hmu_fr_mean_spont_opto', hue='hmu_omi_spont', ax=axs[1,1])
axs[1,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,1].transAxes, zorder=-1)
axs[1,1].set_title('Mean stim FR opto vs mean spont FR opto')

sns.scatterplot(data=hmov_df, x='hmu_omi_stim', y='hmu_omi_spont', hue='hmu_fr_mean_e', ax=axs[1,2])
axs[1,2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,2].transAxes, zorder=-1)
axs[1,2].set_title('FR OMI stim vs spont')
axs[1,2].set_xlim([-1,1])
axs[1,2].set_ylim([-1,1])

sns.scatterplot(data=hmov_df, x='hmu_fr_mean_e', y='spl_r_test_mean', hue='hmu_oracle', ax=axs[1,3])
axs[1,3].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,3].transAxes, zorder=-1)
axs[1,3].set_title('Mean exp FR opto vs test prediction score')
# axs[1,3].set_axis_off()



sns.scatterplot(data=hmov_df, x='hmu_explainable_var', y='hmu_oracle', hue='hmu_fr_mean_e', ax=axs[2,0])
axs[2,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2,0].transAxes, zorder=-1)
axs[2,0].set_title('Explainable variance vs Oracle score')

sns.scatterplot(data=hmov_df, x='hmu_explainable_var', y='hmu_oracle', hue='hmu_fr_var_e', ax=axs[2,1])
axs[2,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2,1].transAxes, zorder=-1)
axs[2,1].set_title('Explainable variance vs Oracle score')

sns.scatterplot(data=hmov_df, x='hmu_explainable_var', y='hmu_oracle', hue='spl_r_test_mean', ax=axs[2,2])
axs[2,2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2,2].transAxes, zorder=-1)
axs[2,2].set_title('Explainable variance vs Oracle score')

sns.scatterplot(data=hmov_df, x='hmu_explainable_var', y='hmu_oracle', hue='spl_rf_qi', ax=axs[2,3])
axs[2,3].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2,3].transAxes, zorder=-1)
axs[2,3].set_title('Explainable variance vs Oracle score')

# axs[2,3].set_axis_off()

# %% [markdown]
# ### Plot all vars against one another

# %%
hmov_df.keys()

# %%
hmov_df2 = hmov_df[['spl_r_train', 'spl_r_test_mean', 'spl_fev', 'spl_rf_qi', 'spl_rf_thresh', 'spl_rf_area', 'hmu_fr_mean_e',
       'hmu_fr_var_e', 'hmu_fr_mean_stim', 'hmu_fr_mean_stim_ctrl', 'hmu_fr_var_stim_ctrl', 'hmu_fr_mean_stim_opto', 'hmu_fr_var_stim_opto', 'hmu_fr_mean_spont_ctrl', 'hmu_fr_var_spont_ctrl',
       'hmu_fr_mean_spont_opto', 'hmu_fr_var_spont_opto', 'hmu_omi_e', 'hmu_omi_stim', 'hmu_omi_spont', 'hmu_oracle', 'hmu_explainable_var']]

# %%
sns.pairplot(hmov_df2)

# %% [markdown]
# # Check hmov model scores against unit info

# %% [markdown]
# ## Get unit info df

# %%
# Get unit info df
# unit_info = l6s_utils.get_combined_unit_info(load_df_name='unit_info_20201214')
unit_info = l6s_utils.get_combined_unit_info(load_df_name='unit_info_20210129')
unit_info

# %%
unit_info.keys()

# %% [markdown]
# ## Check hmov model prediction quality against OSI/DSI - are high OSI/DSI cells harder to predict?
# NOTES
# - OSI/DSI are mseu-specific, i.e. per experiment > choose best expt to get to msu level
# - model evaluation criteria are mseup-specific, i.e. per unit-parameterset > use get_best_model() to get to msu level

# %%
# Reduce unit_info to OSI and DSI info
df = unit_info[unit_info['OSI_ctrl'].notna()][['m','s','u', 'OSI_ctrl', 'OSI_opto', 'DSI_ctrl', 'DSI_opto', 'sbc_zscore']]
df

# %%
# Choose best OSI-value per unit (in case of duplicate experiments)
best_exp_idx = []
for i, group in df.groupby(['m','s','u']):
    best_exp_idx.append(group['OSI_ctrl'].idxmax())

df = df.loc[best_exp_idx]
df

# %%
# Add chirp type to df
chirp_df = unit_info[unit_info['chirp_type'].notna()][['m', 's', 'u', 'chirp_type']]
chirp_df

# %%
# Merge chirp type info
df = df.merge(chirp_df, on=['m','s','u'], how='left')
df

# %%
# Get SplineLNP model prediction evaluation scores for selected units
splnp = pd.DataFrame((SplineLNP.Eval() & df).fetch(dj.key, 'spl_r_test_mean', 'spl_rf_area', 'spl_rf_thresh', 'spl_rf_val', 'spl_rf_pos_pix', as_dict=True))
splnp

# %%
# Choose best model per unit (in case of duplicates)
# NOTE: can now use functino get_best_model()
best_idx = []
for i, group in splnp.groupby(['m','s','u']):
    best_idx.append(group['spl_r_test_mean'].idxmax())

splnp = splnp.loc[best_idx]
splnp = splnp.drop('e', axis=1)
splnp

# %%
# Merge Spline LNP model scores into OSI/DSI df
df = df.merge(splnp, on=['m','s','u'], how='inner')
df

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction vs RF area
fig, axs = plt.subplots(2,2, figsize=(12,12), dpi=90)

# OSI
sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', size='spl_rf_area', hue='spl_rf_area', ax=axs[0,0])
axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('OSI vs model prediction vs area')

# DSI
sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', size='spl_rf_area', hue='spl_rf_area', ax=axs[0,1])
axs[0,1].set_title('DSI vs model prediction vs area')
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1);


# OSI
sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', size='spl_rf_area', hue='spl_rf_val', palette='coolwarm', ax=axs[1,0])
axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1)
axs[1,0].set_title('OSI vs model prediction vs area vs polarity')

# DSI
sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', size='spl_rf_area', hue='spl_rf_val', palette='coolwarm', ax=axs[1,1])
axs[1,1].set_title('DSI vs model prediction vs area vs polarity')
axs[1,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,1].transAxes, zorder=-1);

# %% [markdown]
# ### Check hmov model X OSI/DSI X chirp_type
# NOTE: NaN chirp types are likely low SNR cells that would not pass quality threshold

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction by chirp type
# NOTE: using seaborn seems more efficient than having to hard code each type or looping through the df.groupby('chirp_type')
fig, axs = plt.subplots(2,3, figsize=(18,12), sharex=False, sharey=False)


sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', color='grey', alpha=0.25, ax=axs[0,0], label='NaN')
sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', hue='chirp_type', ax=axs[0,0])
axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('OSI vs model prediction by chirp type')
axs[0,0].set_xlim(-0.1,1)
axs[0,0].set_ylim(-0.05,0.8)

# axs[0,1].get_shared_x_axes().join(axs[0,0], axs[0,1])
sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', color='grey',alpha=0.25, ax=axs[0,1], label='NaN')
sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', hue='chirp_type', ax=axs[0,1])
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('DSI vs model prediction by chirp type')
axs[0,1].set_xlim(-0.1,1)
axs[0,1].set_ylim(-0.05,0.8)
# axs[0,1] = axs[0,0].twinx()


sns.violinplot(data=df, x='chirp_type', y='spl_r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=df, x='chirp_type', y='spl_r_test_mean', color='white', edgecolor='gray', alpha=0.5, ax=axs[0,2])
axs[0,2].set_ylim(-0.05,0.8)

sns.violinplot(data=df, x='OSI_ctrl', y='chirp_type', inner='quartile', orient='h', ax=axs[1,0])
sns.swarmplot(data=df, x='OSI_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, ax=axs[1,0])
axs[1,0].set_xlim(-0.1,1)

sns.violinplot(data=df, x='DSI_ctrl', y='chirp_type', inner='quartile', orient='h', ax=axs[1,1])
sns.swarmplot(data=df, x='DSI_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, ax=axs[1,1])
axs[1,1].set_xlim(-0.1,1)
axs[1,1].set_yticklabels('')
axs[1,1].set_ylabel('')

axs[1,2].set_axis_off()


# %% [markdown]
# ### Check hmov model X OSI/DSI X mouse and series - check for batch effects

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction by mouse
fig, axs = plt.subplots(1,2, figsize=(12,6))

sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', hue='m', ax=axs[0])
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('OSI vs model prediction by mouse')

sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', hue='m', ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('DSI vs model prediction by mouse')

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction by series
fig, axs = plt.subplots(1,2, figsize=(12,6))

sns.scatterplot(data=df, x='OSI_ctrl', y='spl_r_test_mean', hue='m', palette='bright', style='s', ax=axs[0])
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('OSI vs model prediction by series')

sns.scatterplot(data=df, x='DSI_ctrl', y='spl_r_test_mean', hue='m', palette='bright',style='s', ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('DSI vs model prediction by series')

# %% [markdown]
# ## Check hmov model prediction quality against SbC zscores

# %%
# Reduce unit_info to OSI and DSI info
df = unit_info[unit_info['sbc_zscore'].notna()][['m','s','u','sbc_zscore']]
df

# %%
# Merge Spline LNP model scores into SbC df
df = df.merge(splnp, on=['m','s','u'], how='inner')
df

# %%
# Merge chirp type info
df = df.merge(chirp_df, on=['m','s','u'], how='left')
df

# %%
# Plot scatter plot of SbC score vs model prediction
df.plot.scatter(x='spl_r_test_mean', y='sbc_zscore');
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('SbC score vs model prediction')

# %%
df['sbc_zscore'].plot.hist()

# %%
# Check if SbC score histogram is fine now
sns.histplot(data=df, x='sbc_zscore', hue='chirp_type', element='step', bins=40)

# %%
# Plot scatter plot of SbC score vs model prediction (and chirp type)
fig, axs = plt.subplots(2,2, figsize=(12,12))

df.plot.scatter(x='sbc_zscore', y='spl_r_test_mean', ax=axs[0,0]);
axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('SbC score vs model prediction')

sns.scatterplot(data=df, x='sbc_zscore', y='spl_r_test_mean', ax=axs[0,1], color='grey', label='NaN')
sns.scatterplot(data=df, x='sbc_zscore', y='spl_r_test_mean', hue='chirp_type', ax=axs[0,1])
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('SbC score vs model prediction by chirp type')

sns.histplot(data=df, x='sbc_zscore', element='step', ax=axs[1,0])#, bins=40)
# sns.histplot(data=df[(df.chirp_type=='ON-sust.') | (df.chirp_type=='OFF-sust.')],
#              x='sbc_zscore', hue='chirp_type', element='step', ax=axs[1,1])#, bins=40)
sns.histplot(data=df, x='sbc_zscore', hue='chirp_type', element='step', ax=axs[1,1])#, bins=40)
# sns.kdeplot(data=df, x='sbc_zscore', hue='chirp_type', ax=axs[1,1])#, bins=40)

# %% [markdown]
# ## Check SbCs X area X polarity X chirp type - do SbCs have large areas and negative polarity and are they OFF-sust. cells?

# %%
df

# %%
# Plot scatter plot of SbC score vs area vs polarity vs chirp type
fig, axs = plt.subplots(1,3, figsize=(18,5))

df.plot.scatter(x='sbc_zscore', y='spl_rf_area', ax=axs[0]);
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('SbC score vs model RF area');

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_area', hue='spl_rf_val', palette='coolwarm', ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('SbC score vs model RF area vs polarity');

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_area', hue='chirp_type', ax=axs[2])
axs[2].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[2].transAxes, zorder=-1)
axs[2].set_title('SbC score vs model prediction by chirp type')

# %%
# Plot scatter plot of SbC score vs area
fig, axs = plt.subplots(1,2, figsize=(12,6))
# plt.subplots_adjust(wspace=1)

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_val', size='spl_rf_area', ax=axs[0])
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('SbC score vs model RF polarity vs area');

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_val', color='grey', alpha=0.25, ax=axs[1])
sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_val', size='spl_rf_area', hue='chirp_type', ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('SbC score vs model RF polarity vs area');
axs[1].legend(loc='center left', bbox_to_anchor=(1., 0.5), ncol=1)
# axs[2].set_axis_off()



# %%
# Plot scatter plot of SbC score vs area
fig, axs = plt.subplots(2,3, figsize=(12,8), dpi=90, sharey=False, gridspec_kw={'width_ratios': [0.5, 1, 0.5], 'height_ratios': [1, 0.5]})
# plt.subplots_adjust(wspace=1)

axs[0,0].set_axis_off()

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_val', color='grey', label='NaN', alpha=0.25, ax=axs[0,1])
sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_val', size='spl_rf_area', hue='chirp_type', ax=axs[0,1])
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('SbC score vs model RF polarity vs area');
axs[0,1].legend(loc='center right', bbox_to_anchor=(-0.25, 0.5), ncol=1)
axs[0,1].set_ylim([-0.75, 0.75])
axs[0,1].set_xlim([-27, 18])

# sns.histplot(data=df, y='spl_rf_val', hue='chirp_type', element='step', ax=axs[2])#, bins=40)
sns.kdeplot(data=df, y='spl_rf_val', hue='chirp_type', fill=False, alpha=1, ax=axs[0,2])#, bins=40)
axs[0,2].legend([],[], frameon=False)
axs[0,2].set_ylabel('')
axs[0,2].set_ylim([-0.75, 0.75])
# plt.tight_layout()

axs[1,0].set_axis_off()

sns.kdeplot(data=df, x='sbc_zscore', hue='chirp_type', ax=axs[1,1])#, bins=40)
axs[1,1].set_xlim([-27, 18])
axs[1,1].set_ylabel('')
axs[1,1].legend([],[], frameon=False)

axs[1,2].set_axis_off()

# %%
# Plot scatter plot of SbC score vs area
fig, axs = plt.subplots(1,2, figsize=(12,5))

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_thresh', size='spl_rf_area', ax=axs[0])
axs[0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0].transAxes, zorder=-1)
axs[0].set_title('SbC score vs model RF polarity vs area');

sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_thresh', color='grey', alpha=0.25, ax=axs[1])
sns.scatterplot(data=df, x='sbc_zscore', y='spl_rf_thresh', size='spl_rf_area', hue='chirp_type', ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1].transAxes, zorder=-1)
axs[1].set_title('SbC score vs model RF polarity vs area');
axs[1].legend(loc='center left', bbox_to_anchor=(1., 0.5), ncol=1)
# axs[2].set_axis_off()

# %%
# Plot histograms of RF polarity vs chirp type
fig, axs = plt.subplots(1,3, figsize=(18,5))

sns.histplot(data=df, x='spl_rf_thresh', hue='chirp_type', element='step', ax=axs[0])#, bins=40)

sns.histplot(data=df[(df.chirp_type=='ON-sust.') | (df.chirp_type=='OFF-sust.')],
             x='spl_rf_thresh', hue='chirp_type', element='step', ax=axs[1])#, bins=40)

sns.histplot(data=df[df.chirp_type=='ON-OFF-trans.'], x='spl_rf_thresh', color='b', alpha=0.25, element='step', label='ON-OFF-trans.', ax=axs[2])#, bins=40)
sns.histplot(data=df[df.chirp_type=='ON-sust.'], x='spl_rf_thresh', color='g', element='step', label='ON-sust.', ax=axs[2])#, bins=40)
sns.histplot(data=df[df.chirp_type=='OFF-sust.'], x='spl_rf_thresh', color='r', element='step', label='OFF-sust.', ax=axs[2])#, bins=40)
# sns.histplot(data=df[df.chirp_type=='mixed'], x='spl_rf_thresh', color='y', element='step', label='mixed', ax=axs[2])#, bins=40)
plt.legend();

# %%
# Plot histograms of SbC zscore vs chirp type
fig, axs = plt.subplots(1,3, figsize=(18,5))

sns.histplot(data=df[(df.chirp_type=='ON-sust.') | (df.chirp_type=='OFF-sust.')],
             x='sbc_zscore', hue='chirp_type', element='step', ax=axs[0])#, bins=40)

sns.histplot(data=df[df.chirp_type=='ON-sust.'], x='sbc_zscore', color='g', element='step', label='ON-sust.', ax=axs[1])#, bins=40)
sns.histplot(data=df[df.chirp_type=='OFF-sust.'], x='sbc_zscore', color='r', element='step', label='OFF-sust.', ax=axs[1])#, bins=40)
plt.legend()

sns.histplot(data=df[df.chirp_type=='ON-OFF-trans.'], x='sbc_zscore', color='b', alpha=0.25, element='step', label='ON-OFF-trans.', ax=axs[2])#, bins=40)
sns.histplot(data=df[df.chirp_type=='ON-sust.'], x='sbc_zscore', color='g', element='step', label='ON-sust.', ax=axs[2])#, bins=40)
sns.histplot(data=df[df.chirp_type=='OFF-sust.'], x='sbc_zscore', color='r', element='step', label='OFF-sust.', ax=axs[2])#, bins=40)
# sns.histplot(data=df[df.chirp_type=='mixed'], x='spl_rf_thresh', color='y', element='step', label='mixed', ax=axs[1])#, bins=40)
plt.legend()

# %%
