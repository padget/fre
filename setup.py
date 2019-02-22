"""
Script d'installation de la librairie fre
"""

import setuptools

with open('README.md') as fh:
    long_description = fh.read()

    setuptools.setup(
        name='fre',
        version='0.0.1',
        author='Benjamin MATHIEU',
        author_email='padget.pro@gmail.com',
        description='Function Regular Expression',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/pypa/sampleproject',
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )
