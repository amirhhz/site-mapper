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


def filter_links_on_page(page_content, root_url):
    parsed_page = lxml.html.fromstring(page_content)
    parsed_page.make_links_absolute(root_url)

    result = {'pages': set(), 'assets': set()}

    for element, _, link, _ in parsed_page.iterlinks():
        if root_url in link and element.tag == 'a':
            internal_path = get_url_path(link)
            if internal_path:
                result['pages'].add(internal_path)
        elif element.tag in ['script', 'link', 'img']:
            result['assets'].add(link)

    return result


def process_link(root_url, path):
    # TODO handle network or http failures
    seed_page = requests.get(root_url + path)
    return filter_links_on_page(seed_page.content, root_url)


def main(entry_url):
    sitemap = {}
    path_queue = set(['/'])
    root_url = get_root_url(entry_url)
    while path_queue:
        current_path = path_queue.pop()

        links_on_page = process_link(root_url, current_path)
        new_pages = {
            link for link in links_on_page['pages']
            if link not in sitemap
        }
        path_queue.update(new_pages)
        sitemap[current_path] = links_on_page

    return sitemap


def format_links_data(page_url, link_type, links):
    lines = []
    lines.append("Page '{}' has links to these {}:".format(
        page_url, link_type
    ))
    for link in sorted(links):
        lines.append("\t{}".format(link))

    lines.append('')
    return lines


def present_sitemap(sitemap):
    for page, link_data in sitemap.iteritems():
        print "-" * 72
        for line in format_links_data(page, 'pages', link_data['pages']):
            print line

        for line in format_links_data(page, 'assets', link_data['assets']):
            print line


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        print "Usage:\n\t{} URL".format(sys.argv[0])
        sys.exit(1)

    present_sitemap(main(args[0]))

