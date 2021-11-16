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
# # Convenience notebook for dropping and repopulating database

# %% [markdown]
# ## Setup

# %% [markdown]
# ## Delete DB

# %%
run -im djd.main -- --dbname=dj_lisa --user=write

# %%
from djd.glms import plot_model

# %%

# %%

# %% jupyter={"outputs_hidden": true}
key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 20, 'spl_paramset': 601}
fig, ax = plot_model(key, title=True)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 20, 'spl_paramset': 602}
fig, ax = plot_model(key, title=True)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 20, 'spl_paramset': 603}
fig, ax = plot_model(key, title=True)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 20, 'spl_paramset': 604}
fig, ax = plot_model(key, title=True)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 20, 'spl_paramset': 605}
fig, ax = plot_model(key, title=True)

# %% jupyter={"outputs_hidden": true}
key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 9, 'u': 18, 'spl_paramset': 1, 'spl_stim': 'spnoise'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 9, 'u': 18, 'spl_paramset': 2, 'spl_stim': 'spnoise'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 9, 'u': 18, 'spl_paramset': 3, 'spl_stim': 'spnoise'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 9, 'u': 18, 'spl_paramset': 4, 'spl_stim': 'spnoise'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 9, 'u': 18, 'spl_paramset': 5, 'spl_stim': 'spnoise'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 18, 'spl_paramset': 601, 'spl_stim': 'hmov'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 18, 'spl_paramset': 602, 'spl_stim': 'hmov'}
fig, ax = plot_model(key)

key = {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'e': 10, 'u': 18, 'spl_paramset': 603, 'spl_stim': 'hmov'}
fig, ax = plot_model(key)

# %%

# %%
Mouse()

# %%
# HmovUnit().drop()

# %%
# Drop all tables - restart kernel and continue from next cell on 2nd run
# dropall()

# %% [markdown]
# ## Restart DB and set parameters to populate

# %%
run -im djd.main -- --dbname=dj_hmov --user=execute

# %%
Mouse()

# %% [markdown]
# ## Define paramsets

# %% [markdown]
# ### dj_hmov pars

# %%
# Define SplineLNPParams() parameter to populate

