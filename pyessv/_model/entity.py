# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.node.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A node within the pyessv domain model.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import arrow

from pyessv._constants import NODE_TYPE_AUTHORITY
from pyessv._constants import NODE_TYPE_COLLECTION
from pyessv._constants import NODE_TYPE_SCOPE
from pyessv._constants import NODE_TYPE_TERM
from pyessv._utils.compat import basestring



class Node(object):
    """A node within the pyessv domain model.

    """
    def __init__(self, typekey):
        """Instance constructor.

        """
        self.create_date = None
        self.data = None
        self.description = None
        self.label = None
        self.name = None
        self.typekey = typekey
        self.uid = None
        self.url = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def validate(self):
        """Validates instance.

        :returns: Set of validation errrors.
        :rtype: set

        """
        # N.B. just-in-time import to avoid circular references.
        from pyessv._validation import validate_node

        return validate_node(self)


    @property
    def errors(self):
        """Returns set of validation errors.

        """
        return sorted(list(self.validate()))


    @property
    def is_valid(self):
        """Gets flag indicating validity.

        """
        return len(self.validate()) == 0


    @property
    def io_name(self):
        """Returns name formatted for I/O operations.

        """
        io_name = self.name.strip().lower()
        io_name = io_name.replace("_", "-")
        io_name = io_name.replace(" ", "-")

        return io_name


    @staticmethod
    def get_item(node, key):
        """Returns an item from managed collection.

        """
        # Set collection.
        if node.typekey == NODE_TYPE_AUTHORITY:
            items = node.scopes
        elif node.typekey == NODE_TYPE_COLLECTION:
            items = node.terms
        elif node.typekey == NODE_TYPE_SCOPE:
            items = node.collections

        # Set comparator to be used.
        if isinstance(key, int):
            comparator = lambda i: i.idx
        elif isinstance(key, uuid.UUID):
            comparator = lambda i: i.uid
        else:
            key = str(key).strip().lower()
            try:
                uuid.UUID(key)
            except ValueError:
                comparator = lambda i: i.name
            else:
                comparator = lambda i: str(i.uid)

        # Match against a attribute.
        for item in items:
            if comparator(item) == key:
                return item

        # Match against a synonym.
        try:
            items = [i for i in items if i.synonyms]
        except AttributeError:
            pass
        else:
            for item in items:
                if key in item.synonyms:
                    return item
