# L6S/unit_crit_and_type_info

Code for extracting unit visual responsiveness criteria and unit type information.
The information is extracted by a pipeline of functions and subfunctions, each of which extracts 
specific unit information given a dataframe of mseu keys, and returns the same dataframe with 
the added information.

This code is not intended as a replacement of the ultimate goal to put this info into database
tables, but rather as a supplement to aid users in quickly seeing what unit info exists, where it 
can be found, and it can be obtained, without worrying about implementation details. The functions
below either fetch the info from existing table columns, or they call existing table methods, or 
existing functions in djd modules (such as util.py, signal.py stats.py), or they implement the 
method altogether new. The functions offer one modularized framework to get all unit info in one go,
by calling get_combined_unit_info(), or by calling just subfunctions for the unit info of interest.
All functions use the same framework of dataframes specified by mseu-keys
(mouse, series, expt. unit). The final dataframe is an interim supplement of a meta table in DJD
holding all this info.

This readme is intended for discussing code ideas and listing TODOS.

Code Structure:

*   general ideas
    *   check Martin's code natfeedback_code/calc.py and think about what to put into DJD
    *   (maybe check how Miro did it) 
    1.   put unit info functions into L6S\_utils if project-specific or djd.util if general
    2.   call functions from JNB/scripts in this subfolder unit\_crit_and_type_info
    3.   call those JNBs/scripts from main.py script or main.ipynb
        *   this one can toggle all the different analysis switches on or off depending on need
        *   it could later also call a script figx.py, which can sit alongside the other 
            non-consolidated analyses to allow both flexibility and simplicity
*   function pipeline
    *   get_combined_unit_info(): collects all unit information per experiment (criteria, types,
        states) and optionally applies selection criteria
        *   get_mseu_df(): gets consistent set of mseu keys (defaults or specified ones)
            *   get_units(): gets consistent set of units as msu keys (defaults or specified ones)
            *   get_basic_mseu_info(): Optionally adds basic mseu info (e.g. expt name)
        *   get_unit_crit(): collects various unit response quality criteria
            *   get_unit_tun_rsq(): gets unit tuning r-squared values 
            *   get_unit_zscores(): gets unit z-scores
            *   get_unit_fr(): gets unit firing rates
            *   get_unit_omi(): get unit opto modulation index
            *   get_unit_snr(): gets unit signal-to-noise ratios
            *   get_unit_trial_segment_corr(): gets unit trial segment correlation indices
            *   more ideas: 
        *   get_unit_type(): collects various unit typifications/classifications
            *   get_unit_osi_dsi(): gets unit orientation and direction selectivity indices
            *   get_unit_sbc(): gets unit suppressed-by-contrast index
            *   get_unit_chirp_type(): Gets unit type as ON-sust, OFF-sust, ON-OFF-trans 
                or mixed based on chirp stimulus response
            *   get_unit_wave_type: Gets unit type as inhib or excit based on wave shape
            *   more ideas:
                * RF position and area
                * unit position in shell/core
                * F1/F0-ratio
                * reliability (see Spacek2020)
                * sparseness (see Spacek2020)
        *   get_unit_state(): collects various unit state measures
            *   get_unit_burst_ratios(): gets unit burst ratios
    *   apply_unit_crit(): applies unit selection criteria
        *   set_unit_crit(): gets dictionary of selection criteria (defaults or specified ones)
        *   get_best_unit_duplicate_expt(): gets best of duplicate experiments for a unit
            

* coding tips   
    *   if you need to do some computations
        *   for simple row-wise computations, consider: **df.apply(λ function)**
        *   for more complex unit-wise computations, use: **for i,u, in df.groupby(\['m', 's', 'e', 'u'\]):**


QUESTIONS/DISCUSSION
*   allow all functions to either receive input as mseu df or list of mseu dicts?
*   allow all functions to **return** different output formats?
*   allow all functions to **save** different output formats depending on fname ending?
*   allow all functions inplace=True kwarg?
*   naming: criteria/indices/indicators/metrics/measures?
*   reorder functions according to pipeline?
*   should sbc() be a method of Condition.Zscores() or Unit.Spikes() (has mseu) or sth like Unit.Firing()?
*   Unit.Spikes() has method get_st8sort_new() to sort trials into sit vs run
    * what is the status?
*   Unit.Spikes() has method refine_units() to get visually responsive units
    * should we make a more general Unit.Firing() table that has mseu keys and offer multiple characterizations?
        * similar for Condition.Zscores() > Unit.Firing()?
*   should burst_ratio() be a method of FiringPattern(), and should FiringPattern() be a separate 
    table or be a part table of Unit, e.g. Unit.FiringPattern()?
*   VisDrive(): Should this be Unit.VisDrive()?

INFO


TODO:
- [ ]   consider renaming everything _unit_ > _unitexp_
- [ ]   make function that reduces mseu_df to msu_df
- [ ]   get_combined_unit_info()
    - [x]   get_mseu_df()
        - [x]   get_units()
        - [x]   get_basic_mseu_info()
    - [x]   get_unit_crit()
        - [x]   get_unit_tun_rsq() 
        - [x]   get_unit_zscores()
        - [x]   get_unit_fr()
            - [ ] integrate FRs mean and var for hollymov from HmovUnit()
        - [x]   get_unit_omi()
            - [ ] integrate OMIs for hollymov from HmovUnit()
        - [x]   get_unit_snr()
            - [ ] extend to other stimuli
        - [ ]   get_unit_trial_segment_corr()
    - [x]   get_unit_type()
        - [x]   get_unit_sbc()
            - [ ] check that SbC classification (True/False) is consistent across experiments and is
                consistent with Tuning().plot_overview(). If not, conTun should take precedence
            - [ ] ensure use fo mean method and correct z-threshold  
        - [x]   get_unit_osi_dsi()
            - [ ] adapt function to fetch scores from new SI() table
        - [x]   get_unit_chirp_type()
        - [x]   get_unit_wave_type()
        - [ ]   more ideas:
            - [ ]   RF position and area
            - [ ]   unit position in shell/core
            - [ ]   F1/F0-ratio
            - [ ]   reliability (see Spacek2020)
            - [ ]   sparseness (see Spacek2020)
    - [x]   get_unit_state(): collects various unit state measures
        - [x]   get_unit_burst_ratios()
            - [ ] implement opto titration
    - [ ]   apply_unit_crit()
        - [ ]   set_unit_crit()
        - [ ]   get_best_unit_duplicate_expt()
- [ ] unit info analyses
    - [ ] check unit_info data integrity
        - [ ] fix aspontaneous_opto parsing
        - [x] ensure FlashStim is excluded (e.g. from  SbC)
        - [ ] ...
    - [ ] check SbC RFs
        - do SbC cells have different RFs? Use Tuning().overiew() on mseu_df sorted by SbC-score,
          check RF and print SbC-score
- [x] implement plot_unit_overview()
    
