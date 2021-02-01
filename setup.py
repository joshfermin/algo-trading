from setuptools import setup, find_packages

setup(
    name='algo_trading',
    version='0.1',
    packages=find_packages(exclude=['examples']),
    url='https://github.com/joshfermin/algo-trading',
    license='MIT',
    author='Josh Fermin',
    author_email='joshfermin@gmail.com',
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
