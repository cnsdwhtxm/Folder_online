# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: nturl2path.py
"""Convert a NT pathname to a file URL and vice versa."""

def url2pathname(url):
    """OS-specific conversion from a relative URL of the 'file' scheme
    to a file system path; not recommended for general use."""
    import string, urllib.parse
    url = url.replace(':', '|')
    if '|' not in url:
        if url[:4] == '////':
            url = url[2:]
        components = url.split('/')
        return urllib.parse.unquote('\\'.join(components))
    else:
        comp = url.split('|')
        if len(comp) != 2 or comp[0][(-1)] not in string.ascii_letters:
            error = 'Bad URL: ' + url
            raise OSError(error)
        drive = comp[0][(-1)].upper()
        components = comp[1].split('/')
        path = drive + ':'
        for comp in components:
            if comp:
                path = path + '\\' + urllib.parse.unquote(comp)

        if path.endswith(':') and url.endswith('/'):
            path += '\\'
        return path


def pathname2url(p):
    """OS-specific conversion from a file system path to a relative URL
    of the 'file' scheme; not recommended for general use."""
    import urllib.parse
    if ':' not in p:
        if p[:2] == '\\\\':
            p = '\\\\' + p
        components = p.split('\\')
        return urllib.parse.quote('/'.join(components))
    else:
        comp = p.split(':')
        if len(comp) != 2 or len(comp[0]) > 1:
            error = 'Bad path: ' + p
            raise OSError(error)
        drive = urllib.parse.quote(comp[0].upper())
        components = comp[1].split('\\')
        path = '///' + drive + ':'
        for comp in components:
            if comp:
                path = path + '/' + urllib.parse.quote(comp)

        return path