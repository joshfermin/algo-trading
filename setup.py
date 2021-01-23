from setuptools import setup, find_packages

setup(
    name='bitcoin-price-prediction',
    version='0.1',
    packages=find_packages(exclude=['examples']),
    url='https://github.com/joshfermin/bitcoin-price-prediction',
    license='MIT',
    author='Josh Fermin',
    author_email='joshfermin@gmail.com',
    description='Bayesian regression for latent source model and Bitcoin',
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
