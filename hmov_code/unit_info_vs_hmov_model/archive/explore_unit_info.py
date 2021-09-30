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
# # Explore unit info: response criteria and unit types
# Explore what info we have, where and who we can get it and how we can add info we don't yet have

# %% [markdown]
# ## TODO

# %% [markdown]
# ## Setup

# %% [markdown]
# ### Start DJD
# Run main.py as interactive (-i) module (-m) and remotely (-r)\
# NOTE: any code inside the DJD-executing cell other than the executing line is not allowed

# %%
# %run -im djd.main

# %%
# Import standard libraries/modules
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import rcParams
import matplotlib.gridspec as gridspec
# %matplotlib inline

# Import custom modules
# NOTE: os.path.dirname(__file__) = '/Users/Yannik/code/djd/djd'
from djd import util, signal, plot # DJD modules
from .plot import plot_opto_titration

from l6s import l6s_utils

# %%
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## Explore SbC method

# %%
mkey = {'m': 'Ntsr1Cre_2019_0002'}
mskey = {'m': 'Ntsr1Cre_2019_0002', 's': 3}
msukey = {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 13}
mseukey = {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 13, 'e': 3}
mseukeys = [{'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 13, 'e': 3}, {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 14, 'e': 3},
            {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 13, 'e': 4}]

# %%
l6s_utils.get_all_unitexp_info()

# %%
mseu_df

# %%
df = l6s_utils.get_unitexp_snr(mseu_df)

# %%
foo = ((Condition.Zscores() & mseu_df[['m', 's', 'e', 'u']])
                            # & 'st8_type LIKE "none"')
                           # * (Series.Experiment() & 'e_name NOT LIKE "%OrientationContrFlashStim%"')
                           ).SbC(sbc_method='med_per_exp', z_crit=-1.96)

# %%
pd.DataFrame(foo)

# %%
foo2 = ((Condition.Zscores() & mseu_df[['m', 's', 'e', 'u']])
                            # & 'st8_type LIKE "none"')
                           # * (Series.Experiment() & 'e_name NOT LIKE "%OrientationContrFlashStim%"')
                           ).SbC(sbc_method='med_per_unit', z_crit=-1.96)

# %%
pd.DataFrame(foo2)

# %%
Condition.Zscores() & msukey

# %%
Series.Experiment() & {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'u': 13}

# %%
Condition() & key & {'e':3}

# %%
Condition.Rate() & key & {'e':3}

# %%
sponstimids = (Ivs & key & {'e':3}).fetch('ivs_sponstim_ids')[0]
sponstimids

# %%
pd.DataFrame((Ivs & key & {'e':3}))

# %%
Condition.Zscores() & key & {'e':3}

# %%
Stimulus.GratingCond() & key & {'e':3}

# %%
Stimulus.Trial() & key & {'e':3}

# %% [markdown]
# ## Explore SNR 
# check get_psth() and include splitbytrial kwarg option

# %%
mseu_df = l6s_utils.get_mseu_df()

# %%
l6s_utils.get_unitexp_snr(mseu_df)

# %%
Series.Experiment() & {'m': 'Ntsr1Cre_2019_0002', 's': 3}

# %%
Unit.Properties() & {'m': 'Ntsr1Cre_2019_0002', 's': 3}

# %%
ukey = {'m': 'Ntsr1Cre_2019_0002', 's': 3, 'e': 6, 'u': 14}

# %%
rasters, _, allstimis, opto, _ = (Unit.Spikes() & ukey).get_rasters(tranges=None, offsets=[0, 0], stimis=None, optosort=True)
raster_opto = np.array(rasters[ukey['u']][opto])
raster_ctrl = np.array(rasters[ukey['u']][~opto])

# %%
trange=[0,32]
srate=int(1/0.01)
binw=0.02
t = np.linspace(trange[0], trange[1], int(srate * trange[1]))  #  left bins edges
t_end = t + binw  #  right bin edges
bins = np.hstack((t[:, np.newaxis], t_end[:, np.newaxis]))
bins

# %%

# %%
# No split
# - gives one psth indexed for unit
# - stimis empty
# [(0, 32)]
# - tranges for all 60 trials split into on and off
midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & ukey).get_psths(
                                            offsets=[0, 0], stimis=None, splitbystimi=False, splitbyopto=True, splitbytrial=True,
                                            binw=0.02, tres=0.001, kernel='gauss', tranges=None)

# %%
psths

# %%
psths[13].shape

# %%
psths[14].shape

# %%
tranges.shape

# %%
tranges[0]

# %%
stimis

# %%
midbins

# %%
# Split by Stimi
# - gives 2 psths indexed for unit
# - stimis = [0,1] ~ WHY TWO STIMIS?
# - tranges for all 60 trials split into on and off
midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & ukey).get_psths(
                                            offsets=[0, 0], stimis=None, splitbystimi=True, splitbyopto=False, binw=0.02, tres=0.001, kernel='gauss', tranges=None)

# %%
psths

# %%
psths[13].shape

# %%
tranges.shape

# %%
stimis

# %%
# Split by Opto
# - gives 2 psths indexed for unit
# - stimis = [0,1]
# - tranges for all 60 trials split into on and off
midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & ukey).get_psths(
                                            offsets=[0, 0], stimis=None, splitbystimi=False, splitbyopto=True, binw=0.02, tres=0.001, kernel='gauss', tranges=None)

# %%
psths

# %%
psths[13].shape

# %%
psths[13][0].shape

# %%
len(rasters[13])

# %%
rasters[13][0].shape # ctrl

# %%
rasters[13][1].shape # opto

# %%
rasters[13][0][0].shape # num of spikes in ctrl trial 1

# %%
tranges.shape

# %%
# Split by Opto
# - gives 2 psths indexed for unit
# - stimis = [0,1]
# - tranges for all 60 trials split into on and off
midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & ukey).get_psths(
                                            offsets=[0, 0], stimis=None, splitbystimi=False, splitbyopto=True, splitbytrial=True, 
                                            binw=0.02, tres=0.001, kernel='gauss', tranges=None)

# %%
psths[13].shape

# %%

# %%

# %%

# %%

# %%
# Split by Stimi & Opto
# - gives 2 psths indexed for unit
# - stimis = [0,1]
# - tranges for all 60 trials split into on and off
midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & ukey).get_psths(
                                            offsets=[0, 0], stimis=None, splitbystimi=True, splitbyopto=True, binw=0.02, tres=0.001, kernel='gauss', tranges=None)

# %%
psths

# %%
psths[13].shape

# %%
len(rasters[13])

# %%
rasters[13][0].shape # ctrl

# %%
rasters[13][1].shape # opto

# %%
rasters[13][1][0].shape # num of spikes in opto trial 1

# %%
rasters[63][0][0].shape # num of spikes in ctrl trial 1

# %%
tranges.shape

# %%
stimis

# %% [markdown]
# ### get_rasters()

# %%
# Get rasters - no split
allrasters, tranges, allstimis, opto, _ = (Unit.Spikes() & key).get_rasters(tranges=None, offsets=[0, 0], stimis=None, optosort=False)

# %%
allrasters[6].shape

# %%
allrasters[6][0].shape

# %%
allrasters[6][1].shape

# %%
allstimis

# %%
opto

# %%
# Get rasters - split by opto
allrasters, tranges, allstimis, opto, _ = (Unit.Spikes() & key).get_rasters(tranges=None, offsets=[0, 0], stimis=None, optosort=True)

# %%
allrasters[6].shape

# %%
allrasters[6][0].shape

# %%
allrasters[6][1].shape

# %%
allstimis

# %%
opto

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# ## Check get_combined_unit_info()

# %%
mseu_df = l6s_utils.get_mseu_df()
mseu_df

# %%
foo = l6s_utils.get_unit_wave_type(mseu_df)
foo

