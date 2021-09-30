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
# # Test apply_unit_crit() on unit info df

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

# %%
# Get unit info df
unit_info = l6s_utils.get_all_unitexp_info(load_df_name='unitexp_info_20210521')
unit_info

# %%
unit_info.columns

# %%
default_criteria = {
    'all': {'fr_mean_e': 0.5},  # Mean FR per experiment: Spacek2020 uses 0.01
    'oriTun': {'tun_rsq_ctrl': 0.25},  # Tuning curve fit r^2 for oriTun}
    # 'sbc_zscore': -1.96,
    # 'SNR_ctrl': 0.05,
    # 'trial_corr_qi_crit': 0.001,
    # ...
    }

default_criteria

# %%
crit = l6s_utils.set_unitexp_crit()
crit

# %%
df = l6s_utils.apply_unitexp_crit(unit_info)
df

# %%
