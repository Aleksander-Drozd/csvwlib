About
-----

``csvwlib`` is a python implementation of `W3C CSV on the Web recommendations <http://w3c.github.io/csvw/>`_.
It enables merging CSV file and associated metadata into JSON or RDF.

**This library is not compatible with Python2**

Installation
------------

::

	pip install csvwlib

Usage
-----

The library exposes one class - ``CSVWConverter`` which has methods ``to_json()`` and ``to_rdf()``
Both these methods have similar API. They receive 3+ parameters:

-  ``csv_url`` - URL of CSV file, default ``None``
-  ``metadata_url`` - the URL of metadata file, default ``None``
-  ``mode`` - conversion mode, default ``standard``, second possible value is ``minimal``

The are 3 ways of starting conversion process. 

-  pass only ``csv_url`` - corresponding metadata will be looked up based on ``csv_url`` as described in `Locating Metadata <https://www.w3.org/TR/2015/REC-tabular-data-model-20151217/#locating-metadata>`_
-  pass both ``csv_url`` and ``metadata_url`` - metadata by user will be used. If ``url`` field is set in metadata, the CSV file will be retrieved from that location which can cause, that passed ``csv_url`` will be ignored
-  pass only ``metadata_url`` - associated CSV files will be retrieved based on metadata ``url`` field  

You can also specify the conversion mode - `standard` or `minimal`, the default is `standard`.
From `documentation <https://www.w3.org/TR/2015/REC-csv2rdf-20151217/>`_

	**Standard** mode conversion frames the information gleaned from the cells of the tabular data with details of the rows, tables, and a group of tables within which that information is provided.
    
	**Minimal** mode conversion includes only the information gleaned from the cells of the tabular data.

After conversion to JSON, you receive a ``dict`` object, when converting to RDF it is more complex.
If you pass ``format`` parameter, graph will be serialized to this format and returned as string. 
From ``rdflib`` docs

    Format support can be extended with plugins, but 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig' and 'nquads' are built in.

If you don't specify the format, you will receive a ``rdflib.Graph`` object. 

Examples
--------
Example files can be found at http://w3c.github.io/csvw/tests/  

Common import for all examples:

.. code-block:: python

    from csvwlib import CSVWConverter

Start with csv

.. code-block:: python

    CSVWConverter.to_rdf('http://w3c.github.io/csvw/tests/test001.csv', format='ttl')

Minimal mode

.. code-block:: python

    CSVWConverter.to_rdf('http://w3c.github.io/csvw/tests/tree-ops.csv', mode='minimal', format='ttl')

Start with metadata

.. code-block:: python

    CSVWConverter.to_rdf(metadata_url='http://w3c.github.io/csvw/tests/test188-metadata.json', format='ttl')

Both CSV and metadata URL specified

.. code-block:: python

    CSVWConverter.to_rdf('http://w3c.github.io/csvw/tests/tree-ops.csv', 'http://w3c.github.io/csvw/tests/tree-ops.csv', format='ttl')

Start with metadata

.. code-block:: python

    CSVWConverter.to_json('http://w3c.github.io/csvw/tests/countries.json')

Start with csv

.. code-block:: python

    CSVWConverter.to_json('http://w3c.github.io/csvw/tests/test001.csv')
