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
# # Plot opto condition raster + PSTH
#
# This is currently used as figure 1 panel g, where the output figure from this code is manually inserted into Hmov_L6S_paper/figs/fig_01.ai.

# %% [markdown]
# ## TODO

# %% [markdown]
# ## Setup

# %%
run -im djd.main -- --dbname=dj_hmov --user=write

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Automatically reload modules to get code changes without restarting kernel
# NOTE: Does not work for DJD table modules
# %load_ext autoreload
# %autoreload 2

# %%
# Define example unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}

# %% [markdown]
# ## Plot raster+PSTH for figure for Fig1

# %%
## Update plot parameters
# Option 1: Update general pars from modified matplotlibrc file
plt.rcParams.update(mpl.rc_params_from_file('../../matplotlibrc', fail_on_error=False, use_default_template=True))

# Option 2: Dynamically update general pars (use if not updating from modified matplotlibrc)
plt.rcParams.update({
#     'figure.dpi': 100,
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
#     'figure.dpi': 100,
    'figure.max_open_warning': 0, 
    'axes.labelsize': 7.0,
    'axes.titlesize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    })


# %%
# mpl.rcParams.keys()

# %% [markdown]
# TODO:
# - fix legend pos
# - fix canvas position: reposition rasters to psth rather than vv
# - rethink raster labelling: perhaps avoid side labels and just use one blue and one black raster
# - allow figure to save fig itself (only once the above points are addressed)

# %%
fig, axs = (HmovUnit() & ukey).plot_opto_cond_raster_psth(optocond=['off-on', 'on-off'], stimcond='stim',
                                                          offsets=[-0.5, -0.5], legend=False, legend_frame=False, 
                                                          linewidths=[1, 1, 1, 1], s=0.5, figsize=[3.5, 4.5], dpi=200);
axs[1].legend(ncol=2, frameon=False, loc='lower left', bbox_to_anchor=(1, 1))
# fig.constrained_layout()
plt.savefig('raster_psth.pdf')

# %%

# %%

# %%
fig, axs = (HmovUnit() & ukey).plot_opto_cond_raster_psth(optocond=['off-on', 'on-off'], stimcond='stim',
                                                          offsets=[-0.5, -0.5], legend=False, legend_frame=False, 
                                                          figsize=[3.5, 4.5], dpi=200);

# import pdb
# pdb.set_trace()
# dir(axs[1].get_legend())
# axs[1].get_legend().set_title('')  # access object attributes via dir(axs[2].get_legend())
# # axs[2].get_legend().get_texts()[0].set_text('control')
# # axs[2].get_legend().get_texts()[1].set_text('opto')
# axs[1].get_legend().set_bbox_to_anchor((1, 1.2))

# %%

# %% [markdown]
# ## Showcase plot_opto_cond_raster_psth() 

# %% jupyter={"outputs_hidden": true}
(HmovUnit() & ukey).plot_opto_cond_raster_psth(optocond=['off-on', 'on-off'], stimcond='stim',
                           offsets=[-0.5, -0.5], legend_frame=False, figsize=None, dpi=100);

# %%
