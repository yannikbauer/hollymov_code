from setuptools import setup, find_packages

setup(
    name = 'hmov_code',
    url = 'https://gitlab.lrz.de/blab/hollymov_code',
    description = ('Analysis code for hollywood movie experiments incl. dLGN recordings and '
                   'V1 L6 (primary visual cortex Layer 6) cortico-thalamic feedback direct '
                   'suppression (DFG grant "CRC1233 - Robust Vision", TP13).'),
    long_description = open('README.md').read(),
    author = 'Lisa Schmors @ Berens Lab, U Tuebingen; Yannik Bauer @ Busse Lab, LMU Munich',
    author_email='lisa.schmors@uni-tuebingen.de',
    version = '0.0.1',
    packages=find_packages(exclude=['tests*']),
    )
