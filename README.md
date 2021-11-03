# hollymov_code

Analysis code for the paper on experiments involving recordings of in vivo extracellular dLGN activity, 
locomotion and pupil size during presentation of the Hollywood movie stimulus and optogenetic
suppression of primary visual cortex Layer 6 cortico-thalamic feedback (V1 L6 CT FB). 

Project carried out as Teilprojekt 13 (TP13) as part of DFG grant "CRC1233 - Robust Vision".

Maintainers: \
Lisa Schmors @ Berens Lab, U Tübingen \
Yannik Bauer @ Busse Lab, LMU Munich \
Ann Kotkat @ Busse Lab, LMU Munich

### Code structure
The package hmov_code contains the paper figure code in /hmov_code/, with subfolders for each 
figure which contain Jupyter notebooks to generate the individual figure panels. For the 
underlying analysis, as much code as possible lies in the Busse Lab repo 'djd', to keep the 
figure generation code clean.
Miscellaneous code is located in /notebooks/

### Cloning the hollymov_code repo to your code directory
```
cd <path_to_local_code_directory>
git clone git@gitlab.lrz.de/blab/hollymov_code.git
```

### Installing and updating the hmov_code package
The code package hmov_code can be installed system-wide using pip and then be imported (e.g. to 
jupyter notebooks) from any location via ``import hmov_code`` after the installation was successful.

Simply run the following code. Further code explanations below:
```
cd [PATH_TO]/hollymov_code
sudo pip install -e .  # alternative to `sudo python3 setup.py develop`
```

Code explanations:  
If you are not using your system installation of Python (e.g. if you are using conda), there is
no need for sudo.

You can directly use pip instead of running the setup.py file manually via `python3 setup.py develop`.
The ''-e'' flag stands for ''--editable'', which means that you can still edit the code of this
package (as opposed to other pip installable libraries that you do not contribute to). 
This is equivalent to the ''develop'' flag in `python3 setup.py develop`.

Alternatively to navigating into the hollymov_code directory, you can also go into the containing
directory and adapt the pip code line to `pip install -e djd`

To automatically upgrade all the packages required by hmov_code (as specified in the setup.py 
file), simply run the same code again.

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


### How the final figures are generated
This code only generates the individual figure panels, which are assembled into the paper figures
using Adobe Illustrator or Inkscape and are stored in the separate shared Google Drive folder
`hmov_L6S_paper`. This method avoids cumbersome multi-panel figure tetris code and is more 
flexible with respect to changes in figure layout. 

Figure numbers in the name are avoided as much as possible to flexibly adapt to changing figure
orders.

Panels are already pre-specified in the correct dimensions and are inserted to scale in Adobe
Illustrator via the `Place ...` command to easily update the panel in the figure when replacing
the panel file.
