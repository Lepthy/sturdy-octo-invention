# Crawler

## Disclaimer

This project was rushed in order to reach the release state as fast as possible, tests on critical paths
were added in order to assure the minimum level of reliability. 

The only part of the code that was given special attention is the src/http_utils.py file as it is most likeley the one that will see the most reusability. 

## TODO

* Refactor with data classes and actors
* Add more tests

## Dependencies of this project

* docker
* python3

## Purpose of this project

This project crawl a given domain in order to find every discoverable page through <a> hrefs.

The resulting JSON document contains pages url as the keys and the links and their count as a value:

```json
{URL: {HREF: COUNT}}
```

## Development

In order to start extending this project you will have to run:

```bash
make setup-tests
```

in order to install the python dependencies

Due to time constraints, unit test only cover the main logic path (recognizing and extracting links) as of now. 
More will be added as development progess.

## Build

The docker image can be built with:

```bash
make build
```

Note that the build is prefaced with a run of the tests.

## Run

This project can be run with:

```bash
docker run crawler -d https://aimbrain.com
```

or 

```bash
bash run.sh
```

## Architecture

This project is really simple and rely only on one bit of logic, asyncio.gather (main.py at the time of this writing). 

First we create a list of url to gather, then in the event loop we asynchronously fetch each of them, and then proceed
to analyse the list of (url, result) tuple (the zip(url, crop) construct) in order to do a headcount of the links in
each of the pages. 

We then proceed to start over after streamlining the results from the previous iteration. 

When there is no result left, we successfully fetched every single link discoverable on the target domain. 

