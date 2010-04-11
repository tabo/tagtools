""" tagtools
"""


class Serializer(object):
    """ TODO: docstring
    """
    SEPARATOR = JOINER = TAGS_WITH_SPACES = None

    @classmethod
    def str2tags(cls, tagstr):
        """ TODO: docstring
        """
        if not tagstr:
            return []
        tags, keys = [], set()
        for tag in tagstr.split(cls.SEPARATOR):
            tag = tag.strip()
            cleantag = cls.normalize(tag)
            if not cleantag or cleantag in keys:
                # Ignore if the normalized tag is empty or if there is
                # already tag with the same normalized value.
                # TaG, TAG, tag, taG ==> TaG
                continue
            tags.append((cleantag, tag))
            keys.add(cleantag)
        return tags

    @classmethod
    def tags2str(cls, tags):
        """ TODO: docstring
        """
        if cls.TAGS_WITH_SPACES:
            return cls.JOINER.join(tags)
        results = []
        for tag in tags:
            if ' ' in tag:
                raise TagWithSpaceException(
                    "Tag can't have a space: '%s'" % tag)
            results.append(tag)
        return cls.JOINER.join(results)

    @staticmethod
    def normalize(tag):
        """ TODO: docstring
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


class TagWithSpaceException(Exception):
    """ TODO: docstring
    """
    pass
