from setuptools import setup, find_packages

setup(
    name='bertolb-tools',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'glue=glue.__main__:main',
            'ec2=ec2.__main__:main',
            'emr=emr.__main__:main',
            'pscase=pscase.__main__:main'
        ]
    },
    install_requires=['boto3', 'pyperclip', 'botocore']
)
