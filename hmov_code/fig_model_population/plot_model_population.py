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
# # Plot model population analysis
# Code includes:
# - Fig 3 panel a: model type performance overview: comparing performance with or without certain model filters for opto, run and eye data
# - Fig 3 panel b: population filters
#
# The figure panels are manually stored in the GDrive paper folder 'Hmov_L6S_paper/fig_sources/' and then inserted via Adobe Illustrator into Hmov_L6S_paper/figs/fig_03.ai

# %% [markdown]
# ## TODO

# %% [markdown]
# ## Setup

# %%
run -im djd.main -- --dbname=dj_lisa --user=write

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import seaborn as sns

# from djd.hmov_models import _get_data
# from djd.hmov_unit import plot_multi_traces
from djd.glms import get_best_model, plot_model
from djd.plot import cm2inch

# Automatically reload modules to get code changes without restarting kernel
# NOTE: Does not work for DJD table modules
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ### Set plot parameters

# %%
## Update plot parameters
# Option 1: Update general pars from modified matplotlibrc file
# plt.rcParams.update(mpl.rc_params_from_file('../../matplotlibrc', fail_on_error=False, use_default_template=True))

# Option 2: Dynamically update general pars (use if not updating from modified matplotlibrc)
plt.rcParams.update({
    'figure.dpi': 150,
    'figure.max_open_warning': 0, 
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'axes.labelsize': 'medium',
    'font.sans-serif': ['Arial'],
    'pdf.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    'ps.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    })


# Dynamically update plot-specific pars
plt.rcParams.update({
    'font.size': 8,
    'axes.labelsize': 7.0,
    'axes.titlesize': 8,
    'legend.fontsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,    
    })


# %%
# Make figure directory unless it already exists
fig_dir = os.path.join(os.getcwd(), 'figs')  # os.path.dirname(__file__) gives DJD path
if not os.path.exists(fig_dir):
    print(f"Making figure save directory: {fig_dir}")
    os.makedirs(fig_dir)

# %% [markdown]
# ## Plot model type performance overview
# - dimensions
#   - old Fig2 version: 
#     - row_length=2.75, col_length=3.375
#     - makes 6.75 x 11 cm
#   - vertical Fig3 version: 
#     - row_length=3.75, col_length=3.75
#     - makes 7.5 x 15 cm

# %%
# Select units
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

fig, axs = SplineLNP().plot_performance_overview(keys=keys_crit, pshf_config=False, eval_metric='r', 
                                                 colors=None, num_cols=2, row_length=3.75, col_length=3.75,
                                                 verbose=True, add_first_subplot_space=0.3)
# fig.savefig('./figs/model_performance_overview_vert.pdf')

# %%
# Select units
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

fig, axs = SplineLNP().plot_performance_overview(keys=keys_crit, pshf_config=False, eval_metric='r', 
                                                 colors=None, num_cols=2, row_length=3.75, col_length=3.75,
                                                 verbose=True, add_first_subplot_space=0.3)
fig.savefig('./figs/model_performance_overview_vert.pdf')

# %%
fig, axs = SplineLNP().plot_performance_overview(keys=None, pshf_config=False, eval_metric='r', 
                                                 colors=None, num_cols=4, row_length=2.75, col_length=3.375,
                                                 verbose=True, add_first_subplot_space=0.3)
fig.savefig('./figs/model_performance_overview_horiz.pdf')

# %% [markdown]
# ## Plot model population filters
# - dimensions
#   - old Fig2 version: 
#     - figsize=(3.25, 4.5)
#   - vertical Fig3 version: 
#     - figsize=(4, 3.5)

# %% [markdown]
# ### Opto filters

# %% [markdown]
# #### Test diff opto filter lengths

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper = -0.2
thresh_lower = -1.0
fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='omi',
                                                                     filter_len=15,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='omi',
                                                                     filter_len=20,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()

# fig.savefig('./figs/model_population_filters_opto_02.pdf')

# %% [markdown]
# #### Opto filters for plot

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper = -0.2
thresh_lower = -1.0
fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='omi',
                                                                     filter_len=15,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(4, 3.5),
                                                                     leg_yshift=-0.18)


fig.savefig('./figs/model_population_filters_opto_02.pdf')

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper = -0.2
thresh_lower = -1.0
fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='omi',
                                                                     filter_len=15,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))


