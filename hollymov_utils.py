import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
import sys
import datajoint as dj

sys.path.append('../../djd')

from djd import util
from djd import stimulus
from djd.event import Event
from djd.unit import Unit
from djd.stimulus import Stimulus


def get_xptranges_spont(key):
    """ Gives time ranges for the spontaneous activity that is recorded in response to the
    gray screen (60 s before and and after the movie is shown.

    Parameters
    ----------
    key : dict
        Unit key in the form {mouse ID, series, experiment, unit}
        E.g., {'m': 'Ntsr1Cre_2019_0003', 's': 4, 'e': 9}

    Returns
    -------
    xptranges : np.ndarray
        containing all time ranges (start and stop) of the spontOpto "stimulus"
    """
    expofname = util.key2datafname(key, filetype='.xml', force_exist=True)
    # read the xml file
    tree = etree.parse(expofname)
    root = tree.getroot()
    # get root slots, and passes elements. There's always only one of each of
    # these pluralized elements, but each can have multiple children:
    rootslots = root.find('Slots')
    rootpasses = root.find('Passes')
    # environment should also be available:
    environment = root.find('Environment')
    # find the stimulus SlotIDs:
    slotlabels = [slot.get('Label') for slot in rootslots.getchildren()]
    # search for 'stim' in all slot labels:
    spontslotis = ['spont' in sl.lower() for sl in slotlabels]
    spontslotis = np.where(spontslotis)[0]  # unpack tuple to get array
    spontslots = [rootslots[si] for si in spontslotis]
    stimslotIDs = [spontslot.get('ID') for spontslot in spontslots]  # leave as strings
    xptranges, _ = stimulus._get_expo_tranges_slotids(rootpasses, environment, stimslotIDs)
    return xptranges


def get_all_tranges(key):
    """Get time ranges of all seconds.
    For the hollymov stimulus, every second there is a 50/50 chance of optogenetic stimulation.
    Event.Times() only provides the time ranges of the seconds with opto stimulation. To
    plot neuron activity w.r.t. opto/no opto condition using unit.psth(), all time ranges
    are required: the time ranges of seconds with opto stimulation and without stimulation.

    Parameters
    ----------
    key : dict
        Unit key in the form {mouse ID, series, experiment, unit}
        E.g., {'m': 'Ntsr1Cre_2019_0003', 's': 4, 'e': 9}


    Returns
    -------
    tranges_all : np.ndarray
        Time ranges of all seconds during hmov presentation (not only the ones with opto
        stimulation) excluding spontaneous opto stimulation before and after the movie.

    """
    tranges, _, _ = (Unit().Spikes() & key).get_tranges()
    tranges_opto = (Event.Times() & key & {'ev_chan':'opto1'}).fetch1('ev_tranges')
    trange_last_stop = 0.0
    tranges_all_l = []
    for i, trange in enumerate(tranges_opto):
        trange_current_start = trange[0]
        diff_opto = trange_current_start - trange_last_stop
        # if there is opto stim in the next second
        if diff_opto <= 0.9:
            tranges_all_l.append(trange)
            trange_last_stop = trange[1]
        # if there is approx. 1 sec between opto stimulations
        elif (diff_opto > 0.9) & (diff_opto <= 1.0):
            tranges_all_l.append(np.array([trange_last_stop, trange_current_start]))
            tranges_all_l.append(trange)
            trange_last_stop = trange[1]
        # if there is one or more seconds without opto stimulation
        else:
            # if there is no opto stim in the next second
            # check the number of seconds before the next opto stim
            tranges_num = int(diff_opto)
            # get the total time lag between each new trange caused by a jitter
            stim_jitter = diff_opto - tranges_num
            # get the estimated time jitter for each new trange (should be ~0.002 s)
            stim_jitter_each = stim_jitter / (tranges_num + 1)
            # loop through number of elements needed to be inserted
            for trange_i in range(tranges_num):
                # create a new start and stop time w.o. opto that takes jitter into account
                trange_i_start = round(trange_last_stop + stim_jitter_each, 4)
                trange_i_stop = trange_i_start + 1
                tranges_all_l.append(np.array([trange_i_start, trange_i_stop]))
                trange_last_stop = trange_i_stop
                # update new last trange stop
            tranges_all_l.append(trange)
            trange_last_stop = trange[1]
    tranges_all = np.vstack(tranges_all_l)
    # only include tranges during movie presentation
    tranges_all_hmov = np.squeeze(tranges_all[
        np.where(np.logical_and(tranges_all[:,0] >= tranges[0][0], 
                                tranges_all[:,1] <= tranges[-1][1])), :])
    return tranges_all_hmov


