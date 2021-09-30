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
# # Test rmv_dupl_unitexps() on unit info df

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
ukey = {'m': 'Ntsr1Cre_2020_0001', 's':3}#, 'e_name': 'conTun12_opto'}
df = unit_info.loc[np.all(unit_info[list(ukey)] == pd.Series(ukey), axis=1)]
df = df[['m','s','e','u','e_name','tun_rsq_ctrl', 'tun_rsq_opto', 'OSI_ctrl', 'OSI_opto', 'sbc_zscore', 'OMI']]
df['tun_rsq_ctrl'].loc[1149] = np.nan # set to nan for testing
df['tun_rsq_ctrl'].loc[1263] = np.nan # set to nan for testing
print(len(df))
df

# %%
l6s_utils.rmv_dupl_unitexps(unit_info)

# %%
l6s_utils.rmv_dupl_unitexps(unit_info)

# %%
