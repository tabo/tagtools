FlickrTokenizer
================

.. currentmodule:: tagtools
.. moduleauthor:: Gustavo Picon <tabo@tabo.pe>

.. inheritance-diagram:: FlickrTokenizer
.. autoclass:: FlickrTokenizer
   :show-inheritance:

    Example::

        FlickrTokenizer.str2tags('"Tag 1" Tag2 "TAG 1" Tag3')

    returns::

        [('tag 1', 'Tag 1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        FlickrTokenizer.tags2str(['tag 1', 'tag2', 'tag3'])

    returns::

        '"tag 1" tag2 tag3'

    .. note::

        Flickr tags are very... peculiar.  The test suite has lot of weird
        cases and they all work exactly like Flickr. Please let me know if
        there is a corner case I'm not covering.
