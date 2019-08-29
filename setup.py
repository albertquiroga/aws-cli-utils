from setuptools import setup

setup(
    name='bertolb-tools',
    version='0.0.1',
    packages=['crawl', 'ec2', 'bertolb_utils'],
    entry_points={
        'console_scripts': [
            'crawl=crawl.__main__:main',
            'ec2=ec2.__main__:main'
        ]
    },
    install_requires=['boto3']
)
