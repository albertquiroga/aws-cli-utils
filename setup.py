from setuptools import setup

setup(
    name='bertolb-tools',
    version='0.0.1',
    packages=['crawl', 'myutils'],
    entry_points={
        'console_scripts': [
            'crawl=crawl.__main__:run'
        ]
    },
    install_requires=['boto3']
)