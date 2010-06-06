
__version__ = '0.8c'


class Serializer(object):
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
    """ Serializer for Delicious-like tags.

    Delicious tags are separated by spaces, and don't allow spaces in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.
    """
    SEPARATOR = JOINER = ' '
    TAGS_WITH_SPACES = False


class CommaSerializer(Serializer):
    """ Serializer for comma-separated tags.

    Comma separated tags don't allow commas in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.
    """
    SEPARATOR = ','
    JOINER = ', '
    TAGS_WITH_SPACES = True


class FlickrSerializer(Serializer):
    """ Serializer for Flickr-like tags.

    Flickr tags are separated by spaces. If a tag has spaces, it must be
    enclosed with double quotes.

    Tags are normalized as lowercase by default to avoid tag duplication.
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
