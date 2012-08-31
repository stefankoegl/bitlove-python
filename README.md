bitlove-python
==============

A very simple client for the [bitlove.org API](https://bitlove.org/help/podcaster/api).

Usage
-----

    import bitlove

    # your User-Agent string
    MY_USER_AGENT = 'mycoolapp/1.0 (http://example.com)'

    # some enclosure URLs of media files
    url = [
        'http://spaceboyz.net/~astro/bitlove-show/bl001-introduction.webm',
        'http://spaceboyz.net/~astro/bitlove-show/bl001-introduction.subs.mkv'
    ]

    client = bitlove.BitloveClient(MY_USER_AGENT)
    resp = client.get_by_enclosures(urls)

    info0 = resp.get(url[0])

    # get the torrent URL
    print info0['sources'][0]['torrent']
    # http://bitlove.org/astro/bitlove-show/bl001-introduction.webm.torrent

    # get the Flattr link
    print info0['sources'][0]['payment']
    # http://flattr.com/thing/662636/Torrent-for-BL001-Introduction-on-Bitlove

    # get the title
    print info0['sources'][0]['title']
    # The Bitlove Home Show

    # for the response format see https://bitlove.org/help/podcaster/api
