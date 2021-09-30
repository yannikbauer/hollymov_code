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
# # Analyze hmov unit and model info against unit info dataframes from other experiments

# %% [markdown]
# ## TODO
# - restrict to dLGN
# - for OMI: exclude control mouse (m_genotype='-/-')

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
import warnings
warnings.filterwarnings("ignore")

from djd import hmov_models
from djd import hmov_unit
from djd.hmov_models import get_best_model
from djd.plot import cm2inch
from l6s import l6s_utils # Layer 6 suppression code repo with utility functions for plotting unit overview 

# %%
# %load_ext autoreload
# %autoreload 2

# %%
# Dynamically update general pars (use if not updating from modified matplotlibrc)
plt.rcParams.update({
    'figure.dpi': 150,
    'axes.labelsize': 'large',    
    'figure.max_open_warning': 0, 
    'font.sans-serif': ['Arial'],
    'pdf.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    'ps.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    })

# %% [markdown]
# # HmovUnit() parameters

# %% [markdown]
# ## Get HmovUnit df

# %%
# Create Hmov Unit DataFrame
hmovu_df = HmovUnit().df
hmovu_df.columns = hmovu_df.columns.str.replace(r'hmu_', '')  # rmv prefix 'hmu_' and 'hm_' from column names (better than lstrip)
hmovu_df.columns = hmovu_df.columns.str.replace(r'hm_', '')

# Add genotype info
genotype = pd.DataFrame(Mouse().fetch(dj.key, 'm_genotype', as_dict=True))
hmovu_df = hmovu_df.merge(genotype, on='m', how='left')
# hmovu_df = hmovu_df[hmovu_df.m_genotype=='+/-']  # optionally restrict to Ntsr1-Cre pos mice

# Add region info
region = pd.DataFrame(Series().fetch(dj.key, 's_region', as_dict=True))
hmovu_df = hmovu_df.merge(region, on=['m', 's'], how='left')
hmovu_df = hmovu_df[hmovu_df.s_region=='LGN']  # optionally restrict to LGN

hmovu_df

# %%
hmovu_df.columns

# %% [markdown]
# ## HmovUnit mean firing rates (FR)
# - stimulus vs spontaneous period and opto vs control

# %%
# Plot firing rate scatter plots
# fig, axs = plt.subplots(1,4, figsize=(25,10), sharex=True, sharey=False)
fig, axs = plt.subplots(1,4, figsize=cm2inch((55,25)), dpi=150, sharex=True, sharey=False)
for ax in axs: ax.set_aspect('equal')

# hmovu_df.plot.scatter(x='fr_mean_stim_ctrl', y='fr_mean_stim_opto', hue='omi_stim', ax=axs[0]);
sns.scatterplot(data=hmovu_df, x='fr_mean_stim_ctrl', y='fr_mean_stim_opto', hue='omi_stim', palette='RdBu', style='m_genotype', ax=axs[0])#, hue_norm=(-0.15,0.15))
sns.scatterplot(data=hmovu_df, x='fr_mean_spont_ctrl', y='fr_mean_spont_opto', hue='omi_spont', palette='RdBu', style='m_genotype', ax=axs[1])
sns.scatterplot(data=hmovu_df, x='fr_mean_spont_ctrl', y='fr_mean_stim_ctrl', hue='omi_e', palette='RdBu', style='m_genotype', ax=axs[2])
sns.scatterplot(data=hmovu_df, x='fr_mean_spont_opto', y='fr_mean_stim_opto', hue='omi_e', palette='RdBu', style='m_genotype', ax=axs[3])

# axs[0].set_ylim(axs[0].get_xlim())
axs[0].set_ylim([0,40])
axs[0].set_xlim([0,40])
axs[1].set_ylim(axs[0].get_ylim())
axs[2].set_ylim(axs[0].get_ylim())
axs[3].set_ylim(axs[0].get_ylim())

for ax in axs: ax.plot([0, 1], [0, 1], color='grey', linestyle='--', transform=ax.transAxes, zorder=-1)
# for ax in axs: ax.plot([0, 40], [0, 40], color='grey', linestyle='--', zorder=-1)

# %% [markdown]
# ## HmovUnit FR variance

# %%
hmovu_df.columns

# %%
# Plot scatter plots
# fig, axs = plt.subplots(1,4, figsize=(25,10), sharex=True, sharey=False)
fig, axs = plt.subplots(1,4, figsize=cm2inch((55,10)), dpi=150, sharex=False, sharey=False)
# for ax in axs: ax.set_aspect('equal')

# hmovu_df.plot.scatter(x='fr_mean_stim_ctrl', y='fr_mean_stim_opto', hue='omi_stim', ax=axs[0]);
sns.scatterplot(data=hmovu_df, x='fr_mean_e', y='fr_var_e', hue='omi_stim', palette='RdBu', style='m_genotype', ax=axs[0]) # hue_norm=(-1,1)
sns.scatterplot(data=hmovu_df, x='fr_var_stim_ctrl', y='fr_var_stim_opto', hue='omi_spont', palette='RdBu', style='m_genotype', ax=axs[1])
axs[1].set_aspect('equal')
sns.scatterplot(data=hmovu_df, x='fr_var_spont_ctrl', y='fr_var_spont_opto', hue='omi_e', palette='RdBu', style='m_genotype', ax=axs[2])
axs[2].set_xlim([0,20])
axs[2].set_ylim([0,20])
axs[2].set_aspect('equal')
sns.scatterplot(data=hmovu_df, x='fr_var_e', y='explainable_var', hue='omi_e', palette='RdBu', style='m_genotype', ax=axs[3])

# sns.scatterplot(data=hmovu_df, x='fr_mean_spont_opto', y='fr_mean_stim_opto', hue='omi_e', palette='RdBu', style='m_genotype', ax=axs[3])

# axs[0].set_ylim(axs[1].get_ylim())
# axs[2].set_ylim(axs[1].get_ylim())
# axs[3].set_ylim(axs[1].get_ylim())

for ax in axs: ax.plot([0, 1], [0, 1], color='grey', linestyle='--', transform=ax.transAxes, zorder=-1)

# %% [markdown]
# ## HmovUnit OMIs

# %%
hmovu_df.columns

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,3, figsize=cm2inch((30,10)), dpi=100, sharex=True)#, , figsize=cm2inch((55,25)), dpi=100figsize=cm2inch((55,25)), dpi=100, sharex=True, sharey=False)
for ax in axs: ax.set_aspect('equal')

sns.scatterplot(data=hmovu_df, x='omi_stim', y='omi_spont', hue='fr_mean_e', style='m_genotype', ax=axs[0]) # hue_norm=(-1,1)
axs[0].set_xlim(axs[0].get_ylim())

sns.scatterplot(data=hmovu_df, x='omi_e', y='omi_stim', hue='fr_mean_e', style='m_genotype', ax=axs[1]) # hue_norm=(-1,1)
axs[1].set_ylim(axs[1].get_xlim())

sns.scatterplot(data=hmovu_df, x='omi_e', y='omi_spont', hue='fr_mean_e', style='m_genotype', ax=axs[2]) # hue_norm=(-1,1)

for ax in axs: ax.plot([0, 1], [0, 1], color='grey', linestyle='--', transform=ax.transAxes, zorder=-1)

fig.tight_layout()

# %% [markdown]
# ## HmovUnit explainable variance and oracle score

# %%
hmovu_df.columns

