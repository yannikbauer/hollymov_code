from setuptools import setup, find_packages

setup(
    name = 'hmov_code',
    url = 'https://gitlab.lrz.de/blab/hollymov_code',
    description = ('Additional tools for analysing the Hollywood movie experiments.'),
    long_description = open('README.md').read(),
    author = 'Lisa Schmors',
    author_email='lisa.schmors@uni-tuebingen.de',
    version = '0.0.0',
    packages=find_packages(exclude=['tests*']),
    )
