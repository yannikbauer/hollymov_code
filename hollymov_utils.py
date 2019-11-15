import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
import sys
sys.path.append('../../djd')

import djd.util
import djd.stimulus
from djd.event import Event
from djd.unit import Unit


def get_xptranges_spont(key):
    """ Gives the Expo time ranges for the spontaneous activtiy that is tested in the hollymov experiment before and
    after the movies were shown ("spontOpto" stimulus = grey screen).

        Parameters
        ----------
        key : dict
            contains specifiction on mouse ID, series, experiment and unit
            E.g., {'m': 'Ntsr1Cre_2019_0003', 's': 4, 'e': 9}

        Returns
        -------
        a : np.ndarray
            containing all time ranges (start and stop) of the spontOpto "stimulus"
    """
    #expofname = util.key2datafname(key, filetype='.xml', force_exist=True)
    expofname = djd.util.key2datafname(key, filetype='.xml', force_exist=True)
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
    xptranges, _ = djd.stimulus._get_expo_tranges_slotids(rootpasses, environment, stimslotIDs)
    return xptranges


def get_all_tranges(tranges_opto):
    """Get time ranges of all seconds.
    For the hollymov stimulus, every second there is a 50/50 chance of optogenetic stimulation.
    Event.Times() only provides the time ranges of the seconds with opto stimulation. If you want to compare neuron
    activity w.r.t. opto/no opto condition in unit.psth() with customized time ranges, you need all time
    ranges (output of this function).

        Parameters
        ----------
        tranges_opto : np.ndarray
            Time ranges of seconds with optogenetic stimulation.
            e.g., (Event.Times()&{'m':'Ntsr1Cre_2019_0003','s':4,'e':5,'u':14,'ev_chan':'opto1'}).fetch('ev_tranges')

        Returns
        -------
        tranges_all : np.ndarray
            Time ranges of all seconds (not only the ones with opto stimulation).
    """
    # initialize the first tranges_opto
    tranges_opto = tranges_opto[0]
    # initialize the "all" tranges vector
    ## TODO: consider changing this into list which is converted back into np.array because this is faster
    tranges_all = tranges_opto[0, :]

    # loop through the events; as np.diff() is used, use length-1 otherwise index out of range
    for trange in range(1, tranges_opto.shape[0]):
        trange_current_start = tranges_opto[trange, 0]
        trange_last_stop = tranges_opto[trange - 1, 1]
        diff_opto = trange_current_start - trange_last_stop
        # check if there is opto stim in the next second
        if diff_opto < 1.0:
            trange_start = tranges_opto[trange, 0]
            trange_stop = tranges_opto[trange, 1]
            tranges_next = np.column_stack((trange_start, trange_stop))
            # append the array with opto event time ranges
            tranges_all = np.row_stack((tranges_all, tranges_next))
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
                # update new last trange stop
                trange_last_stop = trange_i_stop
                # add the times to tranges_all
                tranges_i_next = np.column_stack((trange_i_start, trange_i_stop))
                tranges_all = np.row_stack((tranges_all, tranges_i_next))
            # select the next following opto times
            trange_start = tranges_opto[trange, 0]
            trange_stop = tranges_opto[trange, 1]
            tranges_next = np.column_stack((trange_start, trange_stop))
            # append the array with the next opto event time tranges
            tranges_all = np.row_stack((tranges_all, tranges_next))
    return tranges_all


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


def get_tranges_cond_cont(trangesin):
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
    tranges_flatten = trangesin.flatten()
    # difference between all tracked event times (also off times)
    tranges_diff_all = np.diff(tranges_flatten)
    # delete every second element because that is the stimulation length of 1s
    tranges_diff = np.delete(tranges_diff_all, np.arange(0, tranges_diff_all.size, 2))
    # get the idx where a pause is happening
    idx_pause = np.where(tranges_diff < 0.1)
    # add +1 to get the correct index
    idx_onset = np.add(idx_pause, 1)
    # get all real opto ON times with no opto stim in the second before
    onset_time_w_same_cond_bef = trangesin[idx_onset, 0]

    evtranges = np.empty((1, 2))
    # creating an event time ranges vector that has the true ON and OFF times
    for i in range(idx_onset.shape[0]):
        evon = onset_time_w_same_cond_bef[i]
        evoff = onset_time_w_same_cond_bef[i] + 1

        evtranges_i = np.column_stack((evon, evoff))
        evtranges = np.row_stack((evtranges, evtranges_i))
    tranges_w_same_cond_bef = evtranges[1:, :]
    return tranges_w_same_cond_bef