# %%
# fig, axs = plt.subplots(1,1, dpi=100)#, , figsize=cm2inch((55,25)), dpi=100figsize=cm2inch((55,25)), dpi=100, sharex=True, sharey=False)
fig, axs = plt.subplots(1,3, figsize=cm2inch((35,10)), dpi=100)
sns.scatterplot(data=hmovu_df, x='explainable_var', y='oracle', hue='m_genotype', ax=axs[0])
sns.scatterplot(data=hmovu_df, x='explainable_var', y='oracle', hue='fr_mean_e', style='m_genotype', ax=axs[1])
sns.scatterplot(data=hmovu_df, x='explainable_var', y='fr_mean_e', hue='oracle', style='m_genotype', ax=axs[2]) # hue_norm=(-1,1)

# %% [markdown]
# ## HmovUnit RMI

# %%
fig, axs = plt.subplots(1,3, figsize=cm2inch((35,10)), dpi=100)
sns.scatterplot(data=hmovu_df, x='rmi_e', y='fr_mean_e', hue='m_genotype', ax=axs[0])
sns.scatterplot(data=hmovu_df, x='rmi_e', y='omi_e', hue='m_genotype', ax=axs[1])
sns.scatterplot(data=hmovu_df, x='rmi_e', y='explainable_var', hue='m_genotype', ax=axs[2])

# %% [markdown]
# # SplineLNP() model parameters
# - parameters against one another

# %%
# df = pd.DataFrame((SplineLNP.Eval() * HmovUnit()).fetch(as_dict=True))
slnp_df = pd.DataFrame((SplineLNP.Eval()).fetch(as_dict=True))
slnp_df.columns = slnp_df.columns.str.replace(r'spl_', '')  # rmv prefixes from column names (better than lstrip)
slnp_df.columns = slnp_df.columns.str.replace(r'hmu_', '')
slnp_df.columns = slnp_df.columns.str.replace(r'hm_', '')

# Add genotype info
genotype = pd.DataFrame(Mouse().fetch(dj.key, 'm_genotype', as_dict=True))
slnp_df = slnp_df.merge(genotype, on='m', how='left')
# slnp_df = slnp_dfslnp_df[slnp_df.m_genotype=='+/-']  # optionally restrict to Ntsr1-Cre pos mice

# Add region info
region = pd.DataFrame(Series().fetch(dj.key, 's_region', as_dict=True))
slnp_df = slnp_df.merge(region, on=['m', 's'], how='left')
slnp_df = slnp_df[slnp_df.s_region=='LGN']  # optionally restrict to LGN

slnp_df

# %%
slnp_df.columns

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,2, figsize=cm2inch((25,10)), dpi=100)

i = 0
s = sns.scatterplot(data=slnp_df, x='r_train', y='r_test_mean', hue='paramset', palette='tab10', alpha=0.75, ax=axs[i])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')#, ncol=1)
axs[i].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')
axs[i].set_aspect('equal')

i=1
s = sns.scatterplot(data=slnp_df, x='r2_train', y='r2_test_mean', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[i])
axs[i].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')

fig.tight_layout()

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,3, figsize=cm2inch((33,10)), dpi=100)

s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='fev', hue='paramset', palette='tab10', alpha=0.75, ax=axs[0])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')
s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='rf_qi', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')
s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[2])
fig.tight_layout()

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,5, figsize=cm2inch((50,10)), dpi=100)

s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, ax=axs[0])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')
s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_thresh', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[1])
s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_val', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[2])
s = sns.scatterplot(data=slnp_df, x='rf_val', y='rf_thresh', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[3])
s = sns.scatterplot(data=slnp_df, x='rf_val', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[4])

fig.tight_layout()

# %%
hmov_df.columns

# %% [markdown]
# ## Optionally get best SLNP model per unit and re-check parameters

# %%
# Toggle whether or not to reduce models to only best model 
only_best_model = True

if only_best_model:
    slnp_df = get_best_model(slnp_df, model_type='SplineLNP', crit='spl_r_test_mean', groupby=['m','s','u'],
                        opto_config='_', run_config='_', eye_config='_', pshf_config='_',
                        keys_only=False, format='df', verbose=False)
    slnp_df.columns = slnp_df.columns.str.replace(r'spl_', '')  # rmv prefixes from column names (better than lstrip)
    slnp_df.columns = slnp_df.columns.str.replace(r'hmu_', '')
    slnp_df.columns = slnp_df.columns.str.replace(r'hm_', '')
slnp_df

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,2, figsize=cm2inch((25,10)), dpi=100)

i = 0
s = sns.scatterplot(data=slnp_df, x='r_train', y='r_test_mean', hue='paramset', palette='tab10', alpha=0.75, ax=axs[i])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')#, ncol=1)
axs[i].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')
axs[i].set_aspect('equal')

i=1
s = sns.scatterplot(data=slnp_df, x='r2_train', y='r2_test_mean', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[i])
axs[i].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')

fig.tight_layout()

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,3, figsize=cm2inch((33,10)), dpi=100)

s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='fev', hue='paramset', palette='tab10', alpha=0.75, ax=axs[0])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')
s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='rf_qi', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[1])
axs[1].plot([0, 1], [0, 1], color='k', alpha=0.75, linestyle='--')
s = sns.scatterplot(data=slnp_df, x='r_test_mean', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[2])
fig.tight_layout()

# %%
# Plot scatter plots
fig, axs = plt.subplots(1,5, figsize=cm2inch((50,10)), dpi=100)

s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, ax=axs[0])
s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='paramset')
s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_thresh', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[1])
s = sns.scatterplot(data=slnp_df, x='rf_qi', y='rf_val', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[2])
s = sns.scatterplot(data=slnp_df, x='rf_val', y='rf_thresh', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[3])
s = sns.scatterplot(data=slnp_df, x='rf_val', y='rf_area', hue='paramset', palette='tab10', alpha=0.75, legend=False, ax=axs[4])

fig.tight_layout()

# %% [markdown]
# # SplineLNP() model parameters against unit info df

# %% [markdown]
# ## Prepare data

# %% [markdown]
# ### Get unit-experiment info df (mseu) and reduce to unit-wise info (msu)
# This unit-experiment info df was previously computed based on unit respones to other stimuli (e.g. chirp, oriTun, conTun) to obtain unit typing into ON/OFF/trans/sust, OSI/DSI, and SbC.
# This unit-exp info is reduced to unit-wise info by removing potential duplicate experiments for units (and taking the best experiment only), and applying certain unit selection criteria (defaults and/or manual)

# %%
# Get unit-exp info df
unitexp_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unitexp_info_20210521')
unitexp_info_df

# %%
unitexp_info_df.keys()

# %%
# Reduce unitexp info to unit-wise info
unit_info_df = l6s_utils.reduce_unitexp2unit_info(unitexp_info_df, sbc_class_stim='oriTun',
                                                  apply_crit=True, default_crit=True, 
                                                  manual_crit={'all': {'s_region': 'LGN',
#                                                                'm_genotype': '+/-',
                                                               }})
unit_info_df

# %%
unit_info_df.keys()

# %% [markdown]
# ### Merge unit info with HmovUnit() df and SplineLNP() df to creat single unit df

# %% jupyter={"outputs_hidden": true}
hmovu_df

# %%
hmovu_df.keys()

# %% jupyter={"outputs_hidden": true}
slnp_df

# %%
slnp_df.keys()

# %%
unit_info_df.drop(['m_genotype', 's_region'], axis=1, inplace=True)  # already in hmovu_df 
unit_info_df

