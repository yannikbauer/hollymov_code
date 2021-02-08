#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions module for Hollywood movie experiment analysis code.
"""

__author__      = "Lisa Schmors" 
__created__     = "2020-11-06"

# Import standard libraries/modules
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
# Import DJD modules / tables
import datajoint as dj
from djd import hmov_unit
from djd import util
from djd import stimulus
from djd.event import Event
from djd.unit import Unit
from djd.stimulus import Stimulus


def main():
    """Print message to the user calling this as a script"""
    print("This .py file is only intended to be imported as a module providing functions, "
          "not to be executed as a standalone script.")


def psth_cond_base(key, offsets=[-0.5, 0.5], figsize=None, title=True, ax=None):
    """Plot PSTH of the 4 conditions resulting of the hollymov stimulus with opto/no opto
    continuous condition as baseline. The baseline of the continuous conditions is calculated
    as means of the spike firing rate.

    Parameters
    ----------
    key : dict
        Key of the form {'m': ..., 's': ..., 'e': ...}. Could also specify 'u' the unit ID.
        If the unit is not specify, all units are plotted.
    offsets: np.ndarray, optional
        Defines the time range of the PSTH w.r.t. the potential opto switch at time 0.
    figsize : int
         optionally define figure size
    title : bool
        set True to get title that specifies the mouse, series, experiment, and unit
    ax :
        initial input

    Returns
    -------
    axes : list of objects
        figure with one subplot per unit
     """
    # adjust offset wrt to get_psth()
    offsets = [offsets[0], -(1 - offsets[1])]

    # get stimulus time ranges
    stim_tranges, _ = (Stimulus.Trial() & key).get_tranges()

    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # get all time ranges
    tranges_all = hmov_unit.get_all_tranges(evkey)

    # get the opto, no opto mask
    _, _, opto = (Unit.Spikes() & key).get_tranges(tranges=tranges_all)
    no_opto = ~opto

    # get array with time ranges depending on conditon
    tranges_opto = tranges_all[opto]
    tranges_noopto = tranges_all[no_opto]

    # list with switch conditions:
    # (1) opto on switch
    # (2) opto off switch
    tranges_swits = [
        hmov_unit.get_tranges_cond_swit(tranges_opto),
        hmov_unit.get_tranges_cond_swit(tranges_noopto),
                    ]
    # list with continuous conditions:
    # (3) opto on continuity
    # (4) no opto continuity
    tranges_conts = [
        hmov_unit.get_tranges_cond_cont(tranges_opto),
        hmov_unit.get_tranges_cond_cont(tranges_noopto),
                    ]
    labels_swit = ['on-off', 'off-on']
    labels_cont = ['off-off', 'on-on']
    colors = ['tab:blue', 'k']

    # loop through conditions and get psths
    psths_swit = []
    cond_cont_base = []
    for cond in range(len(tranges_swits)):
        tranges_swit = tranges_swits[cond]
        tranges_swit_stim = tranges_swit[util.intersect_tranges(stim_tranges, tranges_swit)]
        # get psths of switch conditions
        midbins, psths, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offsets,
                                                                  tranges=tranges_swit_stim)
        # list (len=num_cond) of dicts with key as uid
        psths_swit.append(psths)

        # only tranges that are in stimulus time ranges
        tranges_cont = tranges_conts[cond]
        tranges_cont_stim = tranges_cont[util.intersect_tranges(stim_tranges, tranges_cont)]
        # get psths of continuous conditions
        _, psths_cont, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offsets,
                                                                 tranges=tranges_cont_stim)
        cond_cont_base.append(psths_cont)

    # plotting
    # save initial ax input. This is important if several units are plotted in the loop
    # because ax will be overwritten
    ax_init = ax
    uids = sorted(psths_swit[0])
    keys = (Unit.Spikes() & key).fetch(dj.key)
    axes = []
    for uid, key in zip(uids, keys):
        assert uid == key['u']  # sanity check
        if ax_init is None:
            f, a = plt.subplots(figsize=figsize)  # make a new figure and axes
        else:
            a = ax
        for cond in range(len(tranges_swits)):
            a.plot(midbins,
                   psths_swit[cond][uid],
                   ls='-',
                   marker='None',
                   label=labels_swit[cond],
                   c=colors[cond],
                   zorder=2)
            a.axhline(y=np.mean(cond_cont_base[cond][int(key['u'])]),
                      linestyle='--', c=colors[cond], label=labels_cont[cond], zorder=1)
        a.axvline(x=0, linestyle=':', c='grey', zorder=1)
        a.set_xlabel("Time (s)")
        a.set_ylabel("Firing rate (Hz)")
        a.legend(title=' L6 CT feedback', frameon=False)

        titlestr = '%s s%02d e%02d u%02d PSTH' % (key['m'], int(key['s']), int(key['e']), uid)
        if title:
            a.set_title(titlestr)

        axes.append(a)

    return axes


def bar_cond(m, s, e, u):
    """Plot bar graph of the 4 conditions resulting of the hollymov stimulus:
        (1) opto on switch
        (2) opto on continuity
        (3) opto off switch
        (4) no opto continuity
    Each condition will be represented as a group of two individual bars, which will show the
    firing rate before and after a potential switch. The potential switch will not take place
    in condition 2 and 4 but a conditon switch will take place in conditon 1 and 3 (either from
    opto off to opto on or vice versa)

    Parameters
    ----------
    m : str
        mouse ID, e.g., 'Ntsr1Cre_2019_0003'
    s: int
        series ID of the experiment
    e: int
        experiment ID
    u: int
        unit ID

    Returns
    -------
    a : plt.bar
        bar plot of the firing rate depending on the opto condition.
     """
    key = {'m': m, 's': str(s), 'e': str(e), 'u': str(u)}
    # get stimulus time ranges
    stim_tranges, _ = (Stimulus.Trial() & key).get_tranges()

    uid = int(key['u'])
    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # get all time ranges
    tranges_all = hmov_unit.get_all_tranges(evkey)

    # get the opto, no opto mask
    _, _, opto = (Unit.Spikes() & key).get_tranges(tranges=tranges_all)
    no_opto = ~opto

    # get array with time ranges depending on conditon
    tranges_opto = tranges_all[opto]
    tranges_noopto = tranges_all[no_opto]

    # list with all conditions:
    # (1) opto on switch
    # (2) opto on continuity
    # (3) opto off switch
    # (4) no opto continuity
    tranges_conds = [hmov_unit.get_tranges_cond_swit(tranges_opto),
                     hmov_unit.get_tranges_cond_cont(tranges_opto),
                     hmov_unit.get_tranges_cond_swit(tranges_noopto),
                     hmov_unit.get_tranges_cond_cont(tranges_noopto)]
    fr_prior = []
    fr_after = []
    std_prior = []
    std_after = []

    for cond in range(len(tranges_conds)):
        # only tranges that are in stimulus time ranges
        tranges_cond = tranges_conds[cond]
        tranges_cond_stim = tranges_cond[util.intersect_tranges(stim_tranges, tranges_cond)]
        _, psths, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=[-1.0, 0.0], tranges=tranges_cond_stim)
        fr_split = np.array_split(psths[int(key['u'])], 2)
        fr_prior.append(np.mean(fr_split[0]))
        std_prior.append(np.std(fr_split[0]))
        fr_after.append(np.mean(fr_split[1]))
        std_after.append(np.std(fr_split[1]))

    # plotting
    labels = ['opto switch on', 'opto continued', 'opto switch off', 'no opto']
    c_prior = ['grey', 'tab:blue', 'tab:blue', 'grey']
    c_after = ['tab:blue', 'tab:blue', 'grey', 'grey']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    f, a = plt.subplots()  # make a new figure and axes

    a.bar(x - width / 2, fr_prior, width, yerr=std_prior, label='prior', color=c_prior)
    a.bar(x + width / 2, fr_after, width, yerr=std_after, label='after', color=c_after)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    a.set_ylabel("Firing rate (Hz)")
    a.set_xticks(x)
    a.set_xticklabels(labels)
    l = a.legend(('no opto', 'opto'), frameon=True, loc='lower right',
                 ncol=2, fancybox=True)
    titlestr = '%s s%02d e%02d u%02d' % (key['m'], int(key['s']), int(key['e']), uid)
    a.set_title(titlestr)
    
def insert_year(mouse):
    """
    Insert year into the iTracking movie file name if missing.
    You have to mount the filesystem first via SSHFS with `hux -r`.
    
    Parameters
    ----------
    mouse: str
        Mouse name (e.g. 'Ntsr1Cre_2020_0002')
    """
    dir_name = os.path.join('/mnt/hux/mudata/iTracking/', mouse)
    os.chdir(dir_name)
    mouse_info_split = mouse.split('_')
    for subdir, dirs, files in os.walk(dir_name):
        for file in files:
            file_info_split = file.split('_')
            if file_info_split[1] != mouse_info_split[1]:
                file_info_split.insert(1,mouse_info_split[1])
                filename_w_year = '_'.join(file_info_split)
                dir_new = os.path.join(subdir,filename_w_year)
                dir_old = os.path.join(subdir,file)
                os.rename(dir_old, dir_new)
                print('Renaming {:s} into {:s}'.format(dir_old, dir_new))
            else:
                pass
