#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

"""

__author__ = "Janell.Huyck and knmarvel"


import os
import re
import sys
import urllib
import argparse


if sys.version_info[0] >= 3:
    raise Exception("This program requires Python 2 to run.")
    sys.exit(1)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # the file we're given is a long apache list.
    with open(filename, "r") as apache_list:
        url_list = apache_list.read().split("\n")
    # get a list of the host names for each request in the url_list
    host_list = [extract_host_name(url)
                 for url in url_list if "GET " in url]

    host_list = filter(lambda url: "puzzle" in url, host_list)
    host_list = list(set(host_list))

    second_word = re.findall(r'puzzle\/.-....-(....).jpg', host_list[0])
    host_dict = {}

    if second_word:
        for url in host_list:
            sorted_word = re.findall(r'puzzle\/.-....-(....).jpg', url)
            host_dict[url] = sorted_word
    else:
        for url in host_list:
            sorted_word = re.findall(r'puzzle\/.-(....)', url)
            host_dict[url] = sorted_word

    sorted_host_list = sorted(host_dict.items(), key=lambda x: x[1])
    sorted_host_list = [host_tuple[0] for host_tuple in sorted_host_list]

    complete_url_list = add_prefixes(filename, sorted_host_list)

    return complete_url_list


def add_prefixes(filename, host_list):
    """Adds the server prefixes to each url in the host list"""

    # extract the server name from the filename.
    # It's what's after the first _ in the filename.

    server_name = 'https://' + re.findall(r'\S+\_(\S+)', filename)[0]
    complete_url_list = [server_name + host for host in host_list]
    return complete_url_list


def extract_host_name(url):
    """return the host name from a given url"""

    host = re.findall(r'GET (\S+) HTTP', url)
    return host[0]


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    create_new_directory(dest_dir)

    # start to write out the new index.html
    index_html = '<html> \n <body> \n'

    for url in img_urls:
        img_destination = dest_dir + '/img' + str(img_urls.index(url))
        download_image(url, img_destination)
        index_html += '<img src="../' + img_destination + '"/>'

    index_html += '\n</body> \n </html>'

    with open(dest_dir + "/index.html", "w") as index_html_file:
        index_html_file.write(index_html)


def download_image(url, img_destination):
    """ Retrieves each image and saves to img_destination"""

    print('Retrieving file: ' + img_destination)
    urllib.urlretrieve(url, img_destination)


def create_new_directory(dest_dir):
    """ Checks if destination directory exists, and
    creates it if it doesn't"""

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def create_parser():
    """Create an argument parser object"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""

    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