# %%
# Check which unit entries are missing in respective dfs. Reasons include:
# - in unit_info_df but not in hmovu_df: early units do not have hmov recordings
# - in slnp_df but not in hmovu_df: slnp_df might contain V1 units unless excluded
# - in hmovu_df but not in slnp_df: units could not be fitted
df1 = unit_info_df.merge(hmovu_df, how='outer', indicator=True)#.loc[lambda x : x['_merge']=='left_only']
df2 = slnp_df.merge(hmovu_df, how='outer', indicator=True)#.loc[lambda x : x['_merge']=='left_only']
df1[0:50]

# %%
udf = unit_info_df.merge(hmovu_df, on=['m','s','u'])  # default: how='inner'
udf

# %%
udf = udf.merge(slnp_df, on=['m','s','e','u'])
udf

# %%
udf.keys()

# %% [markdown]
# ## Hmov model X OSI/DSI
# - prediction quality (r_test_mean): 
#   - are OS/DS cells harder to predict?
# - RF quality (rf_qi):
#   - Do OS/DS cells have lower rf_qi?
# - other RF properties e.g. rf_area, rf_val, rf_pos_pix
#   - do OS/DS cells differ on any?
#
# Non-model parameters
# - oracle: do OS/DS cells have higher-lower oracles scores?
# - rmi: are OS/DS cells more run-modulated?
# - mean FR: do they have higher/lower FRs?
# - omi: are OS/DS cells more/less opto-modulated?
# - chirp_type: are OS/DS cells over-/underrepresented in a particular chirp type?
#
# TODO: try using all models (not just best) to boost n

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction vs RF area
fig, axs = plt.subplots(nrows=9, ncols=2, figsize=cm2inch((20,70)), dpi=110)

