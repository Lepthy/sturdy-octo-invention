import sys

import argparse

from collections import Counter

from urllib.parse import urlparse, urljoin

from logging import Logger, getLogger
import logging

import asyncio

from bs4 import BeautifulSoup

from http_utils import HTTPClient, AIOHTTPClient


def get_links_from_soup(soup, domain: str, url: str):
    internal_links = []
    external_links = []

    domain_object = urlparse(domain)

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            href_object = urlparse(href)
            # if the scheme and domain are identical (but removes fragment and parameters)
            if href_object.scheme == domain_object.scheme and \
                    href_object.port == domain_object.port and \
                    href_object.netloc == domain_object.netloc:
                internal_links.append(urljoin(domain, href_object.path))
            # if the domain isn't specified
            elif not href_object.scheme and \
                    not href_object.netloc:
                # if the path is absolute
                if href_object.path.startswith('/'):
                    internal_links.append(urljoin(domain, href_object.path))
                # if the path is relative
                elif not href_object.path.startswith('/'):
                    internal_links.append(urljoin(url, href_object.path))
            else:
                external_links.append(href)
    return internal_links, external_links


async def fetch_page_soup(client: HTTPClient, url: str):
    response = await client.fetch(url=url, method='GET')

    if response.status_code in range(200, 300):
        soup = BeautifulSoup(response.body.decode(), 'html.parser')
        return soup
    return None


async def crawl(client: HTTPClient, domain: str, url: str):
    soup = await fetch_page_soup(client, url)
    if soup:
        internal_links, external_links = get_links_from_soup(soup, domain, url)
        return internal_links, external_links
    return ([], [])


def main(logger: Logger, domain: str) -> None:
    client = AIOHTTPClient(timeout=30, logger=logger)
    loop = asyncio.get_event_loop()

    seeds = [domain]

    # document will be our memory repository in order to keep track of the target mapping.
    document = {}

    while True:
        # This particular construct allows us to fetch all the hrefs of a given page at once, saving considerable time.
        crop = loop.run_until_complete(
            asyncio.gather(
                *[crawl(client, domain, url) for url in seeds],
                return_exceptions=True)
        )

        new_seeds = []
        for url, task_result in zip(seeds, crop):
            if isinstance(task_result, Exception):
                error = {'exception': {'type': type(task_result), 'value': str(task_result)[:32]}}
                logger.error(error)
                document[url] = {'error': error}
            else:
                internal_links, _ = task_result  # the external links are available but we do not care about them here.
                document[url] = dict(Counter(internal_links))
                internal_links = set(internal_links) - set(document.keys())
                new_seeds.extend(internal_links)
        seeds = list(set(new_seeds))  # clean out duplicates.

        if not len(seeds):
            break

    loop.close()

    print(document)


if __name__ == '__main__':
    logger = getLogger('crawler')

    FORMAT = u"[%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)s] %(message)s"
    formatter = logging.Formatter(FORMAT)

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='Domain crawler')
    parser.add_argument('-d', '--domain', type=str, required=True, help='the domain to crawl')
    args = parser.parse_args()

    main(logger=logger, domain=args.domain)
