#!/usr/bin/env python
import sys
import urlparse

import lxml.html
import requests


def get_root_url(url):
    parsed = urlparse.urlparse(url)
    return urlparse.urlunparse([
        parsed.scheme, parsed.netloc, '', '', '', ''
    ])


def get_url_path(url):
    return urlparse.urlparse(url).path



def get_internal_links_on_page(page_content, root_url):
    parsed_page = lxml.html.fromstring(page_content)
    parsed_page.make_links_absolute(root_url)

    result = {'links': set(), 'assets': set()}

    for element, _, link, _ in parsed_page.iterlinks():
        if root_url in link and element.tag == 'a':
            internal_path = get_url_path(link)
            if internal_path:
                result['links'].add(internal_path)
        elif element.tag in ['script', 'link', 'img']:
                result['assets'].add(link)

    return result


def main(args):
    root_url = get_root_url(args[0])
    seed_page = requests.get(root_url)
    links_on_page = get_internal_links_on_page(seed_page.content, root_url)
    return links_on_page['links']


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print "Usage:\n\t{} URL".format(sys.argv[0])
        sys.exit(1)
    print main(args)
