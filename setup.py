import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meteoalertapi",
    version="0.0.7",
    author="Rolf Berkenbosch",
    author_email="rolf@berkenbosch.nl",
    description="A small api to get alerting messages from extreme weather in Europe from https://www.meteoalarm.eu.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rolfberkenbosch/meteoalarm-api",
    install_requires=[
        'xmltodict',
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
