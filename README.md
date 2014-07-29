Diavgeia
========

A crawler that leverages Diavgeia's [OpenDataAPI](https://diavgeia.gov.gr/api/help) 
to download decisions as well as their respective metadata.

Prerequisites
-------------

- Python 2.7.x
- Scrapy

Introduction
------------

The cralwer parses command line arguments (as defined by Scrapy Framework), and
performs the respective calls to Diavgeia's OpenData API in order to fetch
decisions metadata and documents. Documents are downloaded using a seperate
threaded downloader pipeline. Currently the work on this project is ongoing.

Settings
--------
Diavgeia stores its configuration under diavgeia/settings.py file. The values
that are configurable are the following:

- `DOWNLOAD_DIR`: The directory where the downloader pipeline stores the
  decision documents. To avoid resulting to a directory full of documents, the
  downloader seggregates decisions by their organization id. Therefore when a decision 
  is downloaded, a new subdirectory is created (if not exists) named under the
  organization ID. Default is `/tmp/diavgeia`
- `THREADS`: Number of concurrent threads that will be used to download decision 
  documents. Default is 15.

Run Diavgeia
------------
Diavgeia can be run using the following command: 
`scrapy crawl diavgeia_spider`
The above command fetches decision documents that were submitted to Diavgeia the previous 
day. Queries can be performed to Diavgeia using search arguments defined by the API.
Such arguments can be passed to the crawler with the `-a` flag. 
e.g: If we wish to search every decision published by an organization we can use the 
following command: `scrapy crawl diavgeia_spider -a org=30` where 30 is the organization ID.
Diavgeia allows us to request an organization using its name as well.

Allowed arguments for the spider are depicted on the following table:

| `ada`			| Unique decision ID
| `org`			| ID or latin name of organization
| `subject`	| Subject of the decision
| `protocol`	| Protocol number
| `term`			| General search term
| `unit`			| Unit ID 
| `signer`		| Signer ID
| `type`			| Type of decisions
| `tag`			| Category tag
| `from_date`		| From submission date (in YYYY-MM-DD format)
| `to_date`		| To submission date (in YYYY-MM-DD format)
| `from_issue_date`	| From issue date (in YYYY-MM-DD format)
| `status`		| To issue date (in YYYY-MM-DD format)
| `size`			| Results size.

<!-- vi: tw=80 -->
