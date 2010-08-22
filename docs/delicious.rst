DeliciousTokenizer
===================

.. currentmodule:: tagtools
.. moduleauthor:: Gustavo Picon <tabo@tabo.pe>

.. inheritance-diagram:: DeliciousTokenizer
.. autoclass:: DeliciousTokenizer
   :show-inheritance:

    Example::

        DeliciousTokenizer.str2tags('Tag1 Tag2 TAG1 Tag3')

    returns::

        [('tag1', 'Tag1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        DeliciousTokenizer.tags2str(['tag1', 'tag2', 'tag3'])

    returns::

        'tag1 tag2 tag3'
