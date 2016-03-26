# NLS Post Office Directory Parser
System for reading OCRed Post Office directories from the [National Library of Scotland](http://digital.nls.uk/directories/) and storing them in a database.

## Requirements
This software requires the following Python libraries:
- [arff](https://pypi.python.org/pypi/arff/0.9)
- [editdistance](https://pypi.python.org/pypi/editdistance/0.2)
- [nltk](https://pypi.python.org/pypi/nltk/3.1)
- [numpy](https://pypi.python.org/pypi/numpy/1.10.1)
- [rdflib](https://pypi.python.org/pypi/rdflib/4.2.1)
- [scikit-learn](https://pypi.python.org/pypi/scikit-learn/0.17)
- [scipy](https://pypi.python.org/pypi/scipy/0.16.1)
- [sklearn](https://pypi.python.org/pypi/sklearn/0.0)

Also, if you wish to run the testing scripts, you will need:
- [tabulate](https://pypi.python.org/pypi/tabulate/0.7.5)

Additionally, to run the supplied OCR scripts, you will need:
- [SCRIBO](https://www.lrde.epita.fr/wiki/Olena/Modules#SCRIBO)

## Installation
To install this software from the git repository, do:

```
git clone https://github.com/AllanB3/nls-semantic-tagging.git
```

## Parsing Documents

### OCR
The supplied OCR script takes scans of Post Office directories in PDF form and produces a XML transcript. In order to use the supplied OCR script, run:

```
./ocr_process.sh /path/to/PDF start end
```

where ```start``` and ```end``` are the first and last pages you want to be included in the XML transcript.

### Extracting Entries to Database From XML Transcripts
To extract Post Office directory entries from XML transcripts to the database, do:

```
python3 entryExtractor.py /path/to/XML/transcript source year
```

where ```year``` is the year of publication for the directory and ```source``` is the source of the XML transcript. This will take one of three:

- ```ocr```: the XML transcript is from the supplied OCR module
- ```page```: the XML transcript is of a page downloaded from [the National Library of Scotland](http://digital.nls.uk/directories/)
- ```directory```: the XML transcript is of a directory downloaded from [the National Library of Scotland](http://digital.nls.uk/directories/)

## Querying the Database
To submit a query to the database, do:

```
python3 databaseQuerier.py
```

This script takes the following options:

- ```-s```, ```--surname```: the surname on which to search the database
- ```-f```, ```--forename```: the forename on which to search the database
- ```-t```, ```--title```: the title on which to search the database
- ```-j```, ```--job```: the occupation on which to search the database
- ```-a```, ```--address```: the address on which to search the database
- ```-l```, ```--lat```: the latitude on which to search the database
- ```-o```, ```--lon```: the longitude on which to search the database
- ```-y```, ```--year```: the year on which to search the database
- ```-b```, ```--bkv```: the block key value on which to search the database

## Linking Records From Across the Database
To search the whole database for records pertaining to the same individuals and match them, do:

```
python3 recordLinker.py
```

This script will search the database for records pertaining to the same individuals and link them in the database.

**WARNING**: This will take some time.
