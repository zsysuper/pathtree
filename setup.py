# -*- coding: utf-8 -*-
import codecs
import os
import re
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pathtree.husky',
    version=find_version('pathtree', '__init__.py'),
    description='pathtree implements a tree for fast path lookup.',
    long_description=read('README.rst'),
    packages=find_packages(),

    install_requires=[

    ],

    extras_require={

    },

    url='https://github.com/zsysuper/pathtree',
    author='husky',
    author_email='215941106@qq.com',
    keywords=['pathtree'],
    entry_points={
        'console_scripts': [
            'pathtree = pathtree.main:main',
        ],
    },

    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Distributed Computing',
    ],
)
