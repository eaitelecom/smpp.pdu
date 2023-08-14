import os
from setuptools import setup, find_packages

with open("README.markdown", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="smpp.pdu",
    version="0.3",
    author="Roger Hoover",
    author_email="roger.hoover@gmail.com",
    description="Library for parsing Protocol Data Units (PDUs) in SMPP protocol",
    license="Apache License 2.0",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="smpp pdu",
    url="https://github.com/eaitelecom/smpp.pdu",
    include_package_data=True,
    package_data={"smpp.pdu": ["README.markdown"]},
    zip_safe=False,
    test_suite="smpp.pdu.tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Networking",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)