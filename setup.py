import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meteoalertapi",
    version="0.1.8",
    author="Rolf Berkenbosch",
    author_email="rolf@berkenbosch.nl",
    description="A small api to get alerting messages from extreme weather in Europe from https://www.meteoalarm.org.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rolfberkenbosch/meteoalert-api",
    install_requires=[
        'xmltodict',
        'requests',
    ],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
