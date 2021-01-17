# Copyright (c) 2012 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import os
import sys

from setuptools import setup


def get_static_files(path):
    return [os.path.join(dirpath.replace("luigi/", ""), ext)
            for (dirpath, dirnames, filenames) in os.walk(path)
            for ext in ["*.html", "*.js", "*.css", "*.png",
                        "*.eot", "*.svg", "*.ttf", "*.woff", "*.woff2"]]


luigi_package_data = sum(map(get_static_files, ["luigi/static", "luigi/templates"]), [])

readme_note = """\
.. note::

   For the latest source, discussion, etc, please visit the
   `GitHub repository <https://github.com/spotify/luigi>`_\n\n
"""


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


with open('README.rst') as fobj:
    long_description = readme_note + fobj.read()

# load meta package infos
meta = {}
with open("luigi/__meta__.py") as f:
    exec(f.read(), meta)

setup(
    name='luigi',
    version=meta['__version__'],
    description=meta['__doc__'],
    long_description=long_description,
    author=meta['__author__'],
    url=meta['__contact__'],
    license=meta['__license__'],
    packages=[
        'luigi',
        'luigi.configuration',
        'luigi.contrib',
        'luigi.contrib.hdfs',
        'luigi.tools'
    ],
    package_data={
        'luigi': luigi_package_data
    },
    entry_points={
        'console_scripts': [
            'luigi = luigi.cmdline:luigi_run',
            'luigid = luigi.cmdline:luigid',
            'luigi-grep = luigi.tools.luigi_grep:main',
            'luigi-deps = luigi.tools.deps:main',
            'luigi-deps-tree = luigi.tools.deps_tree:main'
        ]
    },
    install_requires=load_requirements('requirements/base.in'),
    extras_require=load_requirements('requirements/extra.in'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Monitoring',
    ],
)
