from setuptools import setup
import os
import martapy


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="martapy",
    version=martapy.__version__,
    author=martapy.__author__,
    author_email="git@edward.sh",
    description="Wrapper for MARTA realtime rail/bus APIs",
    long_description=read('README.rst'),
    keywords="MARTA API rail train Atlanta Georgia GA ATL itsmarta",
    url="https://github.com/arcward/fbparser",
    license="MIT",
    packages=['martapy'],
    install_requires=['requests'],
    include_package_data=True
)
