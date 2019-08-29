from setuptools import setup

setup(
    name='bertolb-tools',
    version='0.0.1',
    packages=['crawl', 'bertolb_utils'],
    entry_points={
        'console_scripts': [
            'crawl=crawl.__init__:run'
        ]
    },
    install_requires=['boto3']
)
