import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dynamic-xml',
    version='1.1',
    scripts=[
        'dynamicxml.py',
        'dynamicxmlparser.py',
        'dynamictreebuilder.py',
        'dynamicelement.py'
    ] ,
    author="Clay Brooks",
    author_email="clay_brooks@outlook.com",
    description="An etree utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claybrooks/dynamic-xml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
)