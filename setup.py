from setuptools import setup, find_packages

setup(
    name='jobtracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'rich',
        'InquirerPy',
    ],
    entry_points={
        'console_scripts': [
            'jobtracker = jobtracker.__main__:cli',
        ],
    },
)