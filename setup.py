import os
from setuptools import setup, find_packages

setup(
    name='nasa-api-wrapper',
    version="0.1.5",
    author="Brendan Viscomi",
    author_email="contact@brendanviscomi.com",
    description="A convenient wrapper for NASA's APIs",
    url="https://github.com/brendanv/nasa-api",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    packages=find_packages(),
    install_requires=['requests>=2.7.0', 'Pillow>=2.8.1'],
)
