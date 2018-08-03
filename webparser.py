import sys

import requests

from bs4 import BeautifulSoup

import debugging

tags = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'q',
    'blockquote', 'strong', 'em', 'del', 'ins',
    'blink', 'marquee', 'div'
]

"""

    This is simple generalized webparser.   
    Try it to train your model on following sites:

    https://lleo.me/soft/text_dip.htm

    https://proglib.io/p/5-worst-languages/

    https://proglib.io/p/ml-3months/
    
    
    The general idea of this parser's work is check only
    tags, which were listed in list 'tags'.

"""


class WebParser:

    def __init__(self, url: str):
        self.__request = requests.get(url)
        if self.__request.status_code != 200:
            message = "Status %d, terminating!" % self.__request.status_code
            debugging.webparser_logger.error(message)
            print('Cannot connect to %s.' % url)
            sys.exit(1)
        else:
            debugging.webparser_logger.info("Connection to %s success!" % url)

    def parser_content_stream(self):
        """
        Public method

        This method creates generator, which takes content for web-page,
        checks tags from 'tags' and yields text data from them.

        This method uses 'bs4' to parse text content from successful request,
        'requests' is used to get request from site.

        :return: None

        THIS FUNCTION IS USED IN TRAIN.PY
        """
        page_content = self.__request.content
        soup = BeautifulSoup(page_content, 'html.parser')
        debugging.webparser_logger.info("Parser created data stream.")
        debugging.webparser_logger.info("Parsing started.")
        for tag in tags:
            for elem in soup.find_all(tag):
                yield elem.get_text()
        debugging.webparser_logger.info("Parsing finished.")
