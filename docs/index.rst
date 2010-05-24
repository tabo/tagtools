tagtools
========

`tagtools <https://tabo.pe/projects/tagtools/>`_ is a python library that
parses raw strings with tags into a list of tags and viceversa, written by
`Gustavo Picón <https://tabo.pe>`_ and licensed under the Apache License 2.0.

``tagtools`` is:

- **Flexible**: Includes 3 different tag implementations with the same API:

  1. Flickr (:class:`FlickrSerializer`)
  2. Delicious (:class:`DeliciousSerializer`)
  3. Comma separated tags (:class:`CommaSerializer`)

- **Customizable**: Handles customizable per-tag normalization to avoid
  tag duplicates.
- **Easy**: Simple :doc:`API <api>`
- **Clean**: Testable and well tested code base. 100% code/branch test
  coverage.


Contents
--------

.. toctree::
   :maxdepth: 2

   api
   flickr
   delicious
   comma


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

