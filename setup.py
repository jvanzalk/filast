from setuptools import setup

setup(
    name='filast',
    url='https://github.com/jvanzalk/filast',
    author='John van Zalk',
    author_email='johnvanzalk@gmail.com',
    packages=['filast'],
    # Dependencies
    install_requires=['pandas','fuzzywuzzy','python-Levenshtein'],
    version='0.1',
    license='MIT',
    description='A tool for determining email syntaxes and predicting emails'
    # Readme
    # long_description=open('README.txt').read(),
)
