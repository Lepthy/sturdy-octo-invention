import unittest

from bs4 import BeautifulSoup
from main import get_links_from_soup


class TestLinkExtraction(unittest.TestCase):

    def test_extract_local_wrong_scheme_link(self):
        fixture = """
        <html>
            <head>
            </head>
            <body>
                <p>
                    <a href='wss://test.domain.com/about-me'>
                </p>
            </body>
        </html>
        """
        domain = "https://test.domain.com"
        url = "https://test.domain.com/help"

        soup = BeautifulSoup(fixture, 'html.parser')
        internal_links, _ = get_links_from_soup(soup, domain, url)
        self.assertEqual(len(internal_links), 0)

    def test_extract_external_link(self):
        fixture = """
        <html>
            <head>
            </head>
            <body>
                <p>
                    <a href='https://blog.domain.com/about-me'>
                </p>
            </body>
        </html>
        """
        domain = "https://test.domain.com"
        url = "https://test.domain.com/help"

        soup = BeautifulSoup(fixture, 'html.parser')
        _, external_links = get_links_from_soup(soup, domain, url)
        self.assertEqual(external_links[0], 'https://blog.domain.com/about-me')

    def test_extract_local_full_link(self):
        fixture = """
        <html>
            <head>
            </head>
            <body>
                <p>
                    <a href='https://test.domain.com/about-me'>
                </p>
            </body>
        </html>
        """
        domain = "https://test.domain.com"
        url = "https://test.domain.com/help"

        soup = BeautifulSoup(fixture, 'html.parser')
        internal_links, _ = get_links_from_soup(soup, domain, url)
        self.assertEqual(internal_links[0], 'https://test.domain.com/about-me')

    def test_extract_local_absolute_link(self):
        fixture = """
        <html>
            <head>
            </head>
            <body>
                <p>
                    <a href='/about-me'>
                </p>
            </body>
        </html>
        """
        domain = "https://test.domain.com"
        url = "https://test.domain.com/help"

        soup = BeautifulSoup(fixture, 'html.parser')
        internal_links, _ = get_links_from_soup(soup, domain, url)
        self.assertEqual(internal_links[0], 'https://test.domain.com/about-me')

    def test_extract_local_relative_link(self):
        fixture = """
        <html>
            <head>
            </head>
            <body>
                <p>
                    <a href='about-me'>
                </p>
            </body>
        </html>
        """
        domain = "https://test.domain.com"
        url = "https://test.domain.com/help/"

        soup = BeautifulSoup(fixture, 'html.parser')
        internal_links, _ = get_links_from_soup(soup, domain, url)
        self.assertEqual(internal_links[0], 'https://test.domain.com/help/about-me')


if __name__ == '__main__':
    unittest.main()
