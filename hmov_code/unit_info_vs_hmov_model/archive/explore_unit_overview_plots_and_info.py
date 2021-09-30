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
# # Hmov units: Compare unit overview plot, unit info and Hmov RF models

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
import matplotlib.image as mpimg

from djd import hmov_models
from djd import hmov_unit
from l6s import l6s_utils # Layer 6 suppression code repo with utility functions for plotting unit overview

# This import does not seem to work - WHY? works for other DJD modules and functions - circular import?
# from djd.hmov_unit import get_tranges_hmov, _get_xptranges  

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Load model figure from Lisa

# %%
fig, ax = plt.subplots(figsize=[15,10], dpi=150)
image = mpimg.imread("glm_future_rfs.png")
ax.imshow(image)

# %%
# List of units example provided by Lisa that show 'future' RFs in the GLM
ukey1 = {'m': 'Ntsr1Cre_2020_0002', 's':3, 'u':4, 'e':1}
ukey2 = {'m': 'Ntsr1Cre_2020_0002', 's':3, 'u':15, 'e':1}
ukey3 = {'m': 'Ntsr1Cre_2020_0002', 's':3, 'u':16, 'e':1}
ukey4 = {'m': 'Ntsr1Cre_2020_0002', 's':3, 'u':18, 'e':1}
ukeys = [ukey1, ukey2, ukey3, ukey4,]

# %% [markdown]
# ## Plot GLM for example unit

# %%
glm_mean_test = np.round(np.mean(Glm.GlmEval().fetch('glm_r_test')), 3)
glm_std_test = np.round(np.std(Glm.GlmEval().fetch('glm_r_test')), 3)

# %%
glm_keys = (Glm * Glm.GlmEval() & ('glm_r_test > {:.3f}'.format(glm_mean_test+2*glm_std_test)) & {'m':'Ntsr1Cre_2019_0008'} ).fetch(dj.key)
print('Number of units that are better than mean correlation + 2 times std: ', len(glm_keys))
glm_keys

# %%
glm._plot_RF(glm_keys[0])

# %% [markdown]
# ## Plot SplineLNP for example units

# %%
paramset = 7
spl_mean_test = np.round(np.mean((SplineLNP.SplineLNPEval()&{'spl_paramset':paramset}).fetch('spl_r_test')), 3)
spl_std_test = np.round(np.std((SplineLNP.SplineLNPEval()&{'spl_paramset':paramset}).fetch('spl_r_test')), 3)

# %%
spl_keys = (SplineLNP * SplineLNP.SplineLNPEval() & {'spl_paramset':paramset} & ('spl_r_test > {:.3f}'.format(spl_mean_test+1.5*spl_std_test)) & {'m':'Ntsr1Cre_2019_0008'} ).fetch(dj.key)
print('Number of units that are better than mean correlation + 1.5 times std: ', len(spl_keys))

# %%
for key in spl_keys:
    glm._plot_RF(key)
    plt.show()

# %% [markdown]
# ## Show SplineLNP RF and plot_unit_overview() and show unit info

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}

# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20201214')

# Plot unit overview
axs = l6s_utils.plot_unit_overview(ukey, save=False, unit_info_df=unit_info_df)

# Plot SplineLNP RF
hmov_models._plot_RF(ukey, scale=True)

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21, 'spl_paramset': 8}

# Get unit info df
unit_info_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20201214')

# Plot unit overview
axs = l6s_utils.plot_unit_overview(ukey, save=False, unit_info_df=unit_info_df)

# Plot SplineLNP RF
hmov_models._plot_RF(ukey, scale=True)

# %%
axs

# %% [markdown]
# ## Test plot_opto_cond_psth()

# %%
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
nrows, ncols = 1, 1
axlength = 2.5
fig = plt.figure(figsize=[ncols*axlength, nrows*axlength],
                 constrained_layout=True, dpi=100)
gs = gridspec.GridSpec(figure=fig, ncols=ncols, nrows=nrows)  # width_ratios
ax_hmov = fig.add_subplot(gs[0,0])

ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}
hmovkey = ((Unit.Spikes() & ukey) * (Series.Experiment() & 'e_name LIKE "%hollymov%"')
            ).fetch(dj.key, as_dict=True)
(HmovUnit() & hmovkey).plot_opto_cond_psth(ax=ax_hmov, title=False, legend_frame=True, move_spines=5)

# %% [markdown]
# ## Test changes to hmov_unit.py functions:
# - plot_opto_cond_psth()
# - get_opto_cond_psth()
# - get_tranges_hmov()
# - get_xptranges()
# - _get_omi()

# %%
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8}
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u':15}

# %%
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25, 'spl_paramset': 8}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u':15}
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u':21}

hmovkey = ((Unit.Spikes() & ukey) * (Series.Experiment() & 'e_name LIKE "%hollymov%"')
            ).fetch(dj.key, as_dict=True)

# Call plot_opto_cond_psth() with stimcond='stim' is old default
(HmovUnit() & hmovkey).plot_opto_cond_psth(stimcond='stim')

# %%
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u':21}
xptranges_spont = hmov_unit._get_xptranges_spont(ukey)
xptranges_spont

# %%
print(xptranges_spont[0,0], xptranges_spont[0,1])

# %%
tranges_incl_spont = hmov_unit.get_tranges_hmov(ukey, stimcond='all')
tranges_incl_spont

# %%
tranges_incl_spont.shape

# %%
tranges_incl_spont[0:10,:]

# %%
from .util import ConvenienceTable, intersect_tranges, key2datafname, event_in_interval
tranges = tranges_incl_spont[intersect_tranges(xptranges_spont, tranges_incl_spont)]
tranges

# %%
tranges.shape

# %%
tranges2 = hmov_unit.get_tranges_hmov(ukey, stimcond='spont')
tranges2

# %%
tranges2.shape

# %%
(HmovUnit() & ukey).plot_opto_cond_psth(stimcond='spont')

# %%
