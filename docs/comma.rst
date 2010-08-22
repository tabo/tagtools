CommaTokenizer
===============

.. currentmodule:: tagtools
.. moduleauthor:: Gustavo Picon <tabo@tabo.pe>

.. inheritance-diagram:: CommaTokenizer
.. autoclass:: CommaTokenizer
   :show-inheritance:

    Example::

        CommaTokenizer.str2tags('Tag 1, Tag2, TAG 1, Tag3')

    returns::

        [('tag 1', 'Tag 1'), ('tag2', 'Tag2'), ('tag3', 'Tag3')]

    and::

        CommaTokenizer.tags2str(['tag1', 'tag2', 'tag3'])

    returns::

        'tag1, tag2, tag3'