def get_tranges_cond_swit(tranges_in):
    """Get those time ranges that mark a condition switch.
    Condition switch appears when in the previous second (the second prior to the time ranges), the opto condition was
    the opposite.
    E.g., input would be all opto time ranges that mark an opto stimulation (Event.Times()&key).fetch('ev_tranges')
    and output would be time ranges of only those seconds that have no opto stimulation in the second before.

        Parameters
        ----------
        tranges_in : np.ndarray
            Time ranges of seconds with optogenetic stimulation or no optogenetic stimulation.
            e.g., (Event.Times()&{'m':'Ntsr1Cre_2019_0003','s':4,'e':5,'u':14,'ev_chan':'opto1'}).fetch('ev_tranges')

        Returns
        -------
        tranges_w_diff_cond_bef : np.ndarray
            Time ranges of those seconds that have a different condition in the second before.
    """
    tranges_flatten = tranges_in.flatten()
    # difference between all tracked event times (also off times)
    tranges_diff_all = np.diff(tranges_flatten)
    # delete every second element because that is the stimulation length of 1 s
    tranges_diff = np.delete(tranges_diff_all, np.arange(0, tranges_diff_all.size, 2))
    # get the idx where a pause is happening
    idx_pause = np.where(tranges_diff > 0.9)
    # add the first element as ON time (would otherwise be ignored through diff()); add +1 to get the correct index
    idx_onset = np.insert((np.add(idx_pause, 1)), 0, 0)
    # get all real opto ON times with no opto stim in the second before
    onset_time_w_diff_cond_bef = tranges_in[idx_onset, 0]

    evtranges = np.empty((1, 2))
    # creating an event time ranges vector that has the true ON and OFF times
    for i in range(idx_onset.shape[0]):
        evon = onset_time_w_diff_cond_bef[i]
        evoff = onset_time_w_diff_cond_bef[i] + 1
        # append the new array with the selected element
        evtranges_i = np.column_stack((evon, evoff))
        evtranges = np.row_stack((evtranges, evtranges_i))
    # account for the empty entry
    tranges_w_diff_cond_bef = evtranges[1:, :]
    return tranges_w_diff_cond_bef


def get_tranges_cond_cont(tranges):
    """Get those time ranges where the condition is continued.
    E.g., input would be all opto time ranges that mark an opto stimulation (Event.Times()&key).fetch('ev_tranges')
    and output would be the time ranges of only those seconds that have also an opto stimulation in the second before.

        Parameters
        ----------
        tranges_in : np.ndarray
            Time ranges of seconds with optogenetic stimulation or no optogenetic stimulation.
            e.g., (Event.Times()&{'m':'Ntsr1Cre_2019_0003','s':4,'e':5,'u':14,'ev_chan':'opto1'}).fetch('ev_tranges')

        Returns
        -------
        tranges_w_same_cond_bef : np.ndarray
            Time ranges of those seconds that have the same condition in the second before.
    """
    tranges_flatten = tranges.flatten()
    # difference between all tracked event times (also off times)
    tranges_diff_all = np.diff(tranges_flatten)
    # delete every second element because that is the stimulation length of 1s
    tranges_diff = np.delete(tranges_diff_all, np.arange(0, tranges_diff_all.size, 2))
    # get the idx where a pause is happening
    idx_pause = np.where(tranges_diff < 0.1)
    # add +1 to get the correct index
    idx_onset = np.add(idx_pause, 1)
    # get all real opto ON times with no opto stim in the second before
    onset_time_w_same_cond_bef = tranges[idx_onset, 0]

    evtranges = np.empty((1, 2))
    # creating an event time ranges vector that has the true ON and OFF times
    for i in range(idx_onset.shape[0]):
        evon = onset_time_w_same_cond_bef[i]
        evoff = onset_time_w_same_cond_bef[i] + 1

        evtranges_i = np.column_stack((evon, evoff))
        evtranges = np.row_stack((evtranges, evtranges_i))
    tranges_w_same_cond_bef = evtranges[1:, :]
    return tranges_w_same_cond_bef


