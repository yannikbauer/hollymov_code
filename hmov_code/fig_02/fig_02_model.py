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
# # Plot Fig 2 model panels
# Code includes:
# - panel b: example model fits to  (one subpanel per unit-model)
# - panel c: model type performance overview: comparing performance with or without certain model filters for opto, run and eye data
#
# Code excludes:
# - panel a: model diagram: this was generated in Adobe Illustrator
#
# The figure panels are manually stored in the paper repo under 'Hmov_L6S_paper/fig_sources/' and then inserted via Adobe Illustrator into Hmov_L6S_paper/figs/fig_02.ai

# %% [markdown]
# ## Setup

# %%
run -im djd.main -- --dbname=dj_lisa --user=write

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# from djd.hmov_models import _get_data
# from djd.hmov_unit import plot_multi_traces
from djd.glms import get_best_model, plot_model

# Automatically reload modules to get code changes without restarting kernel
# NOTE: Does not work for DJD table modules
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Plot some model example units to check for good candidates

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r2_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %%
for i, key in modkeys.iterrows():
#     print(key)
    key = key.to_dict()
    fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %% [markdown]
# ## Plot model example units for Fig 2

# %%
## Update plot parameters
# Option 1: Update general pars from modified matplotlibrc file
plt.rcParams.update(mpl.rc_params_from_file('../../matplotlibrc', fail_on_error=False, use_default_template=True))

# Option 2: Dynamically update general pars (use if not updating from modified matplotlibrc)
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.max_open_warning': 0, 
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'axes.labelsize': 'medium',
    'font.sans-serif': ['Arial'],
    'pdf.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    'ps.fonttype': 42, # make text editable (otherwise saved as non-text path/shape)
    })


# Dynamically update plot-specific pars
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.max_open_warning': 0, 
    'axes.labelsize': 7.0,
    'axes.titlesize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,    
    })


# %%
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 example cell
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

fig.savefig('foo.pdf')#, format='pdf')

# %%
# Define unit key
# Define example unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}#, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 example cell
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

fig.savefig('foo2.pdf')#, format='pdf')

# %%
HmovUnit() & {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}#, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 example cell
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

fig.savefig('foo3.pdf')#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}#, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 example cell
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# Lisa's suggestions
ukey = {'m':'Ntsr1Cre_2019_0007', 's':6, 'e':9,  'u': 7}
# ukey = {'m':'Ntsr1Cre_2019_0007', 's':3, 'e':7,  'u': 5}
# ukey = {'m':'Ntsr1Cre_2019_0008', 's':3, 'e':7,  'u':14}

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'True', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# fig.savefig('foo3.pdf')#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}#, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 example cell
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# Lisa's suggestions
# ukey = {'m':'Ntsr1Cre_2019_0007', 's':6, 'e':9,  'u': 7}
# ukey = {'m':'Ntsr1Cre_2019_0007', 's':3, 'e':7,  'u': 5}
ukey = {'m':'Ntsr1Cre_2019_0008', 's':3, 'e':7,  'u':14}

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# fig.savefig('foo3.pdf')#, format='pdf')

# %% [markdown]
# ## Plot model type performance overview

# %%
fig, axs = SplineLNP().plot_performance_overview(keys=None, pshf_config=False, eval_metric='r', 
                                                 colors=None, num_cols=2, verbose=True)
fig.savefig('model_performance_overview.pdf')

# %% [markdown]
# ## Plot model population filters

# %% [markdown]
# ### Opto filters

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper = -0.2
thresh_lower = -1.0
fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(thresh_upper=thresh_upper, 
                                                                     thresh_lower=thresh_lower, 
                                                                     keys=keys_crit,
                                                                     mi_kind='omi',
                                                                     zrange=[-.1, .1], 
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True)


fig.savefig('model_population_filters_opto.pdf')

# %% [markdown]
# ### Run filters

# %%
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

thresh_upper=1.0
thresh_lower=0.2

fig, axs = (SplineLNP() & keys_crit).plot_filter_split_by_modulation(thresh_upper=thresh_upper, 
                                                                     thresh_lower=thresh_lower, 
                                                                     keys=keys_crit,
                                                                     mi_kind='rmi',
                                                                     zrange=[-.1, .1], 
                                                                     fr_crit=0.1, 
                                                                     pshf_config=False,
                                                                     data_fs=60, 
                                                                     verbose=True)


fig.savefig('model_population_filters_run.pdf')

# %%
