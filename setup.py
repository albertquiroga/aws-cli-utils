from setuptools import setup, find_packages

setup(
    name='bertolb-tools',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'crawl=glue.crawl.__main__:main',
            'ec2=ec2.connect.__main__:main',
            'devendpoint=glue.devendpoint.__main__:main',
            'emr=emr.connect.__main__:main'
        ]
    },
    install_requires=['boto3']
)