def psth_cond_trace(m, s, e, u, offset):
    """Plot PSTH of the 4 conditions resulting of the hollymov stimulus with opto/no opto continuous condition as semi-
    transparent lines.

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
        offset: np.ndarray, optional
            Defines the time range of the PSTH w.r.t. the potential opto switch marking x=0.

        Returns
        -------
        a : plt.plot
            PSTH plot.
    """
    key = {'m': m, 's': str(s), 'e': str(e), 'u': str(u)}
    # get stimulus time ranges
    stim_tranges, _ = djd.stimulus.Stimulus.Trial.get_tranges(djd.stimulus.Stimulus.Trial() & key)

    uid = int(key['u'])
    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    tranges_all = get_all_tranges(evtimesopto)

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
    labels = ['opto switch on', 'opto continued', 'opto switch off', 'no opto']
    colors = ['tab:blue', 'tab:blue', 'k', 'k']
    lines = ['-', ':', '-', ':']
    widths = [1.5, 3, 1.5, 3]
    visible = [1.0, 0.2, 1.0, 0.2]

    # plotting
    f, a = plt.subplots()  # make a new figure and axes
    for cond in range(len(tranges_conds)):
        # only tranges that are in stimulus time ranges
        tranges_cond = tranges_conds[cond]
        tranges_cond_stim = tranges_cond[djd.util.intersect_tranges(stim_tranges, tranges_cond)]
        midbins, psths, rasters, tranges, stimis = (Unit.Spikes() & key).get_psths(offsets=offset,
                                                                                   trangesin=tranges_cond_stim)
        a.plot(midbins, psths[int(key['u'])], ls='-', marker='None', label=labels[cond], c=colors[cond],
               lw=widths[cond], alpha=visible[cond], zorder=2)

    a.axvline(x=0, linestyle=':', c='grey', zorder=1)
    a.set_xlabel("Time (s)")
    a.set_ylabel("Firing rate (Hz)")
    a.legend(title='stimi', frameon=False)
    titlestr = '%s s%02d e%02d u%02d PSTH' % (key['m'], int(key['s']), int(key['e']), uid)
    a.set_title(titlestr)
    f.tight_layout(pad=0.3)  # crop figure to contents


def psth_cond_base(m, s, e, u, offset):
    """Plot PSTH of the 4 conditions resulting of the hollymov stimulus with opto/no opto continuous condition as a
    baseline. The baseline of the continuous conditions is calculated as means of the spike firing rate.

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
        offset: np.ndarray, optional
            Defines the time range of the PSTH w.r.t. the potential opto switch marking x=0.
        eventfill: bool, optional, default=False
            If True time range of opto stimulation will be filled with transparent blue.

        Returns
        -------
        a : plt.plot
            PSTH plot.
     """
    key = {'m': m, 's': str(s), 'e': str(e), 'u': str(u)}
    # get stimulus time ranges
    stim_tranges, _ = (djd.stimulus.Stimulus.Trial() & key).get_tranges()

    uid = int(key['u'])
    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    # evtimesopto = (Event.Times()&{'m': 'Ntsr1Cre_2019_0003', 's': '4', 'e': '9', 'u':'1','ev_chan':'opto1'}).fetch('ev_tranges')
    tranges_all = get_all_tranges(evtimesopto)

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
    labels_swit = ['opto switch on', 'opto switch off']
    labels_cont = ['opto continued', 'no opto']
    colors = ['tab:blue', 'k']

    # plotting
    f, a = plt.subplots()  # make a new figure and axes
    for cond in range(2):
        # only tranges that are in stimulus time ranges
        tranges_swit = tranges_swits[cond]
        tranges_swit_stim = tranges_swit[djd.util.intersect_tranges(stim_tranges, tranges_swit)]
        # get psths of switch conditions
        midbins, psths_swit, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offset, trangesin=tranges_swit_stim)
        a.plot(midbins, psths_swit[int(key['u'])], ls='-', marker='None', label=labels_swit[cond], c=colors[cond],
               zorder=2)

        # only tranges that are in stimulus time ranges
        tranges_cont = tranges_conts[cond]
        tranges_cont_stim = tranges_cont[djd.util.intersect_tranges(stim_tranges, tranges_cont)]
        # get psths of continuous conditions
        _, psths_cont, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=offset, trangesin=tranges_cont_stim)
        a.axhline(y=np.mean(psths_cont[int(key['u'])]), linestyle='--', c=colors[cond], label=labels_cont[cond],
                  zorder=1)

    a.axvline(x=0, linestyle=':', c='grey', zorder=1)
    a.set_xlabel("Time (s)")
    a.set_ylabel("Firing rate (Hz)")
    a.legend(title='stimi', frameon=False)
    titlestr = '%s s%02d e%02d u%02d PSTH' % (key['m'], int(key['s']), int(key['e']), uid)
    a.set_title(titlestr)
    f.tight_layout(pad=0.3)  # crop figure to contents


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
    stim_tranges, _ = (djd.stimulus.Stimulus.Trial() & key).get_tranges()

    uid = int(key['u'])
    evkey = key
    evkey.update({'ev_chan': 'opto1'})

    # fetch the event times & get array with all time ranges
    evtimesopto = (Event.Times() & evkey).fetch('ev_tranges')
    # evtimesopto = (Event.Times()&{'m': 'Ntsr1Cre_2019_0003', 's': '4', 'e': '9', 'u':'1','ev_chan':'opto1'}).fetch('ev_tranges')
    tranges_all = get_all_tranges(evtimesopto)

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
        tranges_cond_stim = tranges_cond[djd.util.intersect_tranges(stim_tranges, tranges_cond)]
        _, psths, _, _, _ = (Unit.Spikes() & key).get_psths(offsets=[-1.0, 0.0], trangesin=tranges_cond_stim)
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
