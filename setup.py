# -*- coding: utf-8 -*-
import os.path
import platform

from setuptools import setup, Extension

with open(os.path.join(os.path.dirname(__file__),
                       "elephant", "VERSION")) as version_file:
    version = version_file.read().strip()

with open("README.md") as f:
    long_description = f.read()
with open('requirements/requirements.txt') as fp:
    install_requires = fp.read().splitlines()
extras_require = {}
for extra in ['extras', 'docs', 'tests', 'tutorials', 'cuda', 'opencl']:
    with open('requirements/requirements-{0}.txt'.format(extra)) as fp:
        extras_require[extra] = fp.read()

if platform.system() == "Windows":
    fim_module = Extension(
        name='elephant.spade_src.fim',
        sources=['elephant/spade_src/src/fim.cpp'],
        include_dirs=['elephant/spade_src/include'],
        language='c++',
        libraries=[],
        extra_compile_args=[
            '-DMODULE_NAME=fim', '-DUSE_OPENMP', '-DWITH_SIG_TERM',
            '-Dfim_EXPORTS', '-fopenmp', '/std:c++17'])
elif platform.system() == "Darwin":
    fim_module = Extension(
        name='elephant.spade_src.fim',
        sources=['elephant/spade_src/src/fim.cpp'],
        include_dirs=['elephant/spade_src/include'],
        language='c++',
        libraries=['pthread', 'omp'],
        extra_compile_args=[
            '-DMODULE_NAME=fim', '-DUSE_OPENMP', '-DWITH_SIG_TERM',
            '-Dfim_EXPORTS', '-O3', '-pedantic', '-Wextra',
            '-Weffc++', '-Wunused-result', '-Werror', '-Werror=return-type',
            '-Xpreprocessor',
            '-fopenmp', '-std=gnu++17'])
elif platform.system() == "Linux":
    fim_module = Extension(
        name='elephant.spade_src.fim',
        sources=['elephant/spade_src/src/fim.cpp'],
        include_dirs=['elephant/spade_src/include'],
        language='c++',
        libraries=['pthread', 'gomp'],
        extra_compile_args=[
            '-DMODULE_NAME=fim', '-DUSE_OPENMP', '-DWITH_SIG_TERM',
            '-Dfim_EXPORTS', '-O3', '-pedantic', '-Wextra',
            '-Weffc++', '-Wunused-result', '-Werror',
            '-fopenmp', '-std=gnu++17'])

setup_kwargs = {
    "name": "elephant",
    "version": version,
    "packages": ['elephant', 'elephant.test'],
    "include_package_data": True,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "author": "Elephant authors and contributors",
    "author_email": "contact@python-elephant.org",
    "description": "Elephant is a package for analysis of electrophysiology data in Python",  # noqa
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "license": "BSD",
    "url": 'http://python-elephant.org',
    "project_urls": {
            "Bug Tracker": "https://github.com/NeuralEnsemble/elephant/issues",
            "Documentation": "https://elephant.readthedocs.io/en/latest/",
            "Source Code": "https://github.com/NeuralEnsemble/elephant",
        },
    "python_requires": ">=3.7",
    "classifiers": [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering']
}
# do not compile external modules on darwin
if platform.system() in ["Windows", "Linux"]:
    setup_kwargs["ext_modules"] = [fim_module]


setup(**setup_kwargs)
