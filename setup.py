from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yoctoEC2',
    version='0.2.0',
    description='A yocto EC2 Python project',
    long_description=long_description,
    url='https://github.com/ttruongatl/yocto-ec2-utils',
    author='Thanh Truong',
    author_email='thanh.truong@smisy.io',
    keywords='yoctoEC2 build tools development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    install_requires=[
        'Click~=7.0',
        'fabric~=2.4.0',
        'boto3~=1.9.188'
    ],
    tests_require=[
        'pytest',
    ],
    entry_points='''
        [console_scripts]
        yocto-ec2=yoctoEC2.scripts.command:cli
    ''',
    project_urls={
        'Bug Reports': 'https://github.com/ttruongatl/yocto-ec2-utils/issues',
        'Source': 'https://github.com/ttruongatl/yocto-ec2-utils/',
    },
)