# OSI/DSI vs r_test_mean
s = sns.scatterplot(data=udf, x='osi_ctrl', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[0,0])
axs[0,0].set_title('OSI vs prediction score vs area vs polarity')
# axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[0,1])
axs[0,1].set_title('DSI vs prediction score vs area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))#, title='paramset')#, ncol=1)


# OSI/DSI vs RF quality
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[1,0])
axs[1,0].set_title('OSI vs RF quality vs area vs polarity')
# axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1);

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[1,1])
axs[1,1].set_title('DSI vs RF quality vs area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF val
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[2,0])
axs[2,0].set_title('OSI vs RF polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[2,1])
axs[2,1].set_title('DSI vs RF polarity vs area')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF area
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[3,0])
axs[3,0].set_title('OSI vs RF area vs polarity')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[3,1])
axs[3,1].set_title('DSI vs RF area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='osi_ctrl', palette='flare', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_title('OSI vs RF position vs area')
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')

s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='dsi_ctrl', palette='flare', ax=axs[4,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='osi_ctrl')#, ncol=1)
l.get_title().set_position((20, 0))
axs[4,1].set_title('DSI vs RF position vs area')
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')


# OSI/DSI vs oracle
s = sns.scatterplot(data=udf, x='osi_ctrl', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[5,0])
axs[5,0].set_title('OSI vs oracle vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[5,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[5,1].set_title('DSI vs oracle vs polarity vs area')


# OSI/DSI vs RMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[6,0])
axs[6,0].set_title('OSI vs RMI vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[6,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[6,1].set_title('DSI vs RMI vs polarity vs area')


# OSI/DSI vs OMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[7,0])
axs[7,0].set_title('OSI vs OMI vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[7,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[7,1].set_title('DSI vs OMI vs polarity vs area')


# OSI/DSI vs mean FR
s = sns.scatterplot(data=udf, x='osi_ctrl', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[8,0])
axs[8,0].set_title('OSI vs mean FR vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[8,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[8,1].set_title('DSI vs mean FR vs polarity vs area')


for ax in axs[:,0]: ax.set_xlabel(r'OSI$_{control}$')
for ax in axs[:,1]: ax.set_xlabel(r'DSI$_{control}$')

fig.suptitle('OSI (left) and DSI (right) vs model parameters', y=1.02)
fig.tight_layout()

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction vs RF area
fig, axs = plt.subplots(nrows=9, ncols=2, figsize=cm2inch((20,70)), dpi=110)

# OSI/DSI vs r_test_mean
s = sns.scatterplot(data=udf, x='osi_ctrl', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[0,0])
axs[0,0].set_title('OSI vs prediction score vs area vs polarity')
# axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[0,1])
axs[0,1].set_title('DSI vs prediction score vs area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))#, title='paramset')#, ncol=1)


# OSI/DSI vs RF quality
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[1,0])
axs[1,0].set_title('OSI vs RF quality vs area vs polarity')
# axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1);

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[1,1])
axs[1,1].set_title('DSI vs RF quality vs area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF val
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[2,0])
axs[2,0].set_title('OSI vs RF polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[2,1])
axs[2,1].set_title('DSI vs RF polarity vs area')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF area
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[3,0])
axs[3,0].set_title('OSI vs RF area vs polarity')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', ax=axs[3,1])
axs[3,1].set_title('DSI vs RF area vs polarity')
s.legend(loc='center left', bbox_to_anchor=(1., 0.5))


# OSI/DSI vs RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='osi_ctrl', palette='flare', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_title('OSI vs RF position vs area')
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')

s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='dsi_ctrl', palette='flare', ax=axs[4,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5), title='osi_ctrl')#, ncol=1)
l.get_title().set_position((20, 0))
axs[4,1].set_title('DSI vs RF position vs area')
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')


# OSI/DSI vs oracle
s = sns.scatterplot(data=udf, x='osi_ctrl', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[5,0])
axs[5,0].set_title('OSI vs oracle vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[5,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[5,1].set_title('DSI vs oracle vs polarity vs area')


# OSI/DSI vs RMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[6,0])
axs[6,0].set_title('OSI vs RMI vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[6,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[6,1].set_title('DSI vs RMI vs polarity vs area')


# OSI/DSI vs OMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[7,0])
axs[7,0].set_title('OSI vs OMI vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[7,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[7,1].set_title('DSI vs OMI vs polarity vs area')


# OSI/DSI vs mean FR
s = sns.scatterplot(data=udf, x='osi_ctrl', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[8,0])
axs[8,0].set_title('OSI vs mean FR vs polarity vs area')

s = sns.scatterplot(data=udf, x='dsi_ctrl', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[8,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[8,1].set_title('DSI vs mean FR vs polarity vs area')


for ax in axs[:,0]: ax.set_xlabel(r'OSI$_{control}$')
for ax in axs[:,1]: ax.set_xlabel(r'DSI$_{control}$')

fig.suptitle('OSI (left) and DSI (right) vs model parameters', y=1.02)
fig.tight_layout()

# %%
# Get OSI/DSI densities for ON vs OFF cells (by RF polarity = rf_val)
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=cm2inch((20,10)), dpi=100)

# Bottom marginal plots
sns.kdeplot(data=udf[udf.rf_val > 0], x='osi_ctrl', legend=True, label='rf_val > 0', ax=axs[0])
sns.kdeplot(data=udf[udf.rf_val < 0], x='osi_ctrl', legend=True, label='rf_val < 0', ax=axs[0])

sns.kdeplot(data=udf[udf.rf_val > 0], x='dsi_ctrl', legend=True, label='rf_val > 0', ax=axs[1])
s = sns.kdeplot(data=udf[udf.rf_val < 0], x='dsi_ctrl', legend=True, label='rf_val < 0', ax=axs[1])
plt.legend()#loc='center left', bbox_to_anchor=(1., 0.5))

fig.suptitle('OSI/DSI vs RF polarity (rf_val)')

# %%
# Get OSI/DSI densities for ON vs OFF cells (by RF polarity = rf_val)
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=cm2inch((20,10)), dpi=100)

# Bottom marginal plots
sns.kdeplot(data=udf[udf.rf_val > 0], x='osi_ctrl', legend=True, label='rf_val > 0', ax=axs[0])
sns.kdeplot(data=udf[udf.rf_val < 0], x='osi_ctrl', legend=True, label='rf_val < 0', ax=axs[0])

sns.kdeplot(data=udf[udf.rf_val > 0], x='dsi_ctrl', legend=True, label='rf_val > 0', ax=axs[1])
s = sns.kdeplot(data=udf[udf.rf_val < 0], x='dsi_ctrl', legend=True, label='rf_val < 0', ax=axs[1])
plt.legend()#loc='center left', bbox_to_anchor=(1., 0.5))

fig.suptitle('OSI/DSI vs RF polarity (rf_val)')

# %% [markdown]
# ### OSI/DSI opto vs control

# %%
udf.keys()

# %%
# Check OSI/DSI control vs opto (vs OMI and mean FR)
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=cm2inch((28,23)), dpi=100)

axs[0,0].set_aspect('equal')
axs[0,1].set_aspect('equal')
axs[1,0].set_aspect('equal')
axs[1,1].set_aspect('equal')

s = sns.scatterplot(data=udf, x='osi_ctrl', y='osi_opto', hue='omi_e', size='rf_area', style='m_genotype', legend=False, ax=axs[0,0])#, size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[0,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='dsi_opto', hue='omi_e', size='rf_area', style='m_genotype', ax=axs[0,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))#, ncol=3)

s = sns.scatterplot(data=udf, x='osi_ctrl', y='osi_opto', hue='fr_mean_e', size='rf_area', style='m_genotype', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='dsi_opto', hue='fr_mean_e', size='rf_area',  style='m_genotype', ax=axs[1,1])
l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))#, ncol=3)


axs[0,0].set_xlim(axs[0,0].get_ylim())
axs[0,1].set_xlim(axs[0,1].get_ylim())
axs[1,0].set_xlim(axs[1,0].get_ylim())
axs[1,1].set_xlim(axs[1,1].get_ylim())


axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[1,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,0].transAxes, zorder=-1)
axs[1,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[1,1].transAxes, zorder=-1)

fig.tight_layout()

# %% [markdown]
# ### Check for OSI/DSI batch effects

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction by mouse
fig, axs = plt.subplots(1,2, figsize=cm2inch((20,9)), dpi=100)

sns.scatterplot(data=df, x='osi_ctrl', y='r_test_mean', hue='m', style='m_genotype', legend=False, ax=axs[0])
axs[0].set_title('OSI vs model prediction by mouse')

s = sns.scatterplot(data=df, x='dsi_ctrl', y='r_test_mean', hue='m',style='m_genotype', ax=axs[1])
l = s.legend(loc='center left', bbox_to_anchor=[1.0,0.5])
# l = s.legend(loc='center left', bbox_to_anchor=(1., 0.5))
axs[1].set_title('DSI vs model prediction by mouse')

# %% [markdown]
# ### Check units with outlier RF areas

# %%
from djd.hmov_models import plot_rf_filters

# Get unit with large(st) RF area
df = udf.loc[[udf.rf_area.idxmax()]]  # use sort_values to get list
print(len(df))

for i, unit in df.head(n=len(df)).iterrows():
    models = pd.DataFrame((SplineLNP() & unit.loc['m':'u'].to_dict()).fetch(dj.key, as_dict=True))
    key = get_best_model(models, keys_only=True)
    plot_rf_filters(key.to_dict('records')[0], figsize=(16, 5))
    plt.show()

# %% [markdown]
# ## Hmov model X chirp_type
# TODO: try using all models (not just best) to boost n

# %%
udf.keys()

# %%
# Quantify chirp-classified units
# NOTE: NaN chirp types are likely low SNR cells that would not pass quality threshold

print(f'Classified chirp cells: n = {udf["chirp_type"].notna().sum()}')
print(f'Unclassified chirp cells (NaN): n = {udf["chirp_type"].isna().sum()}')

# Show NaNs in plot
df = udf.copy()
df['chirp_type'] = df['chirp_type'].fillna('NaN')

fig, axs = plt.subplots(nrows=1, ncols=1, dpi=90) #figsize=cm2inch((20,70))
ax = sns.countplot(data=df, x='chirp_type', ax=axs)

# %%
# Plot scatter plot of OSI/DSI (control) vs model
fig, axs = plt.subplots(nrows=11, ncols=4, figsize=cm2inch((35,80)), dpi=110)

for r in range(9):  # sharey axis in every row
    if r != 4:
        axs[r,0].get_shared_y_axes().join(axs[r,0], axs[r,1], axs[r,2], axs[r,3])


# r_test_mean
s = sns.scatterplot(data=udf, x='osi_ctrl', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=True, ax=axs[0,0])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='osi_ctrl', y='r_test_mean', color='grey', alpha=0.25, label='NaN', legend=True, ax=axs[0,0])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.5], ncol=2, fontsize=7, markerscale=0.75)
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[0,1])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='dsi_ctrl', y='r_test_mean', color='grey', alpha=0.25, label='NaN', legend=False, ax=axs[0,1])
sns.violinplot(data=udf, x='chirp_type', y='r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='chirp_type', y='r_test_mean', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[0,2])
sns.kdeplot(data=udf, y='r_test_mean', hue='chirp_type', ax=axs[0,3])


# RF quality
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_qi', inner='quartile', ax=axs[1,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_qi', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[1,2])
sns.kdeplot(data=udf, y='rf_qi', hue='chirp_type', legend=False, ax=axs[1,3])


# RF val
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_val', inner='quartile', bw=0.2, ax=axs[2,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_val', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[2,2])
sns.kdeplot(data=udf, y='rf_val', hue='chirp_type',  bw_adjust=0.5, legend=False, ax=axs[2,3])


# RF area
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_area', inner='quartile', ax=axs[3,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_area', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[3,2])
sns.kdeplot(data=udf, y='rf_area', hue='chirp_type', legend=True, ax=axs[3,3])


# RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[4,1])
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')
sns.violinplot(data=udf, x='chirp_type', y=y_pos, inner='quartile', ax=axs[4,2])
sns.swarmplot(data=udf, x='chirp_type', y=y_pos, color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[4,2])
sns.kdeplot(data=udf, y=y_pos, hue='chirp_type', legend=False, ax=axs[4,3])


# oracle
s = sns.scatterplot(data=udf, x='osi_ctrl', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,1])
sns.violinplot(data=udf, x='chirp_type', y='oracle', inner='quartile', ax=axs[5,2])
sns.swarmplot(data=udf, x='chirp_type', y='oracle', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[5,2])
sns.kdeplot(data=udf, y='oracle', hue='chirp_type', legend=False, ax=axs[5,3])


# RMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,1])
sns.violinplot(data=udf, x='chirp_type', y='rmi_e', inner='quartile', ax=axs[6,2])
sns.swarmplot(data=udf, x='chirp_type', y='rmi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[6,2])
sns.kdeplot(data=udf, y='rmi_e', hue='chirp_type', legend=True, ax=axs[6,3])


# OMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,1])
sns.violinplot(data=udf, x='chirp_type', y='omi_e', inner='quartile', ax=axs[7,2])
sns.swarmplot(data=udf, x='chirp_type', y='omi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[7,2])
sns.kdeplot(data=udf, y='omi_e', hue='chirp_type', legend=False, ax=axs[7,3])


# mean FR
s = sns.scatterplot(data=udf, x='osi_ctrl', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,1])
sns.violinplot(data=udf, x='chirp_type', y='fr_mean_e', inner='quartile', ax=axs[8,2])
sns.swarmplot(data=udf, x='chirp_type', y='fr_mean_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[8,2])
sns.kdeplot(data=udf, y='fr_mean_e', hue='chirp_type', legend=False, ax=axs[8,3])

# Bottom marginal plots
sns.violinplot(data=udf, x='osi_ctrl', y='chirp_type', inner='quartile', ax=axs[9,0])
sns.swarmplot(data=udf, x='osi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,0])
sns.kdeplot(data=udf, x='osi_ctrl', hue='chirp_type', legend=False, ax=axs[10,0])
axs[9,0].set_ylabel('')
plt.setp(axs[9,0].get_yticklabels(), rotation=45)

sns.violinplot(data=udf, x='dsi_ctrl', y='chirp_type', inner='quartile', ax=axs[9,1])
sns.swarmplot(data=udf, x='dsi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,1])
sns.kdeplot(data=udf, x='dsi_ctrl', hue='chirp_type', legend=False, ax=axs[10,1])
axs[9,1].set_ylabel('')
plt.setp(axs[9,1].get_yticklabels(), rotation=45)

for ax in axs[:,0]: ax.set_xlabel(r'OSI$_{control}$')
for ax in axs[:,1]: ax.set_xlabel(r'DSI$_{control}$')
for ax in axs[:,2]: ax.set_xlabel('Chirp type')

axs[9,2].set_visible(False)
axs[9,3].set_visible(False)
axs[10,2].set_visible(False)
axs[10,3].set_visible(False)

fig.suptitle('chirp types vs model parameters', y=1.02)
fig.tight_layout()

# %%
# Plot scatter plot of OSI/DSI (control) vs model
fig, axs = plt.subplots(nrows=11, ncols=4, figsize=cm2inch((35,80)), dpi=110)

for r in range(9):  # sharey axis in every row
    if r != 4:
        axs[r,0].get_shared_y_axes().join(axs[r,0], axs[r,1], axs[r,2], axs[r,3])


# r_test_mean
s = sns.scatterplot(data=udf, x='osi_ctrl', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=True, ax=axs[0,0])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='osi_ctrl', y='r_test_mean', color='grey', alpha=0.25, label='NaN', legend=True, ax=axs[0,0])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.5], ncol=2, fontsize=7, markerscale=0.75)
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[0,1])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='dsi_ctrl', y='r_test_mean', color='grey', alpha=0.25, label='NaN', legend=False, ax=axs[0,1])
sns.violinplot(data=udf, x='chirp_type', y='r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='chirp_type', y='r_test_mean', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[0,2])
sns.kdeplot(data=udf, y='r_test_mean', hue='chirp_type', ax=axs[0,3])


# RF quality
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_qi', inner='quartile', ax=axs[1,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_qi', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[1,2])
sns.kdeplot(data=udf, y='rf_qi', hue='chirp_type', legend=False, ax=axs[1,3])


# RF val
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_val', inner='quartile', bw=0.2, ax=axs[2,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_val', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[2,2])
sns.kdeplot(data=udf, y='rf_val', hue='chirp_type',  bw_adjust=0.5, legend=False, ax=axs[2,3])


# RF area
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,1])
sns.violinplot(data=udf, x='chirp_type', y='rf_area', inner='quartile', ax=axs[3,2])
sns.swarmplot(data=udf, x='chirp_type', y='rf_area', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[3,2])
sns.kdeplot(data=udf, y='rf_area', hue='chirp_type', legend=True, ax=axs[3,3])


# RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[4,1])
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')
sns.violinplot(data=udf, x='chirp_type', y=y_pos, inner='quartile', ax=axs[4,2])
sns.swarmplot(data=udf, x='chirp_type', y=y_pos, color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[4,2])
sns.kdeplot(data=udf, y=y_pos, hue='chirp_type', legend=False, ax=axs[4,3])


# oracle
s = sns.scatterplot(data=udf, x='osi_ctrl', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,1])
sns.violinplot(data=udf, x='chirp_type', y='oracle', inner='quartile', ax=axs[5,2])
sns.swarmplot(data=udf, x='chirp_type', y='oracle', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[5,2])
sns.kdeplot(data=udf, y='oracle', hue='chirp_type', legend=False, ax=axs[5,3])


# RMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,1])
sns.violinplot(data=udf, x='chirp_type', y='rmi_e', inner='quartile', ax=axs[6,2])
sns.swarmplot(data=udf, x='chirp_type', y='rmi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[6,2])
sns.kdeplot(data=udf, y='rmi_e', hue='chirp_type', legend=True, ax=axs[6,3])


# OMI
s = sns.scatterplot(data=udf, x='osi_ctrl', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,1])
sns.violinplot(data=udf, x='chirp_type', y='omi_e', inner='quartile', ax=axs[7,2])
sns.swarmplot(data=udf, x='chirp_type', y='omi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[7,2])
sns.kdeplot(data=udf, y='omi_e', hue='chirp_type', legend=False, ax=axs[7,3])


# mean FR
s = sns.scatterplot(data=udf, x='osi_ctrl', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,0])
s = sns.scatterplot(data=udf, x='dsi_ctrl', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,1])
sns.violinplot(data=udf, x='chirp_type', y='fr_mean_e', inner='quartile', ax=axs[8,2])
sns.swarmplot(data=udf, x='chirp_type', y='fr_mean_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[8,2])
sns.kdeplot(data=udf, y='fr_mean_e', hue='chirp_type', legend=False, ax=axs[8,3])

# Bottom marginal plots
sns.violinplot(data=udf, x='osi_ctrl', y='chirp_type', inner='quartile', ax=axs[9,0])
sns.swarmplot(data=udf, x='osi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,0])
sns.kdeplot(data=udf, x='osi_ctrl', hue='chirp_type', legend=False, ax=axs[10,0])
axs[9,0].set_ylabel('')
plt.setp(axs[9,0].get_yticklabels(), rotation=45)

sns.violinplot(data=udf, x='dsi_ctrl', y='chirp_type', inner='quartile', ax=axs[9,1])
sns.swarmplot(data=udf, x='dsi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,1])
sns.kdeplot(data=udf, x='dsi_ctrl', hue='chirp_type', legend=False, ax=axs[10,1])
axs[9,1].set_ylabel('')
plt.setp(axs[9,1].get_yticklabels(), rotation=45)

for ax in axs[:,0]: ax.set_xlabel(r'OSI$_{control}$')
for ax in axs[:,1]: ax.set_xlabel(r'DSI$_{control}$')
for ax in axs[:,2]: ax.set_xlabel('Chirp type')

axs[9,2].set_visible(False)
axs[9,3].set_visible(False)
axs[10,2].set_visible(False)
axs[10,3].set_visible(False)

fig.suptitle('chirp types vs model parameters', y=1.02)
fig.tight_layout()

# %% [markdown]
# ### Check outlier polarity units
# - OFF-sust. and RF polarity > 0
# - ON-sust. and RF polarity < 0

# %%
df = udf[(udf.chirp_type=='ON-sust.') & (udf.rf_val < 0)]
df.iloc[-1]

# %%
from djd.hmov_models import plot_RF, plot_rf_filters

# Check ON-sust units with a negative RF polarity
df = udf[(udf.chirp_type=='ON-sust.') & (udf.rf_val < 0)]
print(len(df))

for i, unit in df.head(n=len(df)).iterrows():
    models = pd.DataFrame((SplineLNP() & unit.loc['m':'u'].to_dict()).fetch(dj.key, as_dict=True))
    key = get_best_model(models, keys_only=True)
    plot_rf_filters(key.to_dict('records')[0], figsize=(16, 5))
    plt.show()

# %%
from djd.hmov_models import plot_RF, plot_rf_filters

# Check OFF-sust units with a positive RF polarity
df = udf[(udf.chirp_type=='OFF-sust.') & (udf.rf_val > 0)]
print(len(df))

for i, unit in df.head(n=len(df)).iterrows():
    models = pd.DataFrame((SplineLNP() & unit.loc['m':'u'].to_dict()).fetch(dj.key, as_dict=True))
    key = get_best_model(models, keys_only=True)
    plot_rf_filters(key.to_dict('records')[0], figsize=(16, 5))
    plt.show()


# %%

# %% [markdown]
# ### Focus on one variable

# %%
# Plot scatter plot of OSI/DSI (control) vs model prediction by chirp type
# NOTE: using seaborn seems more efficient than having to hard code each type or looping through the df.groupby('chirp_type')
fig, axs = plt.subplots(2,3, figsize=cm2inch((35,22)), dpi=80, sharex=False, sharey=False)

var = 'r_test_mean'

sns.scatterplot(data=udf, x='osi_ctrl', y=var, hue='chirp_type', ax=axs[0,0])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='osi_ctrl', y=var, color='grey', alpha=0.25, label='NaN', ax=axs[0,0])
# axs[0,0].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,0].transAxes, zorder=-1)
axs[0,0].set_title('OSI vs model by chirp type')
# axs[0,0].set_xlim(-0.1,1)
# axs[0,0].set_ylim(-0.05,0.8)

# axs[0,1].get_shared_x_axes().join(axs[0,0], axs[0,1])
sns.scatterplot(data=udf, x='dsi_ctrl', y=var, hue='chirp_type', legend=False, ax=axs[0,1])
sns.scatterplot(data=udf[udf.chirp_type.isna()], x='dsi_ctrl', y=var, color='grey', alpha=0.25, label='NaN', legend=False, ax=axs[0,1])
# axs[0,1].plot([0, 1], [0, 1], color='grey', linestyle='--', transform=axs[0,1].transAxes, zorder=-1)
axs[0,1].set_title('DSI vs model by chirp type')
# axs[0,1].set_xlim(-0.1,1)
# axs[0,1].set_ylim(-0.05,0.8)
# axs[0,1] = axs[0,0].twinx()

axs[0,2].get_shared_y_axes().join(axs[0,0], axs[0,1], axs[0,2])
sns.violinplot(data=udf, x='chirp_type', y=var, inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='chirp_type', y=var, color='white', edgecolor='gray', alpha=0.5, ax=axs[0,2])
# axs[0,2].set_ylim(-0.05,0.8)

axs[1,0].get_shared_x_axes().join(axs[0,0], axs[1,0])
sns.violinplot(data=udf, x='osi_ctrl', y='chirp_type', inner='quartile', orient='h', ax=axs[1,0])
sns.swarmplot(data=udf, x='osi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, ax=axs[1,0])
# axs[1,0].set_xlim(-0.1,1)

axs[1,1].get_shared_x_axes().join(axs[0,1], axs[1,1])
sns.violinplot(data=udf, x='dsi_ctrl', y='chirp_type', inner='quartile', orient='h', ax=axs[1,1])
sns.swarmplot(data=udf, x='dsi_ctrl', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, ax=axs[1,1])
# axs[1,1].set_xlim(-0.1,1)
axs[1,1].set_yticklabels('')
axs[1,1].set_ylabel('')

axs[1,2].set_axis_off()

fig.tight_layout()


# %% [markdown]
# ## Hmov model X SbC zscores
# - simple histogram of SbC scores
# - histogram split by chirp type
# - same plot as above for chirp only for SbC types?
#   - should be possible: could even use left column for RF polarity and right for chirp types
# - categorical split by 'sbc' column?
#
# TODO: try sbc-scores from oriTun

# %%
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=cm2inch((27,8)), dpi=100, sharex=False, sharey=False)

print(f'SbC cells: n = {len(udf[udf.sbc==True])}')  # alt: udf.query('sbc==True')
print(f'Other cells: n = {len(udf[udf.sbc==False])}')
print(f'SbC NaN: n = {len(udf[udf.sbc_zscore.isna()])}')

sns.countplot(data=udf, x='sbc', ax=axs[0])
sns.histplot(data=udf, x='sbc_zscore', element='step', bins=40, legend=True, ax=axs[1])
line = axs[1].axvline(-1.96, color='r', linestyle=':', label='SbC z-crit')
plt.legend(handles=[line])
# sns.kdeplot(data=udf, x='sbc_zscore', legend=True, ax=axs[0])
sns.kdeplot(data=udf, x='sbc_zscore', hue='chirp_type', legend=True, ax=axs[2])

fig.tight_layout()

# %%
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=cm2inch((27,8)), dpi=100, sharex=False, sharey=False)

print(f'SbC cells: n = {len(udf[udf.sbc==True])}')  # alt: udf.query('sbc==True')
print(f'Other cells: n = {len(udf[udf.sbc==False])}')
print(f'SbC NaN: n = {len(udf[udf.sbc_zscore.isna()])}')

sns.countplot(data=udf, x='sbc', ax=axs[0])
sns.histplot(data=udf, x='sbc_zscore', element='step', bins=40, legend=True, ax=axs[1])
line = axs[1].axvline(-1.96, color='r', linestyle=':', label='SbC z-crit')
plt.legend(handles=[line])
# sns.kdeplot(data=udf, x='sbc_zscore', legend=True, ax=axs[0])
sns.kdeplot(data=udf, x='sbc_zscore', hue='chirp_type', legend=True, ax=axs[2])

fig.tight_layout()

# %%
# Plot scatter plot of SbC score vs model
fig, axs = plt.subplots(nrows=11, ncols=4, figsize=cm2inch((35,80)), dpi=110)

for r in range(9):  # sharey axis in every row
    if r != 4:
        axs[r,0].get_shared_y_axes().join(axs[r,0], axs[r,1], axs[r,2], axs[r,3])


# r_test_mean
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[0,0])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=True, ax=axs[0,1])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
sns.violinplot(data=udf, x='sbc', y='r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='sbc', y='r_test_mean', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[0,2])
s = sns.kdeplot(data=udf, y='r_test_mean', hue='sbc', ax=axs[0,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF quality
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,1])
sns.violinplot(data=udf, x='sbc', y='rf_qi', inner='quartile', ax=axs[1,2])
sns.swarmplot(data=udf, x='sbc', y='rf_qi', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[1,2])
s = sns.kdeplot(data=udf, y='rf_qi', hue='sbc', legend=False, ax=axs[1,3])


# RF val
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[2,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,1])
sns.violinplot(data=udf, x='sbc', y='rf_val', inner='quartile', bw=0.2, ax=axs[2,2])
sns.swarmplot(data=udf, x='sbc', y='rf_val', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[2,2])
s = sns.kdeplot(data=udf, y='rf_val', hue='sbc', legend=False, bw_adjust=0.5, ax=axs[2,3])

