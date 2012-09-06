# -*- coding: utf-8 -*-
#
# bitlove-python - A Python client library for accessing the bitlove.org API
# http://github.com/stefankoegl/bitlove-python
#
# Copyright (c) 2012 Stefan Koegl <stefan@skoegl.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


""" A Python client library for accessing the bitlove.org API

Bitlove is the fully automatic Podcast download service on P2P speed. It
generates a Torrent for all media files of an RSS feed and seeds them all
the time.

https://bitlove.org/help/podcaster/api
"""


# Will be parsed by setup.py to determine package metadata
__author__ = 'Stefan Kögl <stefan@skoegl.net>'
__version__ = '0.1'
__website__ = 'https://github.com/stefankoegl/bitlove-python'
__license__ = 'Modified BSD License'


import urllib
import urllib2

try:
    import simplejson as json
except ImportError:
    import json


BITLOVE_ENCLOSURE_API='http://api.bitlove.org/by-enclosure.json?'


class BitloveClient(object):
    """ A simple client for the bitlove.org API """

    def __init__(self, user_agent):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', user_agent)]


    def get_by_enclosures(self, enclosure_urls):
        """ Get bitlove data for a list of enclosure URLs """

        # prepare URLs
        enclosure_urls = map(str.strip, enclosure_urls)
        enclosure_urls = filter(None, enclosure_urls)

        return BitloveResponse(self.opener, enclosure_urls)


class BitloveResponse(object):
    """ A lazy response to a bitlove API request """

    def __init__(self, opener, urls):
        self.urls = urls
        self.opener = opener
        self._resp = None


    def get(self, url):
        """ Get the response for the given enclosure URL """
        self._query()
        return Enclosure(self._resp.get(url), url)


    def __iter__(self):
        """ iterate over all enclosure URLs """
        self._query()
        return (Enclosure(self.get(url), url) for url in self.urls)


    def _query(self):
        """ perform a request to the API, only when necessary """

        if not self.urls:
            self._resp = {}

        elif self._resp is None:
            params = [ ('url', url) for url in self.urls]
            query = urllib.urlencode(params)

            # query API
            r = self.opener.open(BITLOVE_ENCLOSURE_API + query)
            self._resp = json.loads(r.read())


class Enclosure(object):
    """ proxies a response for an enclosure """

    def __init__(self, obj, url):
        self.url = url
        self.obj = obj


    def __getattr__(self, key):
        res = self.obj.__getitem__(key)

        if key == 'sources':
            return [Source(s) for s in res]

        return res


    def __str__(self):
        return '<{cls} {url}>'.format(cls=self.__class__.__name__,
                url=self.url)


    def __dir__(self):
        return sorted(dir(object) + self.obj.keys() + ['url'])



class Source(object):
    """ proxies the "source" part of a response """

    def __init__(self, obj):
        self.obj = obj


    def __getattr__(self, key):
        return self.obj.__getitem__(key.replace('_', '.'))


    def __str__(self):
        return '<{cls} {torrent}>'.format(cls=self.__class__.__name__,
                torrent=self.torrent)

    def __dir__(self):
        return sorted(dir(object) + self.obj.keys())
