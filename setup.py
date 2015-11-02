#!/usr/bin/env python
import setuptools

import coercion

setuptools.setup(
    name='coercion',
    version=coercion.__version__,
    description='Coercing data into a normalized form',
    long_description='\n'+open('README.rst').read(),
    url='https://github.com/dave-shawley/coercion',
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    py_modules=['coercion'],
    platforms='any',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'Topic :: Text Processing',
    ],
    zip_safe=True,
)