fig.savefig('./figs/model_population_filters_opto.pdf')

# %% [markdown]
# ### Run filters

# %% [markdown]
# #### Test diff run filter lengths

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper=1.0
thresh_lower=0.2

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=20,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=30,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=40,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=50,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
plt.show()
# fig.savefig('./figs/model_population_filters_run.pdf')

# %% [markdown]
# #### Run filters for plot

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper=1.0
thresh_lower=0.2

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=20,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(4, 3.5),
                                                                     leg_yshift=-0.18)
fig.savefig('./figs/model_population_filters_run_02.pdf')

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper=1.0
thresh_lower=0.2

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='rmi',
                                                                     filter_len=20,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
fig.savefig('./figs/model_population_filters_run.pdf')

# %% [markdown]
# ### Eye filters

# %% [markdown]
# #### Eye filters for plot

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper=1.0
thresh_lower=0.35


fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(mi_kind='emi',
                                                                     filter_len=40,
                                                                     thresh_lower=thresh_lower,
                                                                     thresh_upper=thresh_upper,                                                                      
                                                                     zrange=[-.1, .1], 
                                                                     keys=keys_crit,                                                                                                                                          
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True,
                                                                     figsize=(3.25, 4.5))
fig.savefig('./figs/model_population_filters_eye.pdf')

# %% [markdown]
# ## Plot model parameters

# %% [markdown]
# ### Get model parameters

# %%
# Select units: get keys of units meeting selection criteria
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)
keys_crit = pd.DataFrame(keys_crit)
print('N units passing selection criteria =', len(keys_crit))

# Get best model key for each unit (must be full model with opto+run+eye)
keys_bestm = get_best_model(keys_crit, model_type='SplineLNP', crit='spl_r_val', groupby=['m','s','u'],
                            opto_config='True', opto_len='_', run_config='True', run_len='_',
                            eye_config='True', eye_len='_', pshf_config='False', paramset_ids=None,
                            key_only=True, format='df', verbose=True)

# Get unit info for best models
df = pd.DataFrame((SplineLNP.Eval() * SplineLNPParams() & keys_bestm
                  ).fetch(dj.key, 'spl_rf_area', 'spl_rf_val', 'spl_lambda', as_dict=True))
df.rename(columns={'spl_rf_area': 'rf_area', 'spl_rf_val': 'rf_polarity', 'spl_lambda': 'regularization'}, inplace=True)
df

# %% [markdown]
# ### Plot RF area in one violinplot

# %%
fig, ax = plt.subplots(1,1,figsize=cm2inch((4.14, 3.44)), constrained_layout=True)
sns.violinplot(data=df, y='rf_area', color='white', bw=.3, ax=ax)#,)
sns.swarmplot(data=df, y='rf_area', hue='regularization', x=[""]*len(df), size=3, alpha=0.6, palette='Reds', ax=ax)
ax.set_ylabel('Receptive field area (deg$^2$)')
ax.legend(frameon=False, title='$\lambda$', markerscale=0.5, bbox_to_anchor= (0.6, 1))
sns.despine()
fig.patch.set_facecolor('white')

print(df[['rf_area']].agg(['median', 'mean', 'std', 'count']))

fig.savefig('./figs/model_population_rf_area.pdf')

# %% [markdown]
# ### Plot RF area split by regularization

# %%
import matplotlib.colors

colormap = 'husl'
sns_cmap = sns.color_palette(colormap, 8).as_hex()
cmap = matplotlib.colors.ListedColormap(sns_cmap)

fig, ax = plt.subplots(1,1,figsize=(3,3), dpi=150)
sns.violinplot(data=df, x='regularization', y='rf_area', palette=sns_cmap, inner="stick", bw=.2, ax=ax)
ax.set_ylabel('Receptive field area (deg2)')
ax.set_xlabel('Regularization constant')

sns.despine()

fig.patch.set_facecolor('white')

print(df[['rf_area']].groupby(df['regularization']).agg(['median', 'mean', 'std', 'count']))

#fig.savefig('./plots/RF_area_vs_reg_const.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), transparent=False)

# %% [markdown]
# ### Plot RF polarity

