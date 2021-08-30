# Faker Providers (SG Context)



This project implements a few Providers for [Faker](https://github.com/joke2k/faker) Python package.

List of Providers:

* Singapore NRIC, including residents and foreigners
* Singapore local address, using HDB addresses



## SG NRIC

Reference: https://en.wikipedia.org/wiki/National_Registration_Identity_Card

There are 5 different NRIC types in Singapore.

* "S": "Singapore citizens and permanent residents born before 1 January 2000."
* "T": "Singapore citizens and permanent residents born on or after 1 January 2000"
* "F": "Foreigners issued with long-term passes before 1 January 2000"
* "G": "Foreigners issued with long-term passes from 1 January 2000 to 31 December 2021"
* "M": "Foreigners issued with long-term passes on or after 1 January 2022"



Following code will generate 5 NRIC of different types.

```python
from providers import SgNricProvider

fake = Faker()
fake.add_provider(SgNricProvider)
fake.sg_nric()
```

You can adjust some parameters:

* categories:	Type of NRIC
* count:     Number of records to be generated
* min_age:     Minimum age of the fake person, which affects the type of NRIC
* max_age:    Maximum age of the fake person, which affects the type of NRIC

```
fake.sg_nric(categories=['S', 'T', 'F', 'G', 'M'], count=5, min_age=0, max_age=115)
```

Sample Data

```json
[{"birthday": "2021-03-28", "nric": "M7577745J"},
 {"birthday": "2012-10-10", "nric": "T1264033A"},
 {"birthday": "2005-03-19", "nric": "T0571172Z"},
 {"birthday": "1939-11-25", "nric": "S2992344B"},
 {"birthday": "1953-03-04", "nric": "S1354649E"}]
```





## SG Address

Reference from kaggle https://www.kaggle.com/mylee2009/singapore-postal-code-mapper

The returned data are actually HDB addresses.

Following code returns 5 records of fake data. 

```python
from providers import SgAddressProvider

fake = Faker()
fake.add_provider(SgAddressProvider)
fake.sg_nric()
```



Parameter(s):

* count:     Number of records to return. Default value 5.



Sample Data

```json
[{'postal': '787916',
  'latitude': '1.397338704',
  'longtitude': '103.8204766',
  'blk_no': '10',
  'road_name': 'SPRINGLEAF VIEW'},
 {'postal': '821107',
  'latitude': '1.397198794',
  'longtitude': '103.9068258',
  'blk_no': '107A',
  'road_name': 'EDGEFIELD PLAINS'}]
```



