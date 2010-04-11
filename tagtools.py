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

"""


__version__ = '0.8a'


class Serializer(object):
    """ Provides methods to subclass tagging serializers.

    Must not be used directly, use a subclass instead.

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
        """
        return tag.lower()


class DeliciousSerializer(Serializer):
    """ TODO: docstring
    """
    SEPARATOR = JOINER = ' '
    TAGS_WITH_SPACES = False


class CommaSerializer(Serializer):
    """ TODO: docstring
    """
    SEPARATOR = ','
    JOINER = ', '
    TAGS_WITH_SPACES = True


class FlickrSerializer(Serializer):
    """ TODO: docstring
    """
    SEPARATOR = ' '

    @classmethod
    def str2tags(cls, tagstr):
        """ TODO: docstring
        """
        if not tagstr:
            return []
        if '"' not in tagstr:
            return super(FlickrSerializer, cls).str2tags(tagstr)
        lstr = list(tagstr.strip())
        tags, keys, tok, prev, quoted = [], set(), '', '', False

        def addtok(tok):
            """ TODO: docstring
            """
            tok = tok.strip()
            cleantok = cls.normalize(tok)
            if cleantok and cleantok not in keys:
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
        """ TODO: docstring
        """
        return ' '.join([
            # no X if Y else Z in python<=2.4
            {True: '"%s"', False: '%s'}[' ' in tag] % tag
            for tag in tags])


class TagWithSeparatorException(Exception):
    """ TODO: docstring
    """
    pass
