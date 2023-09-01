from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sand',
    version='2023.8.1.1',
    long_description=long_description,
    packages=['sand', 'sand.config', 'sand.config.default', 'sand.plugin', 'sand.plugin.builtins', 'sand.server',
              'sand.helpers', 'sand.entities', 'sand.entities.resources'],
    url='https://github.com/FatConan/sand',
    license='MIT',
    author='Ian Usher',
    author_email='ian@headwillcollapse.net',
    description='Yet another static site generator',
    entry_points={
        'console_scripts': [
            'sand=sand:main',
        ],
    },
)
