from setuptools import find_packages, setup

setup(
    name='basicbreakevenanalysis',
    packages=find_packages("src"),
    package_dir={"": "src"},
    version='0.1.0',
    description='building the models and doing analysis involving data tables, goal seek and Monte-Carlo simulation',
    author='sandhyasuresh',
    license='MIT',
)