# spnoise: paramest given by Lisa
slnp_pars1 = {
    'spl_paramset': 1,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: testing
slnp_pars2 = {
    'spl_paramset': 2,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.0,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: testing
slnp_pars3 = {
    'spl_paramset': 3,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 16,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: testing
slnp_pars4 = {
    'spl_paramset': 4,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.025,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: testing 
slnp_pars5 = {
    'spl_paramset': 5,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.025,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: testing higher temp_df
slnp_pars6 = {
    'spl_paramset': 6,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: spnoise paramset 1 - now using new get_rf_area() results
slnp_pars7 = {
    'spl_paramset': 7,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# Best paramset from Lisa's recent sets without all extra filters
slnp_pars407 = {
    'spl_paramset': 407,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 6,
    'spl_temp_df': 7,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing spat_df w still low lr and high iterations
slnp_pars600 = {
    'spl_paramset': 600,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 10,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing spat_df=12 whigher lr and fewer iterations
slnp_pars601 = {
    'spl_paramset': 601,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 12,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing spat_df=16
slnp_pars602 = {
    'spl_paramset': 602,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 16,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing 12x12 df
slnp_pars603 = {
    'spl_paramset': 603,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.0,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 12,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing high spatial scaling 0.12
slnp_pars604 = {
    'spl_paramset': 604,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 12,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.12,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing high spat_df and high spatial scaling 0.12 paramset
slnp_pars605 = {
    'spl_paramset': 605,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 16,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.12,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing hmov paramset that matches spnoise paramset 1 ito stim resolution and splines per deg
slnp_pars606 = {
    'spl_paramset': 606,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 13,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0495,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing new get_rf_area() results against paramset 601 with same parameters
slnp_pars607 = {
    'spl_paramset': 607,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.2,
    'spl_max_iter': 1000,
    'spl_spat_df': 12,
    'spl_temp_df': 12,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.06,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing hmov paramset that matches spnoise paramset 1 ito stim resolution and splines per deg - now using new get_rf_area() results
slnp_pars608 = {
    'spl_paramset': 608,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 13,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0495,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# Testing high-res hmov paramset to compare w hmov paramset that matches spnoise paramset 1 ito stim resolution and splines per deg - checking RF new area
slnp_pars609 = {
    'spl_paramset': 609,
    'spl_stim': 'hmov',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 1.4,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 13,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 20,
    'spl_pshf_df': 10,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'False',
    'spl_nlag': 20,
    'spl_shift': 1,
    'spl_spat_scaling': 0.12,
    'spl_data_fs': 60.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'True',
}

# %% [markdown]
# ### dj_lisa pars

# %%
# Define SplineLNPParams() parameter to populate

# spnoise: paramest given by Lisa
slnp_pars1 = {
    'spl_paramset': 1,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: increasing regularization compared to 1
slnp_pars2 = {
    'spl_paramset': 2,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.1,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'True',
    'spl_pshf_len': 10,
    'spl_pshf_df': 8,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: like 1 without PSHF
slnp_pars3 = {
    'spl_paramset': 3,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.05,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'False',
    'spl_pshf_len': 0,
    'spl_pshf_df': 0,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# spnoise: like 2 (higher reg) without PSHF
slnp_pars4 = {
    'spl_paramset': 4,
    'spl_stim': 'spnoise',
    'spl_distr': 'softplus',
    'spl_alpha': 1.0,
    'spl_lambda': 0.1,
    'spl_lr': 0.1,
    'spl_max_iter': 1500,
    'spl_spat_df': 12,
    'spl_temp_df': 8,
    'spl_pshf': 'False',
    'spl_pshf_len': 0,
    'spl_pshf_df': 0,
    'spl_verb': 200,
    'spl_metric': 'corrcoef',
    'spl_norm_y': 'True',
    'spl_nlag': 10,
    'spl_shift': 1,
    'spl_spat_scaling': 0.0,
    'spl_data_fs': 50.0,
    'spl_opto': 'False',
    'spl_opto_len': 0,
    'spl_opto_df': 0,
    'spl_run': 'False',
    'spl_run_len': 0,
    'spl_run_df': 0,
    'spl_eye': 'False',
    'spl_eye_len': 0,
    'spl_eye_df': 0,
    'spl_eye_smooth': 'False',
}

# %% [markdown]
# ### Exponential non-lin test paramset

# %%
exp_par10000 = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par10000['spl_paramset'] = 10000
exp_par10000['spl_distr'] = 'exponential'
exp_par10000

# %%
exp_par10001 = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par10001['spl_paramset'] = 10001
exp_par10001['spl_distr'] = 'exponential'
exp_par10001['spl_lambda'] = 5.0
exp_par10001

# %%
exp_par10002 = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par10002['spl_paramset'] = 10002
exp_par10002['spl_distr'] = 'exponential'
exp_par10002['spl_spat_df'] = 8
exp_par10002['spl_temp_df'] = 5
exp_par10002['spl_opto_df'] = 5
exp_par10002['spl_run_df'] = 6
exp_par10002['spl_eye_df'] = 6
exp_par10002

# %%
exp_par10003 = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par10003['spl_paramset'] = 10003
exp_par10003['spl_distr'] = 'exponential'
exp_par10003['spl_lambda'] = 5.0
exp_par10003['spl_spat_df'] = 8
exp_par10003['spl_temp_df'] = 5
exp_par10003['spl_opto_df'] = 5
exp_par10003['spl_run_df'] = 6
exp_par10003['spl_eye_df'] = 6
exp_par10003

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10004,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 3000,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10005,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 4000,
    'spl_lr': 0.5,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10006,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 4000,
    'spl_lr': 0.4,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10007,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 6000,
    'spl_lr': 0.3,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10008,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 1000,
    'spl_lr': 0.35,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10009,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 1000,
    'spl_lr': 0.325,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10010,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 1000,
    'spl_lr': 0.3175,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10011,
    'spl_distr': 'exponential',
    'spl_lambda': 5.0,
    'spl_max_iter': 3000,
    'spl_lr': 0.325,
    'spl_spat_df': 8,
    'spl_temp_df': 5,
    'spl_opto_df': 5,
    'spl_run_df': 6,
    'spl_eye_df': 6
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10012,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 6000,
    'spl_lr': 0.3175,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10013,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 6000,
    'spl_lr': 0.3175,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10013,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 6000,
    'spl_lr': 0.3175,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10014,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 6000,
    'spl_lr': 0.2,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10015,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 1800,
    'spl_lr': 0.3,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
exp_par = (SplineLNPParams() & {'spl_paramset': 103}).fetch1()
exp_par.update({
    'spl_paramset': 10016,
    'spl_distr': 'exponential',
    'spl_lambda': 2.5,
    'spl_max_iter': 1800,
    'spl_lr': 0.3,
    'spl_spat_df': 13,
    'spl_temp_df': 11,
    'spl_opto_df': 11,
    'spl_run_df': 13,
    'spl_eye_df': 13
    })
exp_par

# %%
SplineLNPParams().populate(exp_par)

# %%
# (SplineLNPParams() & {'spl_paramset': 10013}).delete()

# %% [markdown]
# #### Populate exp nonlin test paramset

# %%
# Trying out Lisa's multiplication of predictors before nonlin
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10016}) # exp nonlin text paramset on Fig1 unit

# %%
# Trying out simple multiplication of predictors before nonlin
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10016}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10014}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10015}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10014}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10013}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10013}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10013}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10012}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10011}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10010}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10009}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10008}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10007}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10006}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10005}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10004}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10002}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10001}) # exp nonlin text paramset on Fig1 unit

