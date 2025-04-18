from setuptools import setup, find_packages

setup(
    name='jobtracker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'InquirerPy'
    ],
    entry_points={
        'console_scripts': [
            'jobtracker=jobtracker.__main__:cli',
        ],
    },
)