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
# # Plot model example cells
# Code includes:
# - Fig 2 panel b-d: example model fits to (one panel per unit-model)
#
# Code excludes:
# - panel a: model diagram: this was generated in Adobe Illustrator
#
# The figure panels are manually stored in the GDrive paper fodler under 'Hmov_L6S_paper/fig_sources/' and then inserted via Adobe Illustrator into Hmov_L6S_paper/figs/fig_02.ai

# %% [markdown]
# ## TODO
# - could save example cells in one figure to reduce manual editing steps and just name it model_example_cells.pdf to reduce need to re-link new cell names
#   - wait for ok on general structure
#   - could do the same for model population filters

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
    'figure.dpi': 150,
    'figure.max_open_warning': 0,
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
# ## Plot model example units

# %% [markdown]
# ### Check for good candidates

# %% [markdown]
# #### Try out several model versions of same cell

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}  # ON RF, rest unclear
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23}#, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}#, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16}#, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}#, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF
# ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 6, 'e': 9, 'u': 8}#, 'spl_paramset': 103}  # ON RF, run U
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 9}#, 'spl_paramset': 103} # OFF RF, run U
# ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 6, 'e': 9, 'u': 11}#, 'spl_paramset': 103} # ON RF, run U, eye U
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 18}#, 'spl_paramset': 103} # ON RF, run in v U
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 48}#, 'spl_paramset': 100} # ON-OFF  RF, run  & eye unclear


# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP.Eval * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(as_dict=True))


# Sort models by r2
modkeys = modkeys.sort_values(by=['spl_r2_test'], ascending=False, ignore_index=True)
print(len(modkeys))

# Plot models
for i, row in modkeys.head(n=len(modkeys)).iterrows():
#     print(row)
    print(f"{i+1}/{len(modkeys)}")
    print(f'alpha: {row.spl_alpha}')
    print(f'lambda: {row.spl_lambda}')
    print(f'lr: {row.spl_lr}')
    print(f'sDF: {row.spl_spat_df}')
    print(f'tDF: {row.spl_temp_df}')
    print(f'opto_len: {row.spl_opto_len}')
    print(f'opto_df: {row.spl_opto_df}')    
    print(f'run_len: {row.spl_run_len}')
    print(f'run_df: {row.spl_run_df}')    
    print(f'eye_len: {row.spl_eye_len}')
    print(f'eye_df: {row.spl_eye_df}')    
    print(f'r_test: {row.spl_r_test}')
    key = row[['m','s','e','u','spl_paramset']].to_dict()
    fig, axs = plot_model(key, title=True)
    plt.show()

# %%
Mouse()

# %%
## Loop through all cells sorted by best model
# Get all keys with filter specifications
keys = pd.DataFrame((SplineLNP.Eval() * SplineLNPParams() 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True', 'spl_run_len': 40}
                     ).fetch(dj.key, 'spl_r2_test', as_dict=True))

# Get best model per unit
keys = get_best_model(keys, crit='spl_r2_test', key_only=False, format='df')

# Sort models by r2
keys = keys.sort_values(by=['spl_r2_test'], ascending=False, ignore_index=True)
print(len(keys))

# Plot models
for i, row in keys.head(n=len(keys)).iterrows():
    print(f"{i+1}/{len(keys)}")
    key = row[['m','s','e','u','spl_paramset']].to_dict()
    print(key)
    fig, axs = plot_model(key, title=True)
    plt.show()

# %%

# %%

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


# Lisa's suggestions
# ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 6, 'e': 9,  'u': 7}
# ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 3, 'e': 7,  'u': 5}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7,  'u': 14}
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7,  'u': 18}
ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 6, 'e': 9,  'u': 11}

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r2_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %% jupyter={"outputs_hidden": true}
for i, key in modkeys.iterrows():
#     print(key)
    key = key.to_dict()
    fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7,  'u': 18}


# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0007', 's': 6, 'e': 9,  'u': 11}


# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, title=True)#, gs=gs[0])

# %%
# Define unit key
ukey = {'m':'Ntsr1Cre_2019_0007', 's':6, 'e':9,  'u': 7}

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'True', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

fig, axs = plot_model(key, title=True)#, gs=gs[0])

# fig.savefig('foo3.pdf')#, format='pdf')

# %%
# Define unit ke
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
# ### Plot model example units

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10014}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10015}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10007}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10006}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10005}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10004}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10003}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10002}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10001}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 10000}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')
key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True', 'spl_run_len': 40}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

key

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_paramset': 103}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True, eval_kind='r')

# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_01.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True', 'spl_run_len': 40, 'spl_lambda': 2.5}
                       ).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)

fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
fname = os.path.join('.','figs', f"model_example_01.pdf")
print(f'Saving file to {fname}')
fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23}#, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}#, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16}#, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}#, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)
# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_02.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15}#, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16}#, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}#, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)
# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_02.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16}#, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}#, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)
fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
fname = os.path.join('.','figs', f"model_example_02.pdf")
print(f'Saving file to {fname}')
fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21}#, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)
fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
fname = os.path.join('.','figs', f"model_example_03.pdf")
print(f'Saving file to {fname}')
fig.savefig(fname)#, format='pdf')

# %%
# Define unit key
# Define example unit key
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig 1 unit
# ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 3, 'e': 7, 'u': 25}
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 23, 'spl_paramset': 723}  # *** ON RF, good run OFF and eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15, 'spl_paramset': 723}  # *** ON RF, opto NONE, run OFF, eye ON
# ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 3, 'e': 6, 'u': 16, 'spl_paramset': 707} # ** ON RF, run ON, eye ON
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 21, 'spl_paramset': 100}  # * OFF RF, opto OFF, run ON-OFF, eye OFF

# Restrict potential model keys for that unit
modkeys = pd.DataFrame((SplineLNP() * SplineLNPParams() & ukey 
                     & {'spl_pshf': 'False', 'spl_opto': 'True', 'spl_run': 'True', 'spl_eye': 'True'}).fetch(dj.key, as_dict=True))

# Pick best model amongst viable model keys
key = get_best_model(modkeys, crit='spl_r_test', key_only=True, format='dict')

# Plot model
fig, axs = plot_model(key, strf_tlims=[-200, 0], title=True)
# fname = os.path.join('.','figs', f"model_{ukey['m']}_s{ukey['s']}_e{ukey['e']}_u{ukey['u']}.pdf")
# fname = os.path.join('.','figs', f"model_example_02.pdf")
# print(f'Saving file to {fname}')
# fig.savefig(fname)#, format='pdf')

# %% [markdown]
# ### Plot STAs

# %%
ukey = {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19}  # Fig1 unit 1
(HmovUnit & ukey).plot_STA(smooth='spline16', plot_center=True, title=True)

# %%
ukey = {'m': 'Ntsr1Cre_2020_0002', 's': 6, 'e': 6, 'u': 15, 'spl_paramset': 723}  # Fig1 unit 2
(HmovUnit & ukey).plot_STA(smooth='spline16', plot_center=True, title=True)

# %%