# %%
SplineLNP().populate({'m': 'Ntsr1Cre_2019_0008', 's': 5, 'e': 8, 'u': 19, 'spl_paramset': 10000}) # exp nonlin text paramset on Fig1 unit

# %%
# (SplineLNPParams() & {'spl_paramset': 5}).delete()

# %%
SplineLNPParams()

# %%
(SplineLNP() & {'m': 'Ntsr1Cre_2019_0008', 's': 5, 'u': 48, 'e': 8})#.delete()

# %% jupyter={"outputs_hidden": true}
# SplineLNP().populate({'m': 'Ntsr1Cre_2020_0004', 's': 6, 'spl_paramset': 601, 'reserve_jobs': True}) # hmov
# SplineLNP().populate({'m': 'Ntsr1Cre_2020_0004', 's': 6, 'spl_paramset': 602, 'reserve_jobs': True}) # hmov
SplineLNP().populate({'m': 'Ntsr1Cre_2020_0004', 's': 6, 'spl_paramset': 603, 'reserve_jobs': True}) # hmov
# SplineLNP().populate({'m': 'Ntsr1Cre_2020_0004', 's': 6, 'spl_paramset': 604})#, 'reserve_jobs': True}) # hmov

# %%
SplineLNP() & {'m': 'Ntsr1Cre_2020_0004', 's': 6, 'spl_paramset': 601}

# %%
# Define GlmParams() pars to populate
glm_pars = {
 'glm_paramset': 1,
 'glm_distr': 'softplus',
 'glm_alpha': 1.0,
 'glm_lambda': 0.00015,
 'glm_solver': 'batch-gradient',
 'glm_lr': 0.7,
 'glm_max_iter': 1000,
 'glm_tol': 1e-06,
 'glm_seed': 0,
 'glm_norm_y': 'True',
 'glm_nlag': 8,
 'glm_shift': 1,
 'glm_spat_scaling': 0.06}

# %%
GlmParams().populate(glm_pars)

# %%
GlmParams()

# %% [markdown]
# ## Repopulate DB w build()

# %%
Unit.Spikes() & {'m':'Ntsr1Cre_2020_0001', 's':2, 'e':7}

# %%
HmovUnit() & {'m':'Ntsr1Cre_2020_0001', 's':2, 'e':7, 'u':19}

