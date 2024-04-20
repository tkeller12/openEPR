import setuptools
from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("pytxr/version.py", "r") as f:
    # Define __version__
    exec(f.read())

setup(
    name="pytxr",
    packages=setuptools.find_packages(),
    version=__version__,
    license="MIT",
    description="S-Band Transceiver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Timothy Keller",
#    url="",
#    download_url="",
#    project_urls={
#    },
    keywords=["S-Band", "Transceiver", "openEPR"],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

