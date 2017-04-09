from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="martapy",
    version="1.0.0",
    author="Edward Wells",
    author_email="git@edward.sh",
    description="Python client library for the MARTA API",
    long_description=read('README.md'),
    keywords="MARTA API rail train Atlanta Georgia GA ATL itsmarta",
    url="https://github.com/arcward/fbparser",
    license="MIT",
    packages=['martapy'],
    install_requires=['requests']
)
