from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aws-cli-utils',
    version='1.0.0',
    author="Albert Quiroga",
    author_email="albertquirogabertolin@gmail.com",
    description="CLI utilities to manage AWS resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertquiroga/aws-cli-utils",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'glue=glue.__main__:main',
            'ec2=ec2.__main__:main',
            'emr=emr.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Utilities"
    ],
    install_requires=['boto3', 'botocore'],
    python_requires='>=3.5'  # TODO check the minimum version
)