# %%
SplineLNP.populate({'m':'Ntsr1Cre_2020_0001', 's':2, 'e':7, 'u':58})

# %%
# Define mice to populate
mouse_ids = [
    {'m': 'Ntsr1Cre_2019_0002'},
    {'m': 'Ntsr1Cre_2019_0003'},
    {'m': 'Ntsr1Cre_2019_0007'},
    {'m': 'Ntsr1Cre_2019_0008'},
    {'m': 'Ntsr1Cre_2020_0001'},
    {'m': 'Ntsr1Cre_2020_0002'},
    {'m': 'Ntsr1Cre_2020_0003'},
    {'m': 'Ntsr1Cre_2020_0004'}
    ]

# %%
# Define sparse noise msekeys
msekeys = (Series.Experiment() & {'e_name': 'AsparseNoise5_60deg'}).fetch(dj.key)
msekeys

# %% jupyter={"outputs_hidden": true}
Series.Experiment()

# %%
# Define sparse noise msekeys
msekeys = (Series.Experiment() & 'e_name LIKE "%hollymov%"').fetch(dj.key)
msekeys

# %%
HmovUnit.populate({'m': 'Ntsr1Cre_2020_0002'})

# %%
# Build mice and report duration
from datetime import datetime
start_time = datetime.now()
print(f'Start date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}\n')
    
build_dict = build(keys=[{'m':'Ntsr1Cre_2020_0001', 's':2, 'e':11}], mantables=BASICMANTABLES+HMOV_MANTABLES, autotables=BASICAUTOTABLES+HMOV_AUTOTABLES)

print(f'\nStop date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
      f'\n-> Duration: {datetime.now() - start_time}')

print('Error dict:\n', build_dict)

# %%
# Time code execution
from datetime import datetime
start_time = datetime.now()
print(f'Start date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}\n')
    
build_dict = build(keys=[{'m': 'Ntsr1Cre_2020_0004'}, {'m': 'Ntsr1Cre_2020_0003'}], mantables=BASICMANTABLES+HMOV_MANTABLES, autotables=BASICAUTOTABLES)#+HMOV_AUTOTABLES)

print(f'\nStop date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
      f'\n-> Duration: {datetime.now() - start_time}')

print(build_dict)

# %%

# %%
# Time code execution
from datetime import datetime
start_time = datetime.now()
print(f'Start date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}\n')
    
build_dict = build(keys=mouse_ids, mantables=BASICMANTABLES+HMOV_MANTABLES, autotables=BASICAUTOTABLES+HMOV_AUTOTABLES)

print(f'\nStop date and time: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
      f'\n-> Duration: {datetime.now() - start_time}')

print(build_dict)

# %%

# %% [markdown]
# ## Lisa's code for restricted paramest population

# %%
param_keys = (SplineLNPParams() & {'spl_stim':'hmov'} & {'spl_pshf':'False'}).fetch(dj.key)
keys_crit = HmovUnit().get_crit_set(fr_crit=0.1, opto=True, run=True, eye=True, excl_ctrl_m=True)

for param_key in param_keys:
    for ukey in keys_crit:
        pop_key = param_key.copy()
        pop_key['m'] = ukey['m']
        pop_key['s'] = ukey['s']
        pop_key['e'] = ukey['e']
        pop_key['u'] = ukey['u']

        SplineLNP().populate(pop_key, reserve_jobs=True) 

# %% [markdown]
# ## Check DB tables

# %%
run -im djd.main -- --dbname=dj_hmov --user=execute

# %%

# %%

# %%

# %%
Mouse()

# %%
HmovUnit()

# %%
SplineLNP()

# %%
SplineLNP.Eval()

# %%
Glm()

# %%
Glm.Eval()

# %%

