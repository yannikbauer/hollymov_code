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
# # Plot multiple response measures to hollymov stimulus
# Includes traces for average stimulus intensity, firing rate PSTH, pupil area, and locomotion.
#
# This is currently used as figure 1 panel f, where the multitraces output figure from this code is manually inserted into Hmov_L6S_paper/figs/fig_01.ai.

# %% [markdown]
# ## TODO
#  - think about folder structure: if file number becomes too large, split into /code, /data, /figures

# %% [markdown]
# ## Setup

# %%
run -im djd.main -- --dbname=dj_hmov --user=write

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

from djd.hmov_models import _get_data
from djd.hmov_unit import plot_multi_traces

# Automatically reload modules to get code changes without restarting kernel
# NOTE: Does not work for DJD table modules
# %load_ext autoreload
# %autoreload 2

# %%
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# Units that are opto sensitive and show FR transition w.r.t. locomotion onset (first choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}

# Units that are opto sensitive, show different FR in run sit (but no transition at onset) (second choice)
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 20}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 5, 'u': 22}

# %% [markdown]
# ## Showcase multi-traces function

# %%
# Plot multi traces - using HmovUnit() method: single test trace
(HmovUnit() & ukey).plot_multi_traces(train_idx=[2], test_idx=None, train_trange=None,
                                      linewidth=1, colors=None, alpha_train=1, alpha_test=0.25,
                                      spines=[], spine_pos=5, suptitle=False, plot_stim_rf=False, 
                                      title_detail=False, figsize=None, save=False, save_fmt='pdf');

# %%
# Plot multi traces - using HmovUnit() method: single test trace
(HmovUnit() & ukey).plot_multi_traces(train_idx=[6], test_idx=[1], train_trange=None,
                                      linewidth=1, colors=None, alpha_train=1, alpha_test=1,
                                      spines=[], spine_pos=5, suptitle=False, plot_stim_rf=False, 
                                      title_detail=False, figsize=None, save=False, save_fmt='pdf');

# %%
# Plot multi traces from hmov_unit.py: using multiple test traces
plot_multi_traces(ukey, train_idx=[6], test_idx=None, train_trange=None,
                  linewidth=1, colors=None, alpha_train=1, alpha_test=0.25,
                  spines=[], spine_pos=5, suptitle=False, plot_stim_rf=False, 
                  title_detail=True, figsize=None, save=False, save_fmt='pdf');

# %% [markdown]
# ## Plot multi-traces figure for Fig1

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
# Plot multi traces from hmov_unit.py: single test trace
plot_multi_traces(ukey, train_idx=[6], test_idx=[1], train_trange=None,
                  linewidth=0.5, colors=None, alpha_train=1, alpha_test=1,
                  spines=[], spine_pos=5, suptitle=False, plot_stim_rf=False, 
                  title_detail=True, figsize=(9.7, 4.8), save=True, save_fmt='pdf');

# %%
# Plot multi traces from hmov_unit.py: multiple test traces
plot_multi_traces(ukey, train_idx=[6], test_idx=None, train_trange=None,
                  linewidth=0.5, colors=None, alpha_train=1, alpha_test=0.25,
                  spines=[], spine_pos=5, suptitle=False, plot_stim_rf=False, 
                  title_detail=True, figsize=(9.7, 4.8), save=True, save_fmt='pdf');

# %%
