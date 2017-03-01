from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Thyme',
    version='0.0.1',
    description='Development Utility/Convenience Tool',
    long_description=long_description,
    url='https://github.com/patallen/thyme',
    author='Patrick Allen',
    author_email='prallen90@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'thyme = thyme.cli:main',
        ],
    },
    install_requires=[
        'argparse==1.4.0',
        'arrow==0.10.0',
        'python-dateutil==2.6.0',
    ],
    extras_require={
        ':python_version=="3.2"': ['pytest<3'],
    },
    keywords='devtool productivity date timestamp uuid secret',
    packages=find_packages(exclude=['docs', 'tests', 'dist']),
)