# %%
mseu_df = l6s_utils.get_all_unitexp_info(save_df_name='default')
mseu_df

# %%
mseu_df = l6s_utils.get_all_unitexp_info(load_df_name='unit_info_20201104')
mseu_df

# %% [markdown]
# ## Check get_units() get_mseu_df() and get_basic_mseu_info()

# %%
mseu_df = l6s_utils.get_mseu_df()
mseu_df

# %%
mseu_df = l6s_utils.get_unitexp_fr(mseu_df)
mseu_df

# %%
mseu_df = l6s_utils.get_unitexp_burst_ratios(mseu_df)
mseu_df

# %%

# %% [markdown]
# ## Test get_unit_chirp_type()

# %%
mseu_df = l6s_utils.get_units(genotype=None)
mseu_df

# %%
mseu_df = l6s_utils.get_unitexp_chirp_type(mseu_df)

# %%
mseu_df

# %% [markdown]
# ## Check Ivs() & Tuning()

# %%
pd.DataFrame(((Ivs() & key) * Series.Experiment()).fetch())

# %%
pd.DataFrame(((Ivs.Stim() & key) * Series.Experiment()).fetch())

# %%
pd.DataFrame(((Ivs.Event() & key) * Series.Experiment()).fetch())

# %%
pd.DataFrame(((TuningInfo() & key) * Series.Experiment()).fetch())

# %%
pd.DataFrame(((Condition.Rate() & key) * Series.Experiment()).fetch())

# %%
Ivs()

# %%

Mouse() & key

# %% [markdown]
# ## Test get_units()

# %%
l6s_utils.get_units()

# %% [markdown]
# ## Get some test keys

# %%
## Get unit keys
# Get all Ntsr1-Cre with stGtACR2 opto experiments and target region LGN
mkeys = (Mouse() & ('m_strain LIKE "Ntsr1-Cre" AND m_dob > "2018-01-01" AND m_notes LIKE "%GtACR%"') \
         & (Series()))  # & 's_region LIKE "LGN"')) # can add AND m_genotype LIKE "+/-"

# Get series keys
skeys = (Series() & mkeys & Stimulus() & Unit()).fetch(dj.key) #& Tuning()# & ('st8_crit LIKE "none"')

# Get experiment keys
# ekeys = (Series().Experiment & 'e_name LIKE "%ori%"') & mkeys & Stimulus() & Unit()
# ekeys = (Series().Experiment & skeys)

# Get unit keys
# ukeys = (Unit().Spikes() & ekeys).fetch(dj.key)

# Put info into dataframe
ss = pd.DataFrame(skeys)
# us = pd.DataFrame(ukeys)

# print("n units =", len(us))

# %% [markdown]
# ## Explore DJD

# %%
Unit.Spikes() & e_keys

# %%

# %%
mkeys = Mouse() & m_str
mkeys

# %% jupyter={"outputs_hidden": true}
Mouse() & 'm_strain LIKE "Ntsr1-Cre"'

# %%

# %% jupyter={"outputs_hidden": true}
Series() & Mouse() & ('m_strain LIKE "Ntsr1-Cre" AND m_dob > "2018-01-01" AND m_notes LIKE "%GtACR%"') 

# %%

# %%

# %%

# %%

# %%
ss

# %%
VisDrive.Units() & skey

# %%
Condition.Zscores() & skey & {'u':7}

# %%
Condition() & skey & {'e':1, 'u':7}

# %%
Stimulus.GratingCond() & {'m': 'Ntsr1Cre_2020_0002', 's': 5, 'e':1}

# %%
(TuningInfo() & {'m': 'Ntsr1Cre_2020_0002', 's': 5, 'e':1}).fetch('ti_stim_map')

# %%
Stimulus.Trial() & skey & {'e':1}

# %%
Event.Condition() & skey & {'e':1}

# %%
(Condition.Rate() & 'st8_type LIKE "none"' & skey)
