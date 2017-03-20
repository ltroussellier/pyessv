# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parser.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of names to match vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_TERM
from pyessv._archive import load
from pyessv._exceptions import ParsingError

_TYPE_BY_IDX = {
    0: ENTITY_TYPE_AUTHORITY,
    1: ENTITY_TYPE_SCOPE,
    2: ENTITY_TYPE_COLLECTION,
    3: ENTITY_TYPE_TERM
}


def parse_namespace(namespace, strict=True):
    namespace = unicode(namespace).split(":")
    if len(namespace) == 0 or len(namespace) > 4:
        raise ValueError("Invalid namespace")

    namespace = namespace + [None for i in range(4 - len(namespace))]

    return parse(namespace[0], namespace[1], namespace[2], namespace[3], strict)


def parse(authority, scope=None, collection=None, term=None, strict=True):
    """Parses a name within a vocabulary hierachy.

    :param str authority: Vocabulary authority, e.g. wcrp.
    :param str scope: Vocabulary scope, e.g. global.
    :param str collection: Vocabulary collection, e.g. institute-id.
    :param str term: Vocabulary term, e.g. ipsl.
    :param bool strict: Flag indicating whether to apply strict lookup rules.

    """
    targets = [
        _EntityInfo(ENTITY_TYPE_AUTHORITY, authority, strict),
        _EntityInfo(ENTITY_TYPE_SCOPE, scope, strict),
        _EntityInfo(ENTITY_TYPE_COLLECTION, collection, strict),
        _EntityInfo(ENTITY_TYPE_TERM, term, strict),
    ]

    for target in [i for i in targets if i.name is not None]:
        entity = load(
            targets[0].get_name(target),
            targets[1].get_name(target),
            targets[2].get_name(target),
            targets[3].get_name(target)
            )
        target.set_entity(entity)

    return target.entity.name


class _EntityInfo(object):
    """Information about an entity whose name is being parsed.

    """
    def __init__(self, typeof, name, strict):
        self.entity = None
        self.name = name
        self.strict = strict
        self.typeof = typeof


    @property
    def formatted_name(self):
        """Gets formatted name used to search archive.

        """
        name = unicode(self.name)
        if not self.strict:
            name = name.strip().lower()

        return name


    def get_name(self, target):
        """Gets parsing relative name.

        """
        if self.entity:
            return self.entity.name
        if target == self:
            return self.formatted_name


    def set_entity(self, entity):
        """Sets entity returned from archive search.

        """
        if entity is None:
            raise ParsingError(self.typeof, self.name)
        if self.strict:
            if entity.name != self.name:
                raise ParsingError(self.typeof, self.name)
        self.entity = entity
