from setuptools import setup

setup(
    name='sand',
    version='2023.8.1.1',
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
