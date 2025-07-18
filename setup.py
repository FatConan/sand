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
    packages=['sand', 'sand.builder', 'sand.config', 'sand.config.default', 'sand.plugin', 'sand.plugin.builtins', 'sand.server',
              'sand.helpers', 'sand.entities', 'sand.entities.resources'],
    url='https://github.com/FatConan/sand',
    license='MIT',
    author='Ian Usher',
    author_email='ian@headwillcollapse.net',
    description='Yet another static site generator',
    install_requires = [
        'Click>=8.2.0',
        'Jinja2>=3.1.6',
        'lesscpy>=0.15.1',
        'libsass>=0.23.0',
        'Markdown>=3.8',
        'MarkupSafe>=3.0.2',
        'pyhocon>=0.3.61',
        'urllib3>=2.4.0',
        'pathlib2>=2.3.7.post1',
        'rfeed>=1.1.1',
        'six>=1.17.0',
        'htmlmin2>=0.1.13'
    ],
    entry_points={
        'console_scripts': [
            'sand=sand:main',
        ],
    },
)
