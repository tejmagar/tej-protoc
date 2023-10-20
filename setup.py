import setuptools
from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="tej-protoc",
    version="0.2.2",
    description="A TEJ Protocol implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/tejmagar/tej-protoc",
    package_dir={'tej_protoc': 'tej_protoc'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
