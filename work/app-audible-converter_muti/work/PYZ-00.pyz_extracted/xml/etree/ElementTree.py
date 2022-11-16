# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: xml\etree\ElementTree.py
"""Lightweight XML support for Python.

 XML is an inherently hierarchical data format, and the most natural way to
 represent it is with a tree.  This module has two classes for this purpose:

    1. ElementTree represents the whole XML document as a tree and

    2. Element represents a single node in this tree.

 Interactions with the whole document (reading and writing to/from files) are
 usually done on the ElementTree level.  Interactions with a single XML element
 and its sub-elements are done on the Element level.

 Element is a flexible container object designed to store hierarchical data
 structures in memory. It can be described as a cross between a list and a
 dictionary.  Each Element has a number of properties associated with it:

    'tag' - a string containing the element's name.

    'attributes' - a Python dictionary storing the element's attributes.

    'text' - a string containing the element's text content.

    'tail' - an optional string containing text after the element's end tag.

    And a number of child elements stored in a Python sequence.

 To create an element instance, use the Element constructor,
 or the SubElement factory function.

 You can also use the ElementTree class to wrap an element structure
 and convert it to and from XML.

"""
__all__ = [
 'Comment',
 'dump',
 'Element', 'ElementTree',
 'fromstring', 'fromstringlist',
 'iselement', 'iterparse',
 'parse', 'ParseError',
 'PI', 'ProcessingInstruction',
 'QName',
 'SubElement',
 'tostring', 'tostringlist',
 'TreeBuilder',
 'VERSION',
 'XML', 'XMLID',
 'XMLParser', 'XMLPullParser',
 'register_namespace']
VERSION = '1.3.0'
import sys, re, warnings, io, collections, contextlib
from . import ElementPath

class ParseError(SyntaxError):
    __doc__ = "An error when parsing an XML document.\n\n    In addition to its exception value, a ParseError contains\n    two extra attributes:\n        'code'     - the specific exception code\n        'position' - the line and column of the error\n\n    "


def iselement(element):
    """Return True if *element* appears to be an Element."""
    return hasattr(element, 'tag')


