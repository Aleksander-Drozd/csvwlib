import pathlib
import setuptools


KEYWORDS = [
    "knowledge graph",
    "rdf",
    "controlled vocabulary",
    "csv",
    "tabular data",
    ]


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

    license="MIT",
    author="Aleksander Drozd",
    author_email="aleksander.drozd@outlook.com",

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

    keywords = ", ".join(KEYWORDS),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Indexing",
        ],
)
