import unicodedata

class Serializer(object):
    SEPARATOR = JOINER = TAGS_WITH_SPACES = None

    @classmethod
    def str2tags(cls, tagstr):
        if not tagstr:
            return []
        return [
            tag.strip()
            for tag in tagstr.split(cls.SEPARATOR)
            if tag.strip()
        ]

    @classmethod
    def tags2str(cls, tags):
        if cls.TAGS_WITH_SPACES:
            return cls.JOINER.join(tags)
        results = []
        for tag in tags:
            if ' ' in tag:
                raise TagWithSpaceException(
                    "Tag can't have a space: '%s'" % tag)
            results.append(tag)
        return cls.JOINER.join(results)


class DeliciousSerializer(Serializer):
    SEPARATOR = JOINER = ' '
    TAGS_WITH_SPACES = False


class CommaSerializer(Serializer):
    SEPARATOR = ','
    JOINER = ', '
    TAGS_WITH_SPACES = True


class FlickrSerializer(Serializer):

    @classmethod
    def str2tags(cls, tagstr):
        if not tagstr:
            return []
        if '"' not in tagstr:
            return [tag.strip() for tag in tagstr.split(' ') if tag.strip()]
        lstr = list(tagstr.strip())
        results, tok, prev, quoted = [], '', '', False
        while lstr:
            char = lstr[0]
            if char == '"':
                quoted = not quoted
            elif char == ' ' and \
                    (not quoted or \
                    (quoted and prev == '"' and '"' not in lstr)):
                if tok:
                    quoted = False
                    results.append(tok.strip())
                    tok = ''
            else:
                tok += char
            prev = char
            del lstr[0]
        tok = tok.strip()
        if tok:
            results.append(tok)
        return results

    @classmethod
    def tags2str(cls, tags):
        return ' '.join([
            '"%s"' % tag if ' ' in tag else tag
            for tag in tags])


def normalize(tags):
    results = {}
    for tag in tags:
        cleantag = unicodedata.tag.strip().lower()
        results[tag] = cleantag
    return results




class TagWithSpaceException(Exception):
    pass
