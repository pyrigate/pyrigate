import os
from setuptools import setup, find_packages


def long_description():
    with open('README.md') as readme_file:
        return readme_file.read()


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


requirements = [
    'colorise',
    'docopt',
    'schedule',
    'schema'
]

setup(
    name='pyrigate',
    version=get_version(os.path.join('pyrigate', '__init__.py')),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms='All',
    description=('Single-plant automated and configurable watering system'),
    long_description=long_description(),
    python_requires='>=3.4',
    license='MIT',
    keywords='Raspberry pi, rpi, watering, automated',
    url='https://github.com/MisanthropicBit/pyrigate',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
        'console_scripts': [
            'pyrigate = pyrigate.main:main'
        ]
    }
)
