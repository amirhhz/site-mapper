"""
write a web crawler. It should be limited to one domain - so when crawling
xyz.com it would crawl all pages within the xyz.com domain, but not follow
the links to the Facebook and Twitter accounts. Given a URL, it should output
a site map, showing which static assets each page depends on, and the links
between pages. Choose the most appropriate data structure to store & display
this site map.
"""
import unittest

from site_mapper import mapper_cli


class SiteMapperAcceptanceTests(unittest.TestCase):

    def test_mapper_cli_happy_day(self):
        """
        Run a test server by going example/ and running:
            python -m SimpleHTTPServer
        """
        result = mapper_cli.main('http://localhost:8000')
        home_page = result['/']
        team_page = result['/company/team.html']
        products_page = result['/products.html']

        self.assertEqual(
            home_page,
            {
                'pages': {
                    '/',
                    '/company/team.html',
                    '/products.html',
                },
                'assets': {
                    'http://cdn.com/lib.js',
                    'http://localhost:8000/app.js',
                    'http://localhost:8000/app.css',
                }
            }
        )

        self.assertEqual(
            team_page,
            {
                'pages': {
                    '/',
                    '/products.html',
                },
                'assets': {
                    'http://cdn.com/lib.js',
                    'https://cdn.com/img.jpg',
                }
            }
        )

        self.assertEqual(
            products_page,
            {
                'pages': {
                    '/',
                    '/company/team.html',
                },
                'assets': {
                    'http://cdn.com/lib.js',
                    'http://localhost:8000/app.js',
                }
            }
        )


class SiteMapperCliTests(unittest.TestCase):

    def test_get_root_url(self):
        result = mapper_cli.get_root_url(
            'http://www.example.com:80/hello?param=value'
        )
        self.assertEqual(result, 'http://www.example.com:80')

    def test_get_root_url_strips_fragments(self):
        result = mapper_cli.get_root_url(
            'http://www.example.com:80/hello#title1'
        )
        self.assertEqual(result, 'http://www.example.com:80')

    def test_get_url_path_strips_fragments(self):
        result = mapper_cli.get_url_path(
            'http://www.example.com:80/hello#title1'
        )
        self.assertEqual(result, '/hello')


    def test_format_links_data_prints_links_in_sorted_order(self):
        output = mapper_cli.format_links_data(
            '/page', 'pages', ['/hello', '/bye'])
        self.assertEqual(
            output,
            [
                "Page '/page' has links to these pages:",
                "\t/bye",
                "\t/hello",
                "",
            ]
        )


class SiteMapperPageParsingTests(unittest.TestCase):


    def setUp(self):
        self.page_content = """
        <html>
        <head>
        </head>
            <script src="app.js"></script>
            <script src="//cdn.com/lib.js"></script>
            <link href="app.css" />
        <body>
            <a href="/about">
            About us
            </a>
            <a href="/terms">
            </a>
            <a href="http://external.com/">
            </a>
            <a href="/about#fun">
            <img src="https://cdn.someplace.com/img.png" />
            <img src="/fun.jpg" />
            </a>
            <a href="#footnote">
            </a>
            <a href="http://example.com/logout#footnote">
            </a>
        </body>
        </html>
        """


    def test_filter_links_on_page(self):
        # TODO break this test into smaller ones for each behaviour
        links = mapper_cli.filter_links_on_page(
            self.page_content, 'http://example.com'
        )

        self.assertEqual(
            links,
            {
                'pages': {'/about', '/terms', '/logout'},
                'assets': {
                    'http://example.com/app.js',
                    'http://cdn.com/lib.js',
                    'http://example.com/app.css',
                    'https://cdn.someplace.com/img.png',
                    'http://example.com/fun.jpg',
                },
            }
        )
