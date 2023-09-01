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
    install_requires = [
        'wheel',
        'Click>=7.1.2',
        'Jinja2>=2.11.3',
        'lesscpy>=0.15.1',
        'Markdown>=3.3.1',
        'MarkupSafe>=1.1.1',
        'pyhocon>=0.3.56',
        'urllib3>=1.26.5',
        'pathlib>=1.0.1',
        'rfeed>=1.1.1',
        'six>=1.15.0'
    ],
    entry_points={
        'console_scripts': [
            'sand=sand:main',
        ],
    },
)
