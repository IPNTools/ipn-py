import re
from os.path import join, dirname
from setuptools import setup, find_packages

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'ipn-py', '__init__.py')) as v_file:
    package_version = re. \
        compile(r".*__version__ = '(.*?)'", re.S). \
        match(v_file.read()). \
        group(1)

dependencies = [
    'requests',
    'pydantic',
    'web3',
    'base58',
    'tronpy',
]

setup(
    name="ipn-py",
    version=package_version,
    author="Daniil Shcherbakov",
    author_email="sherbakovdaniil6@gmail.com",
    description="IPN Python 3.9+ Library",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IPNTools/ipn-py',
    install_requires=dependencies,
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
