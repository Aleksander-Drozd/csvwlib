import pathlib
import setuptools


setuptools.setup(
    name="csvwlib",
    version="0.3.2",

    description="Python implementation of CSV on the Web",
    long_description = pathlib.Path("README.md").read_text(),
    long_description_content_type = "text/markdown",

    url = "https://github.com/DerwenAI/csvwlib",
    project_urls = {
        "Bug Tracker": "https://github.com/DerwenAI/csvwlib/issues",
        "Source Code": "https://github.com/DerwenAI/csvwlib",
        },

    author="Derwen, Inc.",
    author_email="info@derwen.ai",
    license="MIT",

    python_requires=">=3.6",
    packages=[
        "csvwlib",
        "csvwlib.converter",
        "csvwlib.utils",
        "csvwlib.utils.rdf",
        "csvwlib.utils.url",
        "csvwlib.utils.json"
        ],
    install_requires=[
        "python-dateutil >= 2.6.1",
        "rdflib >= 4.2.2",
        "rdflib-jsonld >= 0.4.0",
        "requests >= 2.20.0",
        "uritemplate >= 3.0.0",
        "language-tags >= 0.4.3"
        ],
    zip_safe=False,
)