class Element:
    __doc__ = "An XML element.\n\n    This class is the reference implementation of the Element interface.\n\n    An element's length is its number of subelements.  That means if you\n    want to check if an element is truly empty, you should check BOTH\n    its length AND its text attribute.\n\n    The element tag, attribute names, and attribute values can be either\n    bytes or strings.\n\n    *tag* is the element name.  *attrib* is an optional dictionary containing\n    element attributes. *extra* are additional element attributes given as\n    keyword arguments.\n\n    Example form:\n        <tag attrib>text<child/>...</tag>tail\n\n    "
    tag = None
    attrib = None
    text = None
    tail = None

    def __init__(self, tag, attrib={}, **extra):
        if not isinstance(attrib, dict):
            raise TypeError('attrib must be dict, not %s' % (
             attrib.__class__.__name__,))
        attrib = attrib.copy()
        attrib.update(extra)
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def __repr__(self):
        return '<%s %r at %#x>' % (self.__class__.__name__, self.tag, id(self))

    def makeelement(self, tag, attrib):
        """Create a new element with the same type.

        *tag* is a string containing the element name.
        *attrib* is a dictionary containing the element attributes.

        Do not call this method, use the SubElement factory function instead.

        """
        return self.__class__(tag, attrib)

    def copy(self):
        """Return copy of current element.

        This creates a shallow copy. Subelements will be shared with the
        original tree.

        """
        elem = self.makeelement(self.tag, self.attrib)
        elem.text = self.text
        elem.tail = self.tail
        elem[:] = self
        return elem

    def __len__(self):
        return len(self._children)

    def __bool__(self):
        warnings.warn("The behavior of this method will change in future versions.  Use specific 'len(elem)' or 'elem is not None' test instead.",
          FutureWarning,
          stacklevel=2)
        return len(self._children) != 0

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, element):
        self._children[index] = element

    def __delitem__(self, index):
        del self._children[index]

    def append(self, subelement):
        """Add *subelement* to the end of this element.

        The new element will appear in document order after the last existing
        subelement (or directly after the text, if it's the first subelement),
        but before the end tag for this element.

        """
        self._assert_is_element(subelement)
        self._children.append(subelement)

    def extend(self, elements):
        """Append subelements from a sequence.

        *elements* is a sequence with zero or more elements.

        """
        for element in elements:
            self._assert_is_element(element)

        self._children.extend(elements)

    def insert(self, index, subelement):
        """Insert *subelement* at position *index*."""
        self._assert_is_element(subelement)
        self._children.insert(index, subelement)

    def _assert_is_element(self, e):
        if not isinstance(e, _Element_Py):
            raise TypeError('expected an Element, not %s' % type(e).__name__)

    def remove(self, subelement):
        """Remove matching subelement.

        Unlike the find methods, this method compares elements based on
        identity, NOT ON tag value or contents.  To remove subelements by
        other means, the easiest way is to use a list comprehension to
        select what elements to keep, and then use slice assignment to update
        the parent element.

        ValueError is raised if a matching element could not be found.

        """
        self._children.remove(subelement)

    def getchildren(self):
        """(Deprecated) Return all subelements.

        Elements are returned in document order.

        """
        warnings.warn("This method will be removed in future versions.  Use 'list(elem)' or iteration over elem instead.",
          DeprecationWarning,
          stacklevel=2)
        return self._children

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        return ElementPath.find(self, path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """Find text for first matching element by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *default* is the value to return if the element was not found,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return text content of first matching element, or default value if
        none was found.  Note that if an element is found having no text
        content, the empty string is returned.

        """
        return ElementPath.findtext(self, path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Returns list containing all matching elements in document order.

        """
        return ElementPath.findall(self, path, namespaces)

    def iterfind(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return an iterable yielding all matching elements in document order.

        """
        return ElementPath.iterfind(self, path, namespaces)

    def clear(self):
        """Reset element.

        This function removes all subelements, clears all attributes, and sets
        the text and tail attributes to None.

        """
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None

    def get(self, key, default=None):
        """Get element attribute.

        Equivalent to attrib.get, but some implementations may handle this a
        bit more efficiently.  *key* is what attribute to look for, and
        *default* is what to return if the attribute was not found.

        Returns a string containing the attribute value, or the default if
        attribute was not found.

        """
        return self.attrib.get(key, default)

    def set(self, key, value):
        """Set element attribute.

        Equivalent to attrib[key] = value, but some implementations may handle
        this a bit more efficiently.  *key* is what attribute to set, and
        *value* is the attribute value to set it to.

        """
        self.attrib[key] = value

    def keys(self):
        """Get list of attribute names.

        Names are returned in an arbitrary order, just like an ordinary
        Python dict.  Equivalent to attrib.keys()

        """
        return self.attrib.keys()

    def items(self):
        """Get element attributes as a sequence.

        The attributes are returned in arbitrary order.  Equivalent to
        attrib.items().

        Return a list of (name, value) tuples.

        """
        return self.attrib.items()

    def iter(self, tag=None):
        """Create tree iterator.

        The iterator loops over the element and all subelements in document
        order, returning all elements with a matching tag.

        If the tree structure is modified during iteration, new or removed
        elements may or may not be included.  To get a stable set, use the
        list() function on the iterator, and loop over the resulting list.

        *tag* is what tags to look for (default is to return all elements)

        Return an iterator containing all the matching elements.

        """
        if tag == '*':
            tag = None
        if tag is None or self.tag == tag:
            yield self
        for e in self._children:
            yield from e.iter(tag)

    def getiterator(self, tag=None):
        warnings.warn("This method will be removed in future versions.  Use 'elem.iter()' or 'list(elem.iter())' instead.",
          PendingDeprecationWarning,
          stacklevel=2)
        return list(self.iter(tag))

    def itertext(self):
        """Create text iterator.

        The iterator loops over the element and all subelements in document
        order, returning all inner text.

        """
        tag = self.tag
        if not isinstance(tag, str):
            if tag is not None:
                return
        t = self.text
        if t:
            yield t
        for e in self:
            yield from e.itertext()
            t = e.tail
            if t:
                yield t


def SubElement(parent, tag, attrib={}, **extra):
    """Subelement factory which creates an element instance, and appends it
    to an existing parent.

    The element tag, attribute names, and attribute values can be either
    bytes or Unicode strings.

    *parent* is the parent element, *tag* is the subelements name, *attrib* is
    an optional directory containing element attributes, *extra* are
    additional attributes given as keyword arguments.

    """
    attrib = attrib.copy()
    attrib.update(extra)
    element = parent.makeelement(tag, attrib)
    parent.append(element)
    return element


def Comment(text=None):
    """Comment element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *text* is a string containing the comment string.

    """
    element = Element(Comment)
    element.text = text
    return element


def ProcessingInstruction(target, text=None):
    """Processing Instruction element factory.

    This function creates a special element which the standard serializer
    serializes as an XML comment.

    *target* is a string containing the processing instruction, *text* is a
    string containing the processing instruction contents, if any.

    """
    element = Element(ProcessingInstruction)
    element.text = target
    if text:
        element.text = element.text + ' ' + text
    return element


PI = ProcessingInstruction

class QName:
    __doc__ = 'Qualified name wrapper.\n\n    This class can be used to wrap a QName attribute value in order to get\n    proper namespace handing on output.\n\n    *text_or_uri* is a string containing the QName value either in the form\n    {uri}local, or if the tag argument is given, the URI part of a QName.\n\n    *tag* is an optional argument which if given, will make the first\n    argument (text_or_uri) be interpreted as a URI, and this argument (tag)\n    be interpreted as a local name.\n\n    '

    def __init__(self, text_or_uri, tag=None):
        if tag:
            text_or_uri = '{%s}%s' % (text_or_uri, tag)
        self.text = text_or_uri

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.text)

    def __hash__(self):
        return hash(self.text)

    def __le__(self, other):
        if isinstance(other, QName):
            return self.text <= other.text
        else:
            return self.text <= other

    def __lt__(self, other):
        if isinstance(other, QName):
            return self.text < other.text
        else:
            return self.text < other

    def __ge__(self, other):
        if isinstance(other, QName):
            return self.text >= other.text
        else:
            return self.text >= other

    def __gt__(self, other):
        if isinstance(other, QName):
            return self.text > other.text
        else:
            return self.text > other

    def __eq__(self, other):
        if isinstance(other, QName):
            return self.text == other.text
        else:
            return self.text == other


class ElementTree:
    __doc__ = 'An XML element hierarchy.\n\n    This class also provides support for serialization to and from\n    standard XML.\n\n    *element* is an optional root element node,\n    *file* is an optional file handle or file name of an XML file whose\n    contents will be used to initialize the tree with.\n\n    '

    def __init__(self, element=None, file=None):
        self._root = element
        if file:
            self.parse(file)

    def getroot(self):
        """Return root element of this tree."""
        return self._root

    def _setroot(self, element):
        """Replace root element of this tree.

        This will discard the current contents of the tree and replace it
        with the given element.  Use with care!

        """
        self._root = element

    def parse(self, source, parser=None):
        """Load external XML document into element tree.

        *source* is a file name or file object, *parser* is an optional parser
        instance that defaults to XMLParser.

        ParseError is raised if the parser fails to parse the document.

        Returns the root element of the given source document.

        """
        close_source = False
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
            close_source = True
        try:
            if parser is None:
                parser = XMLParser()
                if hasattr(parser, '_parse_whole'):
                    self._root = parser._parse_whole(source)
                    return self._root
            while True:
                data = source.read(65536)
                if not data:
                    break
                parser.feed(data)

            self._root = parser.close()
            return self._root
        finally:
            if close_source:
                source.close()

    def iter(self, tag=None):
        """Create and return tree iterator for the root element.

        The iterator loops over all elements in this tree, in document order.

        *tag* is a string with the tag name to iterate over
        (default is to return all elements).

        """
        return self._root.iter(tag)

    def getiterator(self, tag=None):
        warnings.warn("This method will be removed in future versions.  Use 'tree.iter()' or 'list(tree.iter())' instead.",
          PendingDeprecationWarning,
          stacklevel=2)
        return list(self.iter(tag))

    def find(self, path, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().find(path), which is Element.find()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.find(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """Find first matching element by tag name or path.

        Same as getroot().findtext(path),  which is Element.findtext()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return the first matching element, or None if no element was found.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.findtext(path, default, namespaces)

    def findall(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().findall(path), which is Element.findall().

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return list containing all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.findall(path, namespaces)

    def iterfind(self, path, namespaces=None):
        """Find all matching subelements by tag name or path.

        Same as getroot().iterfind(path), which is element.iterfind()

        *path* is a string having either an element tag or an XPath,
        *namespaces* is an optional mapping from namespace prefix to full name.

        Return an iterable yielding all matching elements in document order.

        """
        if path[:1] == '/':
            path = '.' + path
            warnings.warn(('This search is broken in 1.3 and earlier, and will be fixed in a future version.  If you rely on the current behaviour, change it to %r' % path),
              FutureWarning,
              stacklevel=2)
        return self._root.iterfind(path, namespaces)

    def write(self, file_or_filename, encoding=None, xml_declaration=None, default_namespace=None, method=None, *, short_empty_elements=True):
        """Write element tree to a file as XML.

        Arguments:
          *file_or_filename* -- file name or a file object opened for writing

          *encoding* -- the output encoding (default: US-ASCII)

          *xml_declaration* -- bool indicating if an XML declaration should be
                               added to the output. If None, an XML declaration
                               is added if encoding IS NOT either of:
                               US-ASCII, UTF-8, or Unicode

          *default_namespace* -- sets the default XML namespace (for "xmlns")

          *method* -- either "xml" (default), "html, "text", or "c14n"

          *short_empty_elements* -- controls the formatting of elements
                                    that contain no content. If True (default)
                                    they are emitted as a single self-closed
                                    tag, otherwise they are emitted as a pair
                                    of start/end tags

        """
        if not method:
            method = 'xml'
        elif method not in _serialize:
            raise ValueError('unknown method %r' % method)
        else:
            if encoding or method == 'c14n':
                encoding = 'utf-8'
            else:
                encoding = 'us-ascii'
        enc_lower = encoding.lower()
        with _get_writer(file_or_filename, enc_lower) as (write):
            if method == 'xml':
                if xml_declaration or xml_declaration is None and enc_lower not in ('utf-8',
                                                                                    'us-ascii',
                                                                                    'unicode'):
                    declared_encoding = encoding
                    if enc_lower == 'unicode':
                        import locale
                        declared_encoding = locale.getpreferredencoding()
                    write("<?xml version='1.0' encoding='%s'?>\n" % (
                     declared_encoding,))
            if method == 'text':
                _serialize_text(write, self._root)
            else:
                qnames, namespaces = _namespaces(self._root, default_namespace)
                serialize = _serialize[method]
                serialize(write, (self._root), qnames, namespaces, short_empty_elements=short_empty_elements)

    def write_c14n(self, file):
        return self.write(file, method='c14n')


@contextlib.contextmanager
def _get_writer(file_or_filename, encoding):
    try:
        write = file_or_filename.write
    except AttributeError:
        if encoding == 'unicode':
            file = open(file_or_filename, 'w')
        else:
            file = open(file_or_filename, 'w', encoding=encoding, errors='xmlcharrefreplace')
        with file:
            yield file.write
    else:
        if encoding == 'unicode':
            yield write
        else:
            with contextlib.ExitStack() as (stack):
                if isinstance(file_or_filename, io.BufferedIOBase):
                    file = file_or_filename
                else:
                    if isinstance(file_or_filename, io.RawIOBase):
                        file = io.BufferedWriter(file_or_filename)
                        stack.callback(file.detach)
                    else:
                        file = io.BufferedIOBase()
                        file.writable = lambda : True
                        file.write = write
                try:
                    file.seekable = file_or_filename.seekable
                    file.tell = file_or_filename.tell
                except AttributeError:
                    pass

                file = io.TextIOWrapper(file, encoding=encoding,
                  errors='xmlcharrefreplace',
                  newline='\n')
                stack.callback(file.detach)
                yield file.write


def _namespaces(elem, default_namespace=None):
    qnames = {None: None}
    namespaces = {}
    if default_namespace:
        namespaces[default_namespace] = ''

    def add_qname(qname):
        try:
            if qname[:1] == '{':
                uri, tag = qname[1:].rsplit('}', 1)
                prefix = namespaces.get(uri)
                if prefix is None:
                    prefix = _namespace_map.get(uri)
                    if prefix is None:
                        prefix = 'ns%d' % len(namespaces)
                    if prefix != 'xml':
                        namespaces[uri] = prefix
                if prefix:
                    qnames[qname] = '%s:%s' % (prefix, tag)
                else:
                    qnames[qname] = tag
            else:
                if default_namespace:
                    raise ValueError('cannot use non-qualified names with default_namespace option')
                qnames[qname] = qname
        except TypeError:
            _raise_serialization_error(qname)

    for elem in elem.iter():
        tag = elem.tag
        if isinstance(tag, QName):
            if tag.text not in qnames:
                add_qname(tag.text)
            else:
                if isinstance(tag, str):
                    if tag not in qnames:
                        add_qname(tag)
                elif tag is not None:
                    if tag is not Comment:
                        if tag is not PI:
                            _raise_serialization_error(tag)
            for key, value in elem.items():
                if isinstance(key, QName):
                    key = key.text
                if key not in qnames:
                    add_qname(key)
                if isinstance(value, QName) and value.text not in qnames:
                    add_qname(value.text)

            text = elem.text
            if isinstance(text, QName) and text.text not in qnames:
                add_qname(text.text)

    return (
     qnames, namespaces)


def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is Comment:
        write('<!--%s-->' % text)
    else:
        if tag is ProcessingInstruction:
            write('<?%s?>' % text)
        else:
            tag = qnames[tag]
    if tag is None:
        if text:
            write(_escape_cdata(text))
        for e in elem:
            _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)

    else:
        write('<' + tag)
        items = list(elem.items())
        if items or namespaces:
            if namespaces:
                for v, k in sorted((namespaces.items()), key=(lambda x: x[1])):
                    if k:
                        k = ':' + k
                    write(' xmlns%s="%s"' % (
                     k,
                     _escape_attrib(v)))

            for k, v in sorted(items):
                if isinstance(k, QName):
                    k = k.text
                else:
                    if isinstance(v, QName):
                        v = qnames[v.text]
                    else:
                        v = _escape_attrib(v)
                write(' %s="%s"' % (qnames[k], v))

        if text or len(elem) or not short_empty_elements:
            write('>')
            if text:
                write(_escape_cdata(text))
            for e in elem:
                _serialize_xml(write, e, qnames, None, short_empty_elements=short_empty_elements)

            write('</' + tag + '>')
        else:
            write(' />')
    if elem.tail:
        write(_escape_cdata(elem.tail))


HTML_EMPTY = ('area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input',
              'isindex', 'link', 'meta', 'param')
try:
    HTML_EMPTY = set(HTML_EMPTY)
except NameError:
    pass

def _serialize_html(write, elem, qnames, namespaces, **kwargs):
    tag = elem.tag
    text = elem.text
    if tag is Comment:
        write('<!--%s-->' % _escape_cdata(text))
    else:
        if tag is ProcessingInstruction:
            write('<?%s?>' % _escape_cdata(text))
        else:
            tag = qnames[tag]
    if tag is None:
        if text:
            write(_escape_cdata(text))
        for e in elem:
            _serialize_html(write, e, qnames, None)

    else:
        write('<' + tag)
        items = list(elem.items())
        if items or namespaces:
            if namespaces:
                for v, k in sorted((namespaces.items()), key=(lambda x: x[1])):
                    if k:
                        k = ':' + k
                    write(' xmlns%s="%s"' % (
                     k,
                     _escape_attrib(v)))

            for k, v in sorted(items):
                if isinstance(k, QName):
                    k = k.text
                else:
                    if isinstance(v, QName):
                        v = qnames[v.text]
                    else:
                        v = _escape_attrib_html(v)
                write(' %s="%s"' % (qnames[k], v))

        write('>')
        ltag = tag.lower()
        if text:
            if ltag == 'script' or ltag == 'style':
                write(text)
            else:
                write(_escape_cdata(text))
        for e in elem:
            _serialize_html(write, e, qnames, None)

    if ltag not in HTML_EMPTY:
        write('</' + tag + '>')
    if elem.tail:
        write(_escape_cdata(elem.tail))


def _serialize_text(write, elem):
    for part in elem.itertext():
        write(part)

    if elem.tail:
        write(elem.tail)


_serialize = {'xml':_serialize_xml, 
 'html':_serialize_html, 
 'text':_serialize_text}

def register_namespace(prefix, uri):
    """Register a namespace prefix.

    The registry is global, and any existing mapping for either the
    given prefix or the namespace URI will be removed.

    *prefix* is the namespace prefix, *uri* is a namespace uri. Tags and
    attributes in this namespace will be serialized with prefix if possible.

    ValueError is raised if prefix is reserved or is invalid.

    """
    if re.match('ns\\d+$', prefix):
        raise ValueError('Prefix format reserved for internal use')
    for k, v in list(_namespace_map.items()):
        if k == uri or v == prefix:
            del _namespace_map[k]

    _namespace_map[uri] = prefix


_namespace_map = {'http://www.w3.org/XML/1998/namespace':'xml', 
 'http://www.w3.org/1999/xhtml':'html', 
 'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf', 
 'http://schemas.xmlsoap.org/wsdl/':'wsdl', 
 'http://www.w3.org/2001/XMLSchema':'xs', 
 'http://www.w3.org/2001/XMLSchema-instance':'xsi', 
 'http://purl.org/dc/elements/1.1/':'dc'}
register_namespace._namespace_map = _namespace_map

def _raise_serialization_error(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))


def _escape_cdata(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        else:
            if '<' in text:
                text = text.replace('<', '&lt;')
            if '>' in text:
                text = text.replace('>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def _escape_attrib(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        else:
            if '<' in text:
                text = text.replace('<', '&lt;')
            else:
                if '>' in text:
                    text = text.replace('>', '&gt;')
                else:
                    if '"' in text:
                        text = text.replace('"', '&quot;')
                    if '\r\n' in text:
                        text = text.replace('\r\n', '\n')
                    if '\r' in text:
                        text = text.replace('\r', '\n')
                if '\n' in text:
                    text = text.replace('\n', '&#10;')
            if '\t' in text:
                text = text.replace('\t', '&#09;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def _escape_attrib_html(text):
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        else:
            if '>' in text:
                text = text.replace('>', '&gt;')
            if '"' in text:
                text = text.replace('"', '&quot;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def tostring(element, encoding=None, method=None, *, short_empty_elements=True):
    """Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which can
    be one of "xml" (default), "html", "text" or "c14n".

    Returns an (optionally) encoded string containing the XML data.

    """
    stream = io.StringIO() if encoding == 'unicode' else io.BytesIO()
    ElementTree(element).write(stream, encoding, method=method, short_empty_elements=short_empty_elements)
    return stream.getvalue()


class _ListDataStream(io.BufferedIOBase):
    __doc__ = 'An auxiliary stream accumulating into a list reference.'

    def __init__(self, lst):
        self.lst = lst

    def writable(self):
        return True

    def seekable(self):
        return True

    def write(self, b):
        self.lst.append(b)

    def tell(self):
        return len(self.lst)


def tostringlist(element, encoding=None, method=None, *, short_empty_elements=True):
    lst = []
    stream = _ListDataStream(lst)
    ElementTree(element).write(stream, encoding, method=method, short_empty_elements=short_empty_elements)
    return lst


def dump(elem):
    """Write element tree or element structure to sys.stdout.

    This function should be used for debugging only.

    *elem* is either an ElementTree, or a single Element.  The exact output
    format is implementation dependent.  In this version, it's written as an
    ordinary XML file.

    """
    if not isinstance(elem, ElementTree):
        elem = ElementTree(elem)
    elem.write((sys.stdout), encoding='unicode')
    tail = elem.getroot().tail
    if not tail or tail[(-1)] != '\n':
        sys.stdout.write('\n')


def parse(source, parser=None):
    """Parse XML document into element tree.

    *source* is a filename or file object containing XML data,
    *parser* is an optional parser instance defaulting to XMLParser.

    Return an ElementTree instance.

    """
    tree = ElementTree()
    tree.parse(source, parser)
    return tree


def iterparse(source, events=None, parser=None):
    """Incrementally parse XML document into ElementTree.

    This class also reports what's going on to the user based on the
    *events* it is initialized with.  The supported events are the strings
    "start", "end", "start-ns" and "end-ns" (the "ns" events are used to get
    detailed namespace information).  If *events* is omitted, only
    "end" events are reported.

    *source* is a filename or file object containing XML data, *events* is
    a list of events to report back, *parser* is an optional parser instance.

    Returns an iterator providing (event, elem) pairs.

    """
    pullparser = XMLPullParser(events=events, _parser=parser)

    def iterator():
        try:
            while True:
                yield from pullparser.read_events()
                data = source.read(16384)
                if not data:
                    break
                pullparser.feed(data)

            root = pullparser._close_and_return_root()
            yield from pullparser.read_events()
            it.root = root
        finally:
            if close_source:
                source.close()

        if False:
            yield None

    class IterParseIterator(collections.Iterator):
        __next__ = iterator().__next__

    it = IterParseIterator()
    it.root = None
    del iterator
    del IterParseIterator
    close_source = False
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
        close_source = True
    return it


class XMLPullParser:

    def __init__(self, events=None, *, _parser=None):
        self._events_queue = collections.deque()
        self._parser = _parser or XMLParser(target=(TreeBuilder()))
        if events is None:
            events = ('end', )
        self._parser._setevents(self._events_queue, events)

    def feed(self, data):
        """Feed encoded data to parser."""
        if self._parser is None:
            raise ValueError('feed() called after end of stream')
        if data:
            try:
                self._parser.feed(data)
            except SyntaxError as exc:
                self._events_queue.append(exc)

    def _close_and_return_root(self):
        root = self._parser.close()
        self._parser = None
        return root

    def close(self):
        """Finish feeding data to parser.

        Unlike XMLParser, does not return the root element. Use
        read_events() to consume elements from XMLPullParser.
        """
        self._close_and_return_root()

    def read_events(self):
        """Return an iterator over currently available (event, elem) pairs.

        Events are consumed from the internal event queue as they are
        retrieved from the iterator.
        """
        events = self._events_queue
        while events:
            event = events.popleft()
            if isinstance(event, Exception):
                raise event
            else:
                yield event


def XML(text, parser=None):
    """Parse XML document from string constant.

    This function can be used to embed "XML Literals" in Python code.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
    if not parser:
        parser = XMLParser(target=(TreeBuilder()))
    parser.feed(text)
    return parser.close()


def XMLID(text, parser=None):
    """Parse XML document from string constant for its IDs.

    *text* is a string containing XML data, *parser* is an
    optional parser instance, defaulting to the standard XMLParser.

    Returns an (Element, dict) tuple, in which the
    dict maps element id:s to elements.

    """
    if not parser:
        parser = XMLParser(target=(TreeBuilder()))
    parser.feed(text)
    tree = parser.close()
    ids = {}
    for elem in tree.iter():
        id = elem.get('id')
        if id:
            ids[id] = elem

    return (
     tree, ids)


fromstring = XML

def fromstringlist(sequence, parser=None):
    """Parse XML document from sequence of string fragments.

    *sequence* is a list of other sequence, *parser* is an optional parser
    instance, defaulting to the standard XMLParser.

    Returns an Element instance.

    """
    if not parser:
        parser = XMLParser(target=(TreeBuilder()))
    for text in sequence:
        parser.feed(text)

    return parser.close()


class TreeBuilder:
    __doc__ = 'Generic element structure builder.\n\n    This builder converts a sequence of start, data, and end method\n    calls to a well-formed element structure.\n\n    You can use this class to build an element structure using a custom XML\n    parser, or a parser for some other XML-like format.\n\n    *element_factory* is an optional element factory which is called\n    to create new Element instances, as necessary.\n\n    '

    def __init__(self, element_factory=None):
        self._data = []
        self._elem = []
        self._last = None
        self._tail = None
        if element_factory is None:
            element_factory = Element
        self._factory = element_factory

    def close(self):
        """Flush builder buffers and return toplevel document Element."""
        if not len(self._elem) == 0:
            raise AssertionError('missing end tags')
        elif not self._last is not None:
            raise AssertionError('missing toplevel element')
        return self._last

    def _flush(self):
        if self._data:
            if self._last is not None:
                text = ''.join(self._data)
                if self._tail:
                    assert self._last.tail is None, 'internal error (tail)'
                    self._last.tail = text
                else:
                    assert self._last.text is None, 'internal error (text)'
                    self._last.text = text
            self._data = []

    def data(self, data):
        """Add text to current element."""
        self._data.append(data)

    def start(self, tag, attrs):
        """Open new element and return it.

        *tag* is the element name, *attrs* is a dict containing element
        attributes.

        """
        self._flush()
        self._last = elem = self._factory(tag, attrs)
        if self._elem:
            self._elem[(-1)].append(elem)
        self._elem.append(elem)
        self._tail = 0
        return elem

    def end(self, tag):
        """Close and return current Element.

        *tag* is the element name.

        """
        self._flush()
        self._last = self._elem.pop()
        assert self._last.tag == tag, 'end tag mismatch (expected %s, got %s)' % (
         self._last.tag, tag)
        self._tail = 1
        return self._last


class XMLParser:
    __doc__ = 'Element structure builder for XML source data based on the expat parser.\n\n    *html* are predefined HTML entities (deprecated and not supported),\n    *target* is an optional target object which defaults to an instance of the\n    standard TreeBuilder class, *encoding* is an optional encoding string\n    which if given, overrides the encoding specified in the XML file:\n    http://www.iana.org/assignments/character-sets\n\n    '

    def __init__(self, html=0, target=None, encoding=None):
        try:
            from xml.parsers import expat
        except ImportError:
            try:
                import pyexpat as expat
            except ImportError:
                raise ImportError('No module named expat; use SimpleXMLTreeBuilder instead')

        parser = expat.ParserCreate(encoding, '}')
        if target is None:
            target = TreeBuilder()
        self.parser = self._parser = parser
        self.target = self._target = target
        self._error = expat.error
        self._names = {}
        parser.DefaultHandlerExpand = self._default
        if hasattr(target, 'start'):
            parser.StartElementHandler = self._start
        if hasattr(target, 'end'):
            parser.EndElementHandler = self._end
        if hasattr(target, 'data'):
            parser.CharacterDataHandler = target.data
        if hasattr(target, 'comment'):
            parser.CommentHandler = target.comment
        if hasattr(target, 'pi'):
            parser.ProcessingInstructionHandler = target.pi
        parser.buffer_text = 1
        parser.ordered_attributes = 1
        parser.specified_attributes = 1
        self._doctype = None
        self.entity = {}
        try:
            self.version = 'Expat %d.%d.%d' % expat.version_info
        except AttributeError:
            pass

    def _setevents(self, events_queue, events_to_report):
        parser = self._parser
        append = events_queue.append
        for event_name in events_to_report:
            if event_name == 'start':
                parser.ordered_attributes = 1
                parser.specified_attributes = 1

                def handler(tag, attrib_in, event=event_name, append=append, start=self._start):
                    append((event, start(tag, attrib_in)))

                parser.StartElementHandler = handler
            elif event_name == 'end':

                def handler(tag, event=event_name, append=append, end=self._end):
                    append((event, end(tag)))

                parser.EndElementHandler = handler
            else:
                if event_name == 'start-ns':

                    def handler(prefix, uri, event=event_name, append=append):
                        append((event, (prefix or '', uri or '')))

                    parser.StartNamespaceDeclHandler = handler
                else:
                    if event_name == 'end-ns':

                        def handler(prefix, event=event_name, append=append):
                            append((event, None))

                        parser.EndNamespaceDeclHandler = handler
                    else:
                        raise ValueError('unknown event %r' % event_name)

    def _raiseerror(self, value):
        err = ParseError(value)
        err.code = value.code
        err.position = (value.lineno, value.offset)
        raise err

    def _fixname(self, key):
        try:
            name = self._names[key]
        except KeyError:
            name = key
            if '}' in name:
                name = '{' + name
            self._names[key] = name

        return name

    def _start(self, tag, attr_list):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        if attr_list:
            for i in range(0, len(attr_list), 2):
                attrib[fixname(attr_list[i])] = attr_list[(i + 1)]

        return self.target.start(tag, attrib)

    def _end(self, tag):
        return self.target.end(self._fixname(tag))

    def _default(self, text):
        prefix = text[:1]
        if prefix == '&':
            try:
                data_handler = self.target.data
            except AttributeError:
                return
            else:
                try:
                    data_handler(self.entity[text[1:-1]])
                except KeyError:
                    from xml.parsers import expat
                    err = expat.error('undefined entity %s: line %d, column %d' % (
                     text, self.parser.ErrorLineNumber,
                     self.parser.ErrorColumnNumber))
                    err.code = 11
                    err.lineno = self.parser.ErrorLineNumber
                    err.offset = self.parser.ErrorColumnNumber
                    raise err

        if prefix == '<' and text[:9] == '<!DOCTYPE':
            self._doctype = []
        elif self._doctype is not None:
            if prefix == '>':
                self._doctype = None
                return
            text = text.strip()
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == 'PUBLIC' and n == 4:
                    name, type, pubid, system = self._doctype
                    if pubid:
                        pubid = pubid[1:-1]
                else:
                    if type == 'SYSTEM' and n == 3:
                        name, type, system = self._doctype
                        pubid = None
            else:
                return
            if hasattr(self.target, 'doctype'):
                self.target.doctype(name, pubid, system[1:-1])
            else:
                if self.doctype != self._XMLParser__doctype:
                    self._XMLParser__doctype(name, pubid, system[1:-1])
                    self.doctype(name, pubid, system[1:-1])
                self._doctype = None

    def doctype(self, name, pubid, system):
        """(Deprecated)  Handle doctype declaration

        *name* is the Doctype name, *pubid* is the public identifier,
        and *system* is the system identifier.

        """
        warnings.warn('This method of XMLParser is deprecated.  Define doctype() method on the TreeBuilder target.', DeprecationWarning)

    _XMLParser__doctype = doctype

    def feed(self, data):
        """Feed encoded data to parser."""
        try:
            self.parser.Parse(data, 0)
        except self._error as v:
            self._raiseerror(v)

    def close(self):
        """Finish feeding data to parser and return element structure."""
        try:
            self.parser.Parse('', 1)
        except self._error as v:
            self._raiseerror(v)

        try:
            try:
                close_handler = self.target.close
            except AttributeError:
                pass
            else:
                return close_handler()
        finally:
            del self.parser
            del self._parser
            del self.target
            del self._target


try:
    _Element_Py = Element
    from _elementtree import *
except ImportError:
    pass