# RF area
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[3,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,1])
sns.violinplot(data=udf, x='sbc', y='rf_area', inner='quartile', ax=axs[3,2])
sns.swarmplot(data=udf, x='sbc', y='rf_area', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[3,2])
s = sns.kdeplot(data=udf, y='rf_area', hue='sbc', legend=False, ax=axs[3,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc_zscore',  palette='coolwarm_r', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc', palette='tab10', legend=False, ax=axs[4,1])
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')
sns.violinplot(data=udf, x='sbc', y=y_pos, inner='quartile', ax=axs[4,2])
sns.swarmplot(data=udf, x='sbc', y=y_pos, color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[4,2])
sns.kdeplot(data=udf, y=y_pos, hue='sbc', legend=False, ax=axs[4,3])


# oracle
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[5,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,1])
sns.violinplot(data=udf, x='sbc', y='oracle', inner='quartile', ax=axs[5,2])
sns.swarmplot(data=udf, x='sbc', y='oracle', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[5,2])
s = sns.kdeplot(data=udf, y='oracle', hue='sbc', legend=False, ax=axs[5,3])


# RMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[6,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,1])
sns.violinplot(data=udf, x='sbc', y='rmi_e', inner='quartile', ax=axs[6,2])
sns.swarmplot(data=udf, x='sbc', y='rmi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[6,2])
s = sns.kdeplot(data=udf, y='rmi_e', hue='sbc', legend=False, ax=axs[6,3])
l = s.legend(labels=['SbC','Non-SbC'])

# OMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[7,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,1])
sns.violinplot(data=udf, x='sbc', y='omi_e', inner='quartile', ax=axs[7,2])
sns.swarmplot(data=udf, x='sbc', y='omi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[7,2])
s = sns.kdeplot(data=udf, y='omi_e', hue='sbc', legend=False, ax=axs[7,3])


# mean FR
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[8,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,1])
sns.violinplot(data=udf, x='sbc', y='fr_mean_e', inner='quartile', ax=axs[8,2])
sns.swarmplot(data=udf, x='sbc', y='fr_mean_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[8,2])
s = sns.kdeplot(data=udf, y='fr_mean_e', hue='sbc', legend=False, ax=axs[8,3])


# Bottom marginal plots
sns.kdeplot(data=udf[udf.rf_val > 0], x='sbc_zscore', legend=True, label='rf_val > 0', ax=axs[10,0])
s = sns.kdeplot(data=udf[udf.rf_val < 0], x='sbc_zscore', legend=True, label='rf_val < 0', ax=axs[10,0])
s.legend()

sns.violinplot(data=udf, x='sbc_zscore', y='chirp_type', inner='quartile', ax=axs[9,1])
sns.swarmplot(data=udf, x='sbc_zscore', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,1])
sns.kdeplot(data=udf, x='sbc_zscore', hue='chirp_type', legend=False, ax=axs[10,1])
axs[9,1].set_ylabel('')
plt.setp(axs[9,1].get_yticklabels(), rotation=45)

for ax in axs[:,0]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,1]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,2]: ax.set_xlabel('SbC')

axs[9,0].set_visible(False)
axs[9,2].set_visible(False)
axs[9,3].set_visible(False)
axs[10,2].set_visible(False)
axs[10,3].set_visible(False)

fig.suptitle('SbC vs model parameters', y=1.02)
fig.tight_layout()

# %%
# Plot scatter plot of SbC score vs model
fig, axs = plt.subplots(nrows=11, ncols=4, figsize=cm2inch((35,80)), dpi=110)

for r in range(9):  # sharey axis in every row
    if r != 4:
        axs[r,0].get_shared_y_axes().join(axs[r,0], axs[r,1], axs[r,2], axs[r,3])


# r_test_mean
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[0,0])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=True, ax=axs[0,1])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
sns.violinplot(data=udf, x='sbc', y='r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='sbc', y='r_test_mean', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[0,2])
s = sns.kdeplot(data=udf, y='r_test_mean', hue='sbc', ax=axs[0,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF quality
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,1])
sns.violinplot(data=udf, x='sbc', y='rf_qi', inner='quartile', ax=axs[1,2])
sns.swarmplot(data=udf, x='sbc', y='rf_qi', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[1,2])
s = sns.kdeplot(data=udf, y='rf_qi', hue='sbc', legend=False, ax=axs[1,3])


# RF val
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[2,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,1])
sns.violinplot(data=udf, x='sbc', y='rf_val', inner='quartile', bw=0.2, ax=axs[2,2])
sns.swarmplot(data=udf, x='sbc', y='rf_val', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[2,2])
s = sns.kdeplot(data=udf, y='rf_val', hue='sbc', legend=False, bw_adjust=0.5, ax=axs[2,3])

# RF area
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[3,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,1])
sns.violinplot(data=udf, x='sbc', y='rf_area', inner='quartile', ax=axs[3,2])
sns.swarmplot(data=udf, x='sbc', y='rf_area', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[3,2])
s = sns.kdeplot(data=udf, y='rf_area', hue='sbc', legend=False, ax=axs[3,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc_zscore',  palette='coolwarm_r', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc', palette='tab10', legend=False, ax=axs[4,1])
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')
sns.violinplot(data=udf, x='sbc', y=y_pos, inner='quartile', ax=axs[4,2])
sns.swarmplot(data=udf, x='sbc', y=y_pos, color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[4,2])
sns.kdeplot(data=udf, y=y_pos, hue='sbc', legend=False, ax=axs[4,3])


# oracle
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[5,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,1])
sns.violinplot(data=udf, x='sbc', y='oracle', inner='quartile', ax=axs[5,2])
sns.swarmplot(data=udf, x='sbc', y='oracle', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[5,2])
s = sns.kdeplot(data=udf, y='oracle', hue='sbc', legend=False, ax=axs[5,3])


# RMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[6,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,1])
sns.violinplot(data=udf, x='sbc', y='rmi_e', inner='quartile', ax=axs[6,2])
sns.swarmplot(data=udf, x='sbc', y='rmi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[6,2])
s = sns.kdeplot(data=udf, y='rmi_e', hue='sbc', legend=False, ax=axs[6,3])
l = s.legend(labels=['SbC','Non-SbC'])

# OMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[7,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,1])
sns.violinplot(data=udf, x='sbc', y='omi_e', inner='quartile', ax=axs[7,2])
sns.swarmplot(data=udf, x='sbc', y='omi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[7,2])
s = sns.kdeplot(data=udf, y='omi_e', hue='sbc', legend=False, ax=axs[7,3])


# mean FR
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[8,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,1])
sns.violinplot(data=udf, x='sbc', y='fr_mean_e', inner='quartile', ax=axs[8,2])
sns.swarmplot(data=udf, x='sbc', y='fr_mean_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[8,2])
s = sns.kdeplot(data=udf, y='fr_mean_e', hue='sbc', legend=False, ax=axs[8,3])


# Bottom marginal plots
sns.kdeplot(data=udf[udf.rf_val > 0], x='sbc_zscore', legend=True, label='rf_val > 0', ax=axs[10,0])
s = sns.kdeplot(data=udf[udf.rf_val < 0], x='sbc_zscore', legend=True, label='rf_val < 0', ax=axs[10,0])
s.legend()

sns.violinplot(data=udf, x='sbc_zscore', y='chirp_type', inner='quartile', ax=axs[9,1])
sns.swarmplot(data=udf, x='sbc_zscore', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,1])
sns.kdeplot(data=udf, x='sbc_zscore', hue='chirp_type', legend=False, ax=axs[10,1])
axs[9,1].set_ylabel('')
plt.setp(axs[9,1].get_yticklabels(), rotation=45)

for ax in axs[:,0]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,1]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,2]: ax.set_xlabel('SbC')