# %% [markdown]
# ## MODELLING MEMORY USAGE ANALYSIS 
#
# BEFORE MODEL
# - SUMMARY: loading data ramps up mem usage for JNB from 800 MB (incl Python background vars) > 5.5 GB
#   - variable shapes and sizes in get_hmov_data()
#     - get_hmov_array() gets stimulus arrays:
#       - stimulus_train_exp_order: shape=(43200, 16, 25); 138 MB (float64); 30 Hz
#       - stimulus_test: shape=(1200, 16, 25); 3.84 MB (float64); 30 Hz
#     - upsample_movie() and train-validation-test split doubles array sizes by upsampling from 30 Hz > 60 Hz, i.e. 2-fold :
#       - stimulus_train: (64800, 16, 25); 207.36 MB (float64); 60 Hz
#       - stimulus_validation: (21600, 16, 25); 69.12 MB (float64); 60 Hz
#       - stimulus_test_interp: (2400, 16, 25); 7.68 MB (float64); 60 Hz
#     - build_design_matrix() multiplies by nlag=20, i.e. 20-fold:
#       - X_train: (64800, 8000)=(nsamples, w x h x lag)=(64800,16 x 25 x 20); 4.15 GB (float64)
#       - X_validation: (21600, 8000); 1.38 GB (float64)
#       - X_test: (2400, 8000); 0.15 GB (float64)
#     - memory usage of data variables before model initialization
#                X_train:  3.9 GiB
#           X_validation:  1.3 GiB
#                 X_test: 146.5 MiB
#                   pars:  1.2 KiB
#              parentkey:  376.0 B
#                hm_info:  376.0 B
#              responses:  376.0 B
#        splinelnp_entry:  376.0 B
#        validation_dict:  248.0 B
#         y_test_repeats:  200.0 B
#                   dims:   96.0 B
#         TOTAL USAGE INCL PYTHON BACKGROUND VARS: ca. 800 MB + 5.5 GB = 6.3 GB
#
# DURING MODEL
# - model initialization:
#   - increases mem usage from 5.5 GB > 12 GB, growing to 14.5 GB
#   - duration: 3:40 min
# - model filter initialization
#   - no mem increase
#   - duration: < 1 s
# - model fitting 
#   - ramps up to 26 GB, with heavy use of swap memory: 5.6 GB -> thrashing (=rapid inefficient swapping between memory and storage)?
#     - at this peak of 26 GB, assuming data takes 5 GB, the model consumes 26 GB - 5 GB = 19 GB
#   - duration: 5 min
# - model prediction
#   - step reduces mem usage to 19 GB, then declining to 17 GB
#   - duration: 3 min
# => TOTAL PEAK MEM: ca. 25 GB (but depends heavily on model parameters, e.g. scaling=0.12 already crashes kernel)
# => TOTAL DURATION: ca. 12 min
#
# AFTER MODEL
# - at the end of the SplineLNP.make() function, mem usage is still 16 GB 
#   - calling calling gc.collect() at this point does not change this
# - interrupting kernel immediately frees memory
#
# FOLLOWING make() RUN
#   - at the beginning of the following run of SplineLNP.make(), mem usage is still 16 GB 
#     - to free up memory, calling gc.collect() at the start of SplineLNP.make() reduces memory from 16 GB > 6.5 GB
#       - so there seems to be a memory hangover of 6.6 GB - 800 MB = 5.2 GB (unclear if data or previous unclosed model)
#   - in the 2nd run of make(), after data loading, memory grows from 6.5 GB > 12 GB
#   - during model initialization, memory usage seems to be similar to the first run
#     - so the memory hangover seems to disappear at this point (presumably the previous model which was unclosed, gets overwritten)
#
# SUGGESTIONS FOR FREEING UP MEM SPACE
#   - we should try to reduce data type encoding to reduce the memory pressure
#     - uint8 instead of float64 can reduce memory by 8x
#       - but uint8 would not allow normalized values in range [0,1] > might need to resort to float32 or float16 
#        - Encoding of 8-bit unsigned integers (0-255) as float16 should be fine, given that we can reconvert them into uint8 without loss of precision:
#          - (np.linspace(0,1,255).astype(np.float16) * 255).astype(np.uint8) = np.array([0,1,2,3....255])
#   - check any memory reduction techniques on the SplineLNPBehaviour package side

# %%
