from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="annotizer",
    version=find_version('annotizer', '__init__.py'),
    description="This module allows multiple projects to share the __annotations__ dictionary.",
    long_description=long_description,
    url="https://github.com/oranguman/annotizer.git",
    author="Cem Karan",
    author_email="cfkaran2+annotizer@gmail.com",
    maintainer="Cem Karan",
    maintainer_email="cfkaran2+annotizer@gmail.com",
    license="PSF", # Need to set this

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Software Development'
    ],

    # What does your project relate to?
    keywords='__annotations__ decorator',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
)
