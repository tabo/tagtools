"""

tagtools
--------

:synopsys: Python helpers to work with tags.
:copyright: 2010 by Gustavo Picon
:license: Apache License 2.0
:version: 0.8a
:url: http://code.tabo.pe/tagtools/
:documentation:
   `tagtools-docs
   <http://docs.tabo.pe/tagtools/tip/>`_
:examples:
   `tagtools-tests
   <http://code.tabo.pe/tagtools/src/tip/tests.py>`_

Python library that parses raw strings with tags into a list of tags and
viceversa.

Includes the tag parsing methods used in Flickr (:class:`FlickrSerializer`),
Delicious (:class:`DeliciousSerializer`) and tag separation with commas
(:class:`CommaSerializer`).

Handles customizable per-tag normalization to avoid tag duplicates.

"""


__version__ = '0.8a'


class Serializer(object):
    """ Provides methods to subclass tagging serializers.

    Must not be used directly, use a subclass (:class:`FlickrSerializer`,
    :class:`DeliciousSerializer` or :class:`CommaSerializer`) instead.

    The subclasses are not designed to be instantiated, they contains only
    class and static methods.
    """
    SEPARATOR = JOINER = TAGS_WITH_SPACES = None

    @classmethod
    def str2tags(cls, tagstr):
        """ Takes a raw string with tags and returns a list of parsed tags.

        :param tagstr: A string with tags as entered by a user on a form.

        :returns: A list of tuples. Each tuple represents a tag and has
                  two elements:

                  - The normalized tag. Normalization is done by the
                    :meth:`normalize` static method.
                  - The raw tag as was entered, but without leading/trailing
                    whitespace.

        .. note::

            If more than one tag have the same normalized form, only the first
            tag will be included in the resulting list. So for instance, if
            using the :class:`CommaSerializer` subclass::

                CommaSerializer.str2tags("TaG, tag, TAG")

            would return::

                [('tag', 'TaG')]

        """
        if not tagstr:
            return []
        tags, keys = [], set()
        for tag in tagstr.split(cls.SEPARATOR):
            tag = tag.strip()
            cleantag = cls.normalize(tag)
            if not cleantag or cleantag in keys:
                # Ignore if the normalized tag is empty or if there is
                # already a tag with the same normalized value.
                # TaG, TAG, tag, taG ==> TaG
                continue
            tags.append((cleantag, tag))
            keys.add(cleantag)
        return tags

    @classmethod
    def tags2str(cls, tags):
        """ Takes a list of tags and returns a string that can be edited.

        :param tags: A list of tags that are correct for the Serializer being
                     used. For instance, when using :class:`CommaSerializer`,
                     tags can't have commas on them.

        :returns: A string that, if serialized, would return the same tags.

        :raise TagWithSeparatorException:

          * if a tag has a space when using :class:`DeliciousSerializer`, or
          * a tag has a comma when using :class:`CommaSerializer`

        .. note::

            The use case for this method is when a program needs to
            provide a user interface for the user to edit the tags, and
            the user interface is a single input entry.

        """
        results = []
        for tag in tags:
            if cls.SEPARATOR in tag:
                raise TagWithSeparatorException(
                    "Tag can't include the separator: '%s'" % tag)
            results.append(tag)
        return cls.JOINER.join(results)

    @staticmethod
    def normalize(tag):
        """ Normalizes a single tag. Called by :meth:`str2tags`

        :param tag: A single tag, as a string. It is assumed that the tag has
                    no leading/trailing whitespace.

        :returns: A normalized version of the tag.

        .. note::

            By default, all Serializers will call `.lower()` on the
            given `tag`. You can change this behavior either by
            further subclassing or composition, like::

                class MySerializer(CommaSerializer):

                    @staticmethod
                    def normalize(tag):
                        return tag.upper()
        """
        return tag.lower()


class DeliciousSerializer(Serializer):
    """ Serializer for Delicious-like tags.

    Delicious tags are separated by spaces, and don't allow spaces in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.

    Example::

        DeliciousSerializer.str2tags('Tag1 Tag2 TAG1 Tag3')

    returns::

        [('tag1', 'Tag1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        DeliciousSerializer.tags2str(['tag1', 'tag2', 'tag3'])

    returns::

        'tag1 tag2 tag3'
    """
    SEPARATOR = JOINER = ' '
    TAGS_WITH_SPACES = False


class CommaSerializer(Serializer):
    """ Serializer for comma-separated tags.

    Comma separated tags don't allow commas in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.

    Example::

        CommaSerializer.str2tags('Tag 1, Tag2, TAG 1, Tag3')

    returns::

        [('tag 1', 'Tag 1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        CommaSerializer.tags2str(['tag1', 'tag2', 'tag3'])

    returns::

        'tag1, tag2, tag3'
    """
    SEPARATOR = ','
    JOINER = ', '
    TAGS_WITH_SPACES = True


class FlickrSerializer(Serializer):
    """ Serializer for Flickr-like tags.

    Flickr tags are separated by spaces. If a tag has spaces, it must be
    enclosed with double quotes.

    Tags are normalized as lowercase by default to avoid tag duplication.

    Example::

        FlickrSerializer.str2tags('"Tag 1" Tag2 "TAG 1" Tag3')

    returns::

        [('tag 1', 'Tag 1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        FlickrSerializer.tags2str(['tag 1', 'tag2', 'tag3'])

    returns::

        '"tag 1" tag2 tag3'

    .. note::

        Flickr tags are very... peculiar.  The test suite has lot of weird
        cases and they all work exactly like Flickr. Please let me know if
        there is a corner case I'm not covering.
    """
    SEPARATOR = ' '

    @classmethod
    def str2tags(cls, tagstr):
        "Parser for the incredibly weird flickr tags (see tests)."
        if not tagstr:
            return []
        if '"' not in tagstr:
            return super(FlickrSerializer, cls).str2tags(tagstr)
        lstr = list(tagstr.strip())
        tags, keys, tok, prev, quoted = [], set(), '', '', False

        def addtok(tok):
            "adds a valid token (tag) to both the tags list and the keys set"
            tok = tok.strip()
            cleantok = cls.normalize(tok)
            if cleantok and cleantok not in keys:
                # don't add the tag if it's invalid (empty) or if the
                # normalized value is already in the keys set
                tags.append((cleantok, tok))
                keys.add(cleantok)

        while lstr:
            char = lstr[0]
            if char == '"':
                quoted = not quoted
            elif char == ' ' and \
                    (not quoted or \
                    (quoted and prev == '"' and '"' not in lstr)):
                if tok:
                    quoted = False
                    addtok(tok)
                    tok = ''
            else:
                tok += char
            prev = char
            del lstr[0]
        tok = tok.strip()
        if tok:
            addtok(tok)
        return tags

    @classmethod
    def tags2str(cls, tags):
        'Returns a string of tags. If a tag has spaces, enclose it with "s'
        return ' '.join([
            # no X if Y else Z in python<=2.4
            {True: '"%s"', False: '%s'}[' ' in tag] % tag
            for tag in tags])


class TagWithSeparatorException(Exception):
    "Raised when a tag includes the separator used by the serializer."
