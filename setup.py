"""pyrigate distribution script."""

from __future__ import with_statement

import os
import distutils.core


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


distutils.core.setup(
    name='pyrigate',
    version=get_version(os.path.join('pyrigate', '__init__.py')),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms='All',
    description=('Single-plant automated and configurable watering system'),
    license='MIT',
    keywords='Raspberry pi, watering, automated',
    url='https://github.com/MisanthropicBit/pyrigate',
    packages=['pyrigate', 'pyrigate.sensors'],
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
