## About

`csvwlib` is a Python implementation of the W3C 
[CSV on the Web](http://w3c.github.io/csvw/) recommendations.

This enables converting tabular data, and optionally its associated
metadata, to a semantic graph in RDF or JSON-LD format.

Tabular data includes CSV files, TSV files, and upstream may be
coming from spreadsheets, RDBMS export, etc.

Requires Python 3.6 or later.


## Installation

```
pip install csvwlib
```


## Usage

The library exposes one class - `CSVWConverter` which has methods `to_json()` and `to_rdf()`

Both of these methods have similar API, and require 3+ parameters: 

  * `csv_url` - URL of a CSV file; default `None`
  * `metadata_url` - optional URL of a metadata file; default `None`
  * `mode` - conversion mode; default `standard`, or `minimal`

The are three ways of starting the conversion process:

  * pass only `csv_url` - corresponding metadata will be looked up based on `csv_url` as described in [Locating Metadata](https://www.w3.org/TR/2015/REC-tabular-data-model-20151217/#locating-metadata)

  * pass both `csv_url` and `metadata_url` - metadata by user will be used. If `url` field is set in metadata, the CSV file will be retrieved from that location which can cause, that passed `csv_url` will be ignored

  * pass only `metadata_url` - associated CSV files will be retrieved based on metadata `url` field  


You can also specify the conversion mode - `standard` or `minimal`, the default is `standard`.
From the [W3C documentation](https://www.w3.org/TR/2015/REC-csv2rdf-20151217/):

> **Standard** mode conversion frames the information gleaned from the cells of the tabular data with details of the rows, tables, and a group of tables within which that information is provided.  
> **Minimal** mode conversion includes only the information gleaned from the cells of the tabular data.

After conversion to JSON, you receive a `dict` object, when converting to RDF it is more complex.
If you pass `format` parameter, graph will be serialized to this format and returned as string. 
From the `rdflib` docs:

> Format support can be extended with plugins, but "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig" and "nquads" are built in.

If you don't specify the format, you will receive a `rdflib.Graph` object. 


## Examples

Example data+metadata files can be found at 
<http://w3c.github.io/csvw/tests/>

Starting with CSV:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_rdf("http://w3c.github.io/csvw/tests/test001.csv", format="ttl")
```

Minimal mode:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_rdf("http://w3c.github.io/csvw/tests/tree-ops.csv", mode="minimal", format="ttl")
```

Starting with metadata only:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_rdf(metadata_url="http://w3c.github.io/csvw/tests/test188-metadata.json", format="ttl")
```

Both CSV and metadata URL specified:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_rdf("http://w3c.github.io/csvw/tests/tree-ops.csv", "http://w3c.github.io/csvw/tests/tree-ops.csv", format="ttl")
```

Starting with metadata:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_json("http://w3c.github.io/csvw/tests/countries.json")
```

Starting with CSV:
```python
from csvwlib import CSVWConverter

CSVWConverter.to_json("http://w3c.github.io/csvw/tests/test001.csv")
```


## Contributors

Authored by [@Aleksander-Drozd](https://github.com/Aleksander-Drozd)

Maintained by [@DerwenAI](https://github.com/DerwenAI)