# %%
fig, ax = plt.subplots(1,1,figsize=cm2inch((4.14, 3.44)), constrained_layout=True)
sns.violinplot(data=df, y='rf_polarity', color='white', inner='quartiles', bw=.3, ax=ax)#,)
sns.swarmplot(data=df, y='rf_polarity', hue='rf_polarity', x=[""]*len(df), size=3, alpha=0.7, palette='coolwarm_r', 
              vmin=-1, vmax=1, ax=ax)
ax.set_ylabel('Receptive field polarity')
# ax.legend(frameon=False, title='$\lambda$', markerscale=0.5, bbox_to_anchor= (0.6, 1))
ax.legend([],[], frameon=False)
sns.despine()
fig.patch.set_facecolor('white')

print(df[['rf_polarity']].agg(['median', 'mean', 'std', 'count']))

fig.savefig('./figs/model_population_rf_polarity.pdf')

# %% [markdown]
# ### Plot RF area and polarity combined in one figure

# %%
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=cm2inch((4.5, 7)), constrained_layout=True)

# RF area
sns.violinplot(data=df, y='rf_area', color='white', bw=.3, ax=axs[0])
sns.swarmplot(data=df, y='rf_area', hue='regularization', x=[""]*len(df), size=3, alpha=0.6, palette='Reds', ax=axs[0])
axs[0].set_ylabel('Receptive field area (deg$^2$)')
axs[0].legend(frameon=False, title='$\lambda$', markerscale=0.5, bbox_to_anchor= (0.6, 1))

# RF polarity
sns.violinplot(data=df, y='rf_polarity', color='white', inner='quartiles', bw=.3, ax=axs[1])
sns.swarmplot(data=df, y='rf_polarity', hue='rf_polarity', x=[""]*len(df), size=3, alpha=0.7, palette='coolwarm_r', 
              vmin=-1, vmax=1.5, ax=axs[1])
axs[1].set_ylabel('Receptive field polarity')
axs[1].legend([],[], frameon=False)
sns.despine()
fig.patch.set_facecolor('white')

print(df[['rf_area', 'rf_polarity']].agg(['median', 'mean', 'std', 'count']))

fig.savefig('./figs/model_population_rf_params.pdf')

# %% [markdown]
# ## TESTING: Get tRF full width half max FWHM
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html

# %%
# Get model weights = stRFs
df = pd.DataFrame((SplineLNP() & keys_bestm).fetch(dj.key, 'spl_w_opt', as_dict=True))
df

# %%
# Extract tRFs
from djd.glms import get_strf_comps  # gets stRF components from model weights

# Get tRF for one good example unit model
strf = df.iloc[2].spl_w_opt  
sRF, tRF = get_strf_comps(strf)
plt.plot(tRF)

# %%
# Apply get_strf_comps() to all models, returning only tRFs (2nd arg)
df['tRF'] = df['spl_w_opt'].apply(lambda x: get_strf_comps(x)[1])  # lambda allows to select fn return arg by idx
plt.plot(df.iloc[2].tRF)

# %% [markdown]
# ### Find width OPTION 1

# %%
# Find peaks
import scipy

# This finds multiple peaks and returns properties if width kwarg is given
peaks, properties = scipy.signal.find_peaks(tRF, height=None, threshold=None, distance=None, 
                                            prominence=None, width=1, wlen=None, rel_height=0.5, plateau_size=None)

# %%
peaks

# %%
properties

# %%
# Use prominences to extract highest peak
maxidx = properties['prominences'].argmax()
width = properties['widths'][maxidx]
width

# %% [markdown]
# ### Find width OPTION 2 - more direct

# %%
maxpeak = np.array([tRF.argmax()])
maxpeak

# %%
width, w_height, lips, rips = scipy.signal.peak_widths(tRF, maxpeak, rel_height=0.5, prominence_data=None, wlen=None)

# %%
(lips + (rips - lips)/2)[0]

# %%
plt.plot(tRF)
plt.plot(maxpeak, tRF[maxpeak], "x")
plt.hlines(w_height, lips, rips, color="C1", linestyle='--')
plt.annotate(f'w = {width[0]:.2f}', ((lips + (rips - lips)/2)[0], w_height-0.05), va='top', ha='center')

# %%
# Apply width function to all models ...

# Convert width into actual time (ms) ...
