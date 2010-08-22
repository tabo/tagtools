import re

__version__ = '0.8d'

RE_MACHINE_TAG = re.compile(r"""
                            ^                   # begin
                            ([a-z][a-z0-9_]*)   # namespace
                            \:                  # separator
                            ([a-z][a-z0-9_]*)   # predicate
                            \=                  # separator
                            (.+)                # value
                            $                   # the end """, re.VERBOSE)


class Tag:
    "Tag objects"

    def __init__(self, raw_tag):
        self.raw = raw_tag.strip()
        self.is_machinetag = False
        self.namespace, self.predicate, self.value = None, None, None
        self.parse()

    def parse(self):
        self.clean = self.normalize(self.raw)

        if ':' in self.raw and '=' in self.raw:
            mmatch = RE_MACHINE_TAG.match(self.raw)
            if mmatch:
                self.is_machinetag = True
                self.namespace, self.predicate, value = mmatch.groups()
                self.value = self.normalize(value)

    @staticmethod
    def normalize(tag):
        """ Normalizes a single tag.

        :param tag: A single tag, as a string. It is assumed that the tag has
                    no leading/trailing whitespace.

        :returns: A normalized version of the tag.
        """
        return tag.lower()


class Tokenizer(object):
    SEPARATOR = JOINER = TAGS_WITH_SPACES = None
    TAGCLASS = Tag

    @classmethod
    def _process_tag(cls, tags, keys, strtag):
        tag = cls.TAGCLASS(strtag)
        cleantag = tag.clean
        if cleantag and cleantag not in keys:
            # Ignore if the normalized tag is empty or if there is
            # already a tag with the same normalized value.
            # TaG, TAG, tag, taG ==> TaG
            tags.append(tag)
            keys.add(cleantag)

    @classmethod
    def str2tags(cls, tagstr):
        """ Takes a raw string with tags and returns a list of parsed tags.

        :param tagstr: A string with tags as entered by a user on a form.

        :returns: A list of Tag objects. If you subclass Tag, set your subclass
                  in the TAGCLASS property.
        """
        if not tagstr:
            return []
        tags, keys = [], set()
        for strtag in tagstr.split(cls.SEPARATOR):
            cls._process_tag(tags, keys, strtag)
        return tags

    @classmethod
    def tags2str(cls, tags):
        """ Takes a list of tags and returns a string that can be edited.

        :param tags: A list of tags that are correct for the Tokenizer being
                     used. For instance, when using :class:`CommaTokenizer`,
                     tags can't have commas on them.

        :returns: A string that, if serialized, would return the same tags.

        :raise TagWithSeparatorException:

          * if a tag has a space when using :class:`DeliciousTokenizer`, or
          * a tag has a comma when using :class:`CommaTokenizer`
        """
        results = []
        for tag in tags:
            if cls.SEPARATOR in tag:
                raise TagWithSeparatorException(
                    "Tag can't include the separator: '%s'" % tag)
            results.append(tag)
        return cls.JOINER.join(results)



class DeliciousTokenizer(Tokenizer):
    """ Tokenizer for Delicious-like tags.

    Delicious tags are separated by spaces, and don't allow spaces in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.
    """
    SEPARATOR = JOINER = ' '
    TAGS_WITH_SPACES = False


class CommaTokenizer(Tokenizer):
    """ Tokenizer for comma-separated tags.

    Comma separated tags don't allow commas in a tag.

    Tags are normalized as lowercase by default to avoid tag duplication.
    """
    SEPARATOR = ','
    JOINER = ', '
    TAGS_WITH_SPACES = True


class FlickrTokenizer(Tokenizer):
    """ Tokenizer for Flickr-like tags.

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
            return super(FlickrTokenizer, cls).str2tags(tagstr)
        lstr = list(tagstr.strip())
        tags, keys, tok, prev, quoted = [], set(), '', '', False

        while lstr:
            char = lstr[0]
            if char == '"':
                quoted = not quoted
            elif char == ' ' and \
                    (not quoted or \
                    (quoted and prev == '"' and '"' not in lstr)):
                if tok:
                    quoted = False
                    cls._process_tag(tags, keys, tok)
                    tok = ''
            else:
                tok += char
            prev = char
            del lstr[0]
        tok = tok.strip()
        if tok:
            cls._process_tag(tags, keys, tok)
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
