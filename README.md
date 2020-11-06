# hollymov_code

Additional analysis code for Hollywood movie experiments on dLGN recordings. The experiments
have been recorded in the scope of V1 L6 (primary visual cortex Layer 6) cortico-thalamic 
feedback direct suppression experiments as part of DFG grant "CRC1233 - Robust Vision".

Maintainers: Lisa Schmors

### Code structure
The package hmov_code contains additional functions to analyze dLGN activity in the response to
the Hollywood movie stimulus and plotting functions. They mostly address the analysis of the optogenetic 
stimulations that are integrated into the djd database yet.

### Cloning the hollymov_code repo to your code directory
```
cd <path_to_local_code_directory>
git clone git@gitlab.lrz.de/blab/hollymov_code.git
```

### Installing the hmov_code package
The code package hmov_code can be installed system-wide using pip and then be imported (e.g. to 
jupyter notebooks) by ``import hmov_code`` after the installation was successful.
To install it using Python3:
```
cd hollymov_code
sudo python3 setup.py develop
```

### Usage of the hmov_code package
Functions can then be used by e.g.:
```
from hmov_code import hmov_utils

key = {'m': 'Ntsr1Cre_2019_0008', 's': 6, 'e': 6}
all_tranges = hmov_utils.get_all_tranges(key)
```
Be aware that you need to be connected to the database first.

Examples of the package usage can also be found in
``hollymov_code/notebooks/<latest_update>_test_hmov_utils.ipynb``