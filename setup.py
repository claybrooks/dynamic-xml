import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dynamicxml',
    version='1.1',
    packages=['dynamicxml'],
    author="Clay Brooks",
    author_email="clay_brooks@outlook.com",
    description="An etree utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claybrooks/dynamic-xml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
)