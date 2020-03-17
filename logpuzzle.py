#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    with open(filename, "r") as apache_list:
        url_list = apache_list.read().split("\n")
        print(type(url_list))
        print(len(url_list))

    host_list = [extract_host_name(url)
                 for url in url_list if "GET " in url]

    host_list = filter(lambda url: "puzzle" in url, host_list)

    host_list = sorted(list(set(host_list)))

    return host_list


def extract_host_name(url):
    """return the host name from a given url"""

    host = re.findall(r'(GET )(\S+)( HTTP)', url)
    return host[0][1]


print("\n".join(read_urls("place_code.google.com")))


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    pass


# def create_parser():
#     """Create an argument parser object"""
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '-d', '--todir',  help='destination directory for downloaded images')
#     parser.add_argument('logfile', help='apache logfile to extract urls from')

#     return parser


# def main(args):
#     """Parse args, scan for urls, get images from urls"""
#     parser = create_parser()

#     if not args:
#         parser.print_usage()
#         sys.exit(1)

#     parsed_args = parser.parse_args(args)

#     img_urls = read_urls(parsed_args.logfile)

#     if parsed_args.todir:
#         download_images(img_urls, parsed_args.todir)
#     else:
#         print('\n'.join(img_urls))


# if __name__ == '__main__':
#     main(sys.argv[1:])
