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
# # Test reduce_unitexp2unit_info()

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
df = l6s_utils.get_all_unitexp_info(load_df_name='unitexp_info_20210521')
df

# %%
msudf = l6s_utils.reduce_unitexp2unit_info(df, apply_crit=True, default_crit=True, 
                                           manual_crit={'all': {'s_region': 'LGN',
#                                                                'm_genotype': '+/-',
                                                               }})
msudf

# %%
msudf = l6s_utils.reduce_unitexp2unit_info(df, apply_crit=True, default_crit=True, 
                                           manual_crit={'all': {'s_region': 'LGN',
                                                               'm_genotype': '+/-'}})
msudf

# %%
msudf[msudf.s_region=='LGN']

# %%
msudf[msudf.m_genotype=='-/-']

# %% [markdown]
# ## Check validity of df vs msudf info

# %%
# df[(df.m=='Ntsr1Cre_2019_0002') & (df.s==3) & (df.e_name.str.contains('conTun'))][['m','s','u', 'e', 'e_name', 'sbc_zscore', 'sbc']]
df[(df.m=='Ntsr1Cre_2019_0008') & (df.s==3) & (df.u==25)][['m','s','u', 'e', 'e_name', 'm_genotype', 's_region', 
                                                           'chirp_type', 'osi_ctrl', 'osi_opto', 'dsi_ctrl', 'dsi_opto',
                                                           'sbc_zscore', 'sbc', 'tun_rsq_ctrl', 'wave_type']]

# %%
# df[(df.m=='Ntsr1Cre_2019_0002') & (df.s==3) & (df.e_name.str.contains('conTun'))][['m','s','u', 'e', 'e_name', 'sbc_zscore', 'sbc']]
msudf[(msudf.m=='Ntsr1Cre_2019_0002') & (msudf.s==3) & (msudf.u==13)][['m','s','u', 'm_genotype', 's_region', 
                                                           'chirp_type', 'osi_ctrl', 'osi_opto', 'dsi_ctrl', 'dsi_opto',
                                                           'sbc_zscore', 'sbc', 'wave_type']]

# %%
msudf[msudf.m_genotype=='-/-']

# %%
msudf[msudf.s_region=='V1']

# %%
# df[(df.m=='Ntsr1Cre_2019_0002') & (df.s==3) & (df.e_name.str.contains('conTun'))][['m','s','u', 'e', 'e_name', 'sbc_zscore', 'sbc']]
df[(df.m=='Ntsr1Cre_2019_0002') & (df.s==3) & (df.u==40)][['m','s','u', 'e', 'e_name', 'm_genotype', 's_region', 
                                                           'chirp_type', 'osi_ctrl', 'osi_opto', 'dsi_ctrl', 'dsi_opto',
                                                           'sbc_zscore', 'sbc', 'wave_type']]

# %%
msudf[np.isnan(msudf.osi_ctrl)]

# %%
msudf.osi_ctrl.values

# %%

# %%

# %% [markdown]
# ## Check validity of df vs DJD

# %%

# %%

# %%
df[df.e_name.str.contains('conTun_')][['m','s','u', 'e', 'sbc_zscore']]

# %%

# %%

# %%
df[df.e_name.str.contains('conTun_')].index.values

# %%
df[(df.m=='Ntsr1Cre_2019_0002') & (df.s==3) & (df.e_name.str.contains('conTun'))][['m','s','u', 'e', 'e_name', 'sbc_zscore', 'sbc']]

# %%
## Check SbC zscores - which to use?

# %%
# df = df[df['sbc_zscore'].notna()][['m','s','u','e_name','sbc_zscore']]
df = df[df['sbc_zscore'].notna()][['e_name','sbc_zscore']]

df

# %%
df.hist(by=df.e_name)
plt.tight_layout()

# %%