def psth_cond_trace(key, offsets=[-0.5, 0.5], figsize=None, title=True, ax=None):
    """Plot PSTH of the 4 conditions resulting of the hollymov stimulus with opto/no opto continuous condition as a
    baseline. The baseline of the continuous conditions is calculated as means of the spike firing rate.

        key : dict
            Contains at least 3 entries: 'm': mouse ID e.g. 'Ntsr1Cre_2019_0003', 's' series ID of the experiment,
            'e' experiment ID. Could also specify 'u' the unit ID. If the unit is not specify, all units are plotted.
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
    offset = [offsets[0], -(1 - offsets[1])]

    # get stimulus time ranges
    stim_tranges, _ = (Stimulus.Trial() & key).get_tranges()

    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    if evtimesopto.size == 0:
        print('No opto events populated in Event.Times() for unit '
              '{:s} s{:02d} e{:02d} u{:02d}.\n  Skip plotting.'.format(
                                            evkey['m'], evkey['s'], evkey['e'], evkey['u']))
    else:
        tranges_all = get_all_tranges(evkey)

        # get the opto, no opto mask
        _, _, opto = (Unit.Spikes() & key).get_tranges(tranges=tranges_all)
        no_opto = ~opto

        # get array with time ranges depending on conditon
        tranges_opto = tranges_all[opto]
        tranges_noopto = tranges_all[no_opto]

        # list with all conditions:
        # (1) opto on switch / suppression off switch
        # (2) opto on continuity / suppression continuously off
        # (3) opto off switch / suppression on switch
        # (4) no opto continuity / suppression continuously on
        tranges_conds = [get_tranges_cond_swit(tranges_opto),
                         get_tranges_cond_cont(tranges_opto),
                         get_tranges_cond_swit(tranges_noopto),
                         get_tranges_cond_cont(tranges_noopto),
                        ]
        labels = ['on-off', 'off-off', 'off-on','on-on']
        colors = ['tab:blue', 'tab:blue', 'k', 'k']
        lines = ['-', ':', '-', ':']
        widths = [1.5, 3, 1.5, 3]
        visible = [1.0, 0.2, 1.0, 0.2]

        # loop through conditions and get psths
        psths_cond = []
        midbins_cond = []
        for cond in range(len(tranges_conds)):
            # only tranges that are in stimulus time ranges
            tranges_cond = tranges_conds[cond]
            tranges_cond_stim = tranges_cond[util.intersect_tranges(stim_tranges, tranges_cond)]

            midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & key).get_psths(offsets=offset,
                                                                                       tranges=tranges_cond_stim)
            # list (len=num_cond) of dicts with key as uid
            psths_cond.append(psths)
            midbins_cond.append(midbins)

        # plotting
        # save initial ax input. This is important if several units are plotted in the loop
        # because ax will be overwritten
        ax_init = ax
        uids = sorted(psths_cond[0])
        keys = (Unit.Spikes() & key).fetch(dj.key)
        axes = []
        for uid, key in zip(uids, keys):
            assert uid == key['u']  # sanity check
            if ax_init is None:
                f, a = plt.subplots(figsize=figsize)  # make a new figure and axes
            else:
                a = ax
            for cond in range(len(tranges_conds)):
                a.plot(midbins_cond[cond], psths_cond[cond][uid], ls='-', marker='None', label=labels[cond], c=colors[cond],
                       lw=widths[cond], alpha=visible[cond], zorder=2)
            a.axvline(x=0, linestyle=':', c='grey', zorder=1)
            a.set_xlabel("Time (s)")
            a.set_ylabel("Firing rate (Hz)")
            a.legend(title=' L6 CT feedback', frameon=False, fontsize=13)

            titlestr = '%s s%02d e%02d u%02d PSTH' % (key['m'], int(key['s']), int(key['e']), uid)
            if title:
                a.set_title(titlestr)

            axes.append(a)

        return axes


def psth_cond_base(key, offsets=[-0.5, 0.5], figsize=None, title=True, ax=None):
    """Plot PSTH of the 4 conditions resulting of the hollymov stimulus with opto/no opto continuous condition as a
    baseline. The baseline of the continuous conditions is calculated as means of the spike firing rate.

        key : dict
            Contains at least 3 entries: 'm': mouse ID e.g. 'Ntsr1Cre_2019_0003', 's' series ID of the experiment,
            'e' experiment ID. Could also specify 'u' the unit ID. If the unit is not specify, all units are plotted.
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

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    tranges_all = get_all_tranges(evkey)

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
        get_tranges_cond_swit(tranges_opto),
        get_tranges_cond_swit(tranges_noopto),
    ]
    # list with continuous conditions:
    # (3) opto on continuity
    # (4) no opto continuity
    tranges_conts = [
        get_tranges_cond_cont(tranges_opto),
        get_tranges_cond_cont(tranges_noopto),
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
        midbins, psths, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offsets, tranges=tranges_swit_stim)
        # list (len=num_cond) of dicts with key as uid
        psths_swit.append(psths)

        # only tranges that are in stimulus time ranges
        tranges_cont = tranges_conts[cond]
        tranges_cont_stim = tranges_cont[util.intersect_tranges(stim_tranges, tranges_cont)]
        # get psths of continuous conditions
        _, psths_cont, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offsets, tranges=tranges_cont_stim)
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
            a.plot(midbins, psths_swit[cond][uid], ls='-', marker='None', label=labels_swit[cond], c=colors[cond],
                   zorder=2)
            a.axhline(y=np.mean(cond_cont_base[cond][int(key['u'])]), linestyle='--', c=colors[cond], label=labels_cont[cond],
                      zorder=1)
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
    """Plot bar graph of the 4 conditions resulting of the hollymov stimulus:   (1) opto on switch
                                                                                (2) opto on continuity
                                                                                (3) opto off switch
                                                                                (4) no opto continuity
    Each condition will be represented as a group of two individual bars, which will show the firing rate before and
    after a potential switch. The potential switch will not take place in condition 2 and 4 but a conditon switch will
    take place in conditon 1 and 3 (either from opto off to opto on or vice versa)

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

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    # evtimesopto = (Event.Times()&{'m': 'Ntsr1Cre_2019_0003', 's': '4', 'e': '9', 'u':'1','ev_chan':'opto1'}).fetch('ev_tranges')
    tranges_all = get_all_tranges(evkey)

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
    tranges_conds = [get_tranges_cond_swit(tranges_opto),
                     get_tranges_cond_cont(tranges_opto),
                     get_tranges_cond_swit(tranges_noopto),
                     get_tranges_cond_cont(tranges_noopto)]
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
