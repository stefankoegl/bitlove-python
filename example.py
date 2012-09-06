#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bitlove

# your User-Agent string
MY_USER_AGENT = 'mycoolapp/1.0 (http://example.com)'

# some enclosure URLs of media files
urls = [
    'http://spaceboyz.net/~astro/bitlove-show/bl001-introduction.webm',
    'http://spaceboyz.net/~astro/bitlove-show/bl001-introduction.subs.mkv'
]

client = bitlove.BitloveClient(MY_USER_AGENT)
resp = client.get_by_enclosures(urls)

info0 = resp.get(urls[0])

# all available attributes of info0
print dir(info0)

# we use the first available source
source0 = info0.sources[0]

# and inspect its available attributes as well
print dir(source0)

# get the torrent URL
print source0.torrent
# http://bitlove.org/astro/bitlove-show/bl001-introduction.webm.torrent

# get the Flattr link
print source0.item_payment
# http://flattr.com/thing/662636/Torrent-for-BL001-Introduction-on-Bitlove

# get the title
print source0.item_title
# The Bitlove Home Show

# for the response format see https://bitlove.org/help/podcaster/api
