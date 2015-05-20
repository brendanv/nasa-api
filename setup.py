import os
from setuptools import setup, find_packages

setup(
    name='nasa-api-wrapper',
    version="0.1.0",
    author="Brendan Viscomi",
    description="A convenient wrapper for NASA's APIs",
    url="https://github.com/brendanv/nasa-api",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    install_requires=['requests>=2.7.0', 'Pillow>=2.8.1'],
)
