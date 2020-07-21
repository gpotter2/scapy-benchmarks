import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scapy-benchmarks",
    version="0.0.1",
    author="gpotter2",
    description="Continuous scapy benchmarks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpotter2/scapy-benchmarks",
    install_requires=[
        'matplotlib>3.1;python_version>"3"',
        'matplotlib<3.1;python_version<"2.7"',
        'argparse;python_version<"2.7"'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
)