axs[9,0].set_visible(False)
axs[9,2].set_visible(False)
axs[9,3].set_visible(False)
axs[10,2].set_visible(False)
axs[10,3].set_visible(False)

fig.suptitle('SbC vs model parameters', y=1.02)
fig.tight_layout()

# %%
# Plot scatter plot of SbC score vs model
fig, axs = plt.subplots(nrows=11, ncols=4, figsize=cm2inch((35,80)), dpi=110)

for r in range(9):  # sharey axis in every row
    if r != 4:
        axs[r,0].get_shared_y_axes().join(axs[r,0], axs[r,1], axs[r,2], axs[r,3])


# r_test_mean
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=True, ax=axs[0,0])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
s = sns.scatterplot(data=udf, x='sbc_zscore', y='r_test_mean', size='rf_area', hue='chirp_type', palette='tab10', legend=True, ax=axs[0,1])
l = s.legend(loc='top left', bbox_to_anchor=[1.0,1.6], ncol=2, fontsize=9, markerscale=0.75)
sns.violinplot(data=udf, x='sbc', y='r_test_mean', inner='quartile', ax=axs[0,2])
sns.swarmplot(data=udf, x='sbc', y='r_test_mean', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[0,2])
s = sns.kdeplot(data=udf, y='r_test_mean', hue='sbc', ax=axs[0,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF quality
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[1,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_qi', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[1,1])
sns.violinplot(data=udf, x='sbc', y='rf_qi', inner='quartile', ax=axs[1,2])
sns.swarmplot(data=udf, x='sbc', y='rf_qi', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[1,2])
s = sns.kdeplot(data=udf, y='rf_qi', hue='sbc', legend=False, ax=axs[1,3])


# RF val
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[2,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_val', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[2,1])
sns.violinplot(data=udf, x='sbc', y='rf_val', inner='quartile', bw=0.2, ax=axs[2,2])
sns.swarmplot(data=udf, x='sbc', y='rf_val', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[2,2])
s = sns.kdeplot(data=udf, y='rf_val', hue='sbc', legend=False, bw_adjust=0.5, ax=axs[2,3])

# RF area
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[3,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rf_area', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[3,1])
sns.violinplot(data=udf, x='sbc', y='rf_area', inner='quartile', ax=axs[3,2])
sns.swarmplot(data=udf, x='sbc', y='rf_area', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[3,2])
s = sns.kdeplot(data=udf, y='rf_area', hue='sbc', legend=False, ax=axs[3,3])
l = s.legend(labels=['SbC','Non-SbC'])


# RF position
x_pos = np.array([x for x,y in udf.rf_pos_pix.values])
y_pos = np.array([y for x,y in udf.rf_pos_pix.values])
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc_zscore',  palette='coolwarm_r', legend=False, ax=axs[4,0])  # crest, rocket_r
axs[4,0].set_xlabel('RF x-pos (pix)')
axs[4,0].set_ylabel('RF y-pos (pix)')
axs[4,0].set_aspect('equal')
s = sns.scatterplot(data=udf, x=x_pos, y=y_pos, size='rf_area', hue='sbc', palette='tab10', legend=False, ax=axs[4,1])
axs[4,1].set_xlabel('RF x-pos (pix)')
axs[4,1].set_ylabel('RF y-pos (pix)')
axs[4,1].set_aspect('equal')
sns.violinplot(data=udf, x='sbc', y=y_pos, inner='quartile', ax=axs[4,2])
sns.swarmplot(data=udf, x='sbc', y=y_pos, color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[4,2])
sns.kdeplot(data=udf, y=y_pos, hue='sbc', legend=False, ax=axs[4,3])


# oracle
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[5,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='oracle', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[5,1])
sns.violinplot(data=udf, x='sbc', y='oracle', inner='quartile', ax=axs[5,2])
sns.swarmplot(data=udf, x='sbc', y='oracle', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[5,2])
s = sns.kdeplot(data=udf, y='oracle', hue='sbc', legend=False, ax=axs[5,3])


# RMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[6,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='rmi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[6,1])
sns.violinplot(data=udf, x='sbc', y='rmi_e', inner='quartile', ax=axs[6,2])
sns.swarmplot(data=udf, x='sbc', y='rmi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[6,2])
s = sns.kdeplot(data=udf, y='rmi_e', hue='sbc', legend=False, ax=axs[6,3])
l = s.legend(labels=['SbC','Non-SbC'])

# OMI
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[7,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='omi_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[7,1])
sns.violinplot(data=udf, x='sbc', y='omi_e', inner='quartile', ax=axs[7,2])
sns.swarmplot(data=udf, x='sbc', y='omi_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[7,2])
s = sns.kdeplot(data=udf, y='omi_e', hue='sbc', legend=False, ax=axs[7,3])


# mean FR
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='rf_val', palette='coolwarm_r', legend=False, ax=axs[8,0])
s = sns.scatterplot(data=udf, x='sbc_zscore', y='fr_mean_e', size='rf_area', hue='chirp_type', palette='tab10', legend=False, ax=axs[8,1])
sns.violinplot(data=udf, x='sbc', y='fr_mean_e', inner='quartile', ax=axs[8,2])
sns.swarmplot(data=udf, x='sbc', y='fr_mean_e', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[8,2])
s = sns.kdeplot(data=udf, y='fr_mean_e', hue='sbc', legend=False, ax=axs[8,3])


# Bottom marginal plots
sns.kdeplot(data=udf[udf.rf_val > 0], x='sbc_zscore', legend=True, label='rf_val > 0', ax=axs[10,0])
s = sns.kdeplot(data=udf[udf.rf_val < 0], x='sbc_zscore', legend=True, label='rf_val < 0', ax=axs[10,0])
s.legend()

sns.violinplot(data=udf, x='sbc_zscore', y='chirp_type', inner='quartile', ax=axs[9,1])
sns.swarmplot(data=udf, x='sbc_zscore', y='chirp_type', color='white', edgecolor='gray', alpha=0.5, size=3.5, ax=axs[9,1])
sns.kdeplot(data=udf, x='sbc_zscore', hue='chirp_type', legend=False, ax=axs[10,1])
axs[9,1].set_ylabel('')
plt.setp(axs[9,1].get_yticklabels(), rotation=45)

for ax in axs[:,0]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,1]: ax.set_xlabel(r'SbC$_{zscore}$')
for ax in axs[:,2]: ax.set_xlabel('SbC')

axs[9,0].set_visible(False)
axs[9,2].set_visible(False)
axs[9,3].set_visible(False)
axs[10,2].set_visible(False)
axs[10,3].set_visible(False)

fig.suptitle('SbC vs model parameters', y=1.02)
fig.tight_layout()

# %%

# %%

# %%

# %% [markdown]
# ### OLD FIGURES (temporary, for comparison)

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

# %% [markdown]
# # Unit info clustering?

# %%
# Check how many full-featured units we have
udf.dropna()  # 10/6/21: 78 rows

# %%
unit_info_df.dropna()

# %%
# Check which columns we have (and which could be dropped for clustering)
udf.keys()

# %%
