API
===

.. module:: tagtools
.. moduleauthor:: Gustavo Picon <tabo@tabo.pe>

.. inheritance-diagram:: Serializer
.. autoclass:: Serializer
   :show-inheritance:

   Provides methods to subclass tagging serializers.

   Must not be used directly, use a subclass (:class:`FlickrSerializer`,
   :class:`DeliciousSerializer` or :class:`CommaSerializer`) instead.

   The subclasses are not designed to be instantiated, they contains only
   class and static methods.

   .. automethod:: str2tags

        .. note::

            If more than one tag have the same normalized form, only the first
            tag will be included in the resulting list. So for instance, if
            using the :class:`CommaSerializer` subclass::

                CommaSerializer.str2tags("TaG, tag, TAG")

            would return::

                [('tag', 'TaG')]

   .. automethod:: tags2str

        .. note::

            The use case for this method is when a program needs to
            provide a user interface for the user to edit the tags, and
            the user interface is a single input entry.

   .. automethod:: normalize

        .. note::

            By default, all Serializers will call `.lower()` on the
            given `tag`. You can change this behavior either by
            further subclassing or composition, like::

                class MySerializer(CommaSerializer):

                    @staticmethod
                    def normalize(tag):
                        return tag.upper()
