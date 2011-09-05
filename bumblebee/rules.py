

def spacedList(val):
    if not isinstance(val, basestring):
        raise Exception("Expected string to work with.")
    if not val:
        return []
    return val.split(' ')


def notNone(val):
    if not val:
        raise Exception("You must have a value for this.")
    return val


class Base(object):
    def __init__(self, conditions=[], extras={}):
        self.conditions = conditions
        self.extras = extras

    def skip(self, root):
        for condition in self.conditions:
            if condition(root):
                return False
            else:
                return True
        return False


class BaseSingle(Base):

    def __init__(self, src=None, conditions=[], extras={}):
        super(BaseSingle, self).__init__(conditions, extras)
        self.src = notNone(src)

    def process_nodes(self, root):
        if self.skip(root):
            return None, True
        src = self.src(root)

        if not src:
            return src, True
        return src, False


class BaseDouble(BaseSingle):

    def __init__(self, src=None, dst=None, conditions=[], extras={}):
        super(BaseDouble, self).__init__(src, conditions, extras)
        self.dst = notNone(dst)

    def process_nodes(self, root):
        src, skip = super(BaseDouble, self).process_nodes(root)
        dst = self.dst(root)

        if not dst:
            skip = True

        return src, dst, skip


class Before(BaseDouble):
    """
    Move the src node before the dst node
    """

    def __call__(self, root):
        src, dst, skip = self.process_nodes(root)
        if skip:
            return None

        dst = dst[0]
        for el in src:
            dst.addprevious(el)
        return src


class After(BaseDouble):
    """
    Move the src node after the dst node
    """

    def __call__(self, root):
        src, dst, skip = self.process_nodes(root)
        if skip:
            return None
        dst = dst[0]

        for el in src:
            dst.addnext(el)
        return src


class Drop(BaseSingle):
    """
    Drop the src node.
    """

    def __call__(self, root):
        src, skip = self.process_nodes(root)
        if skip:
            return None

        for el in src:
            parent = el.getparent()
            parent.remove(el)
        return src


class Replace(BaseDouble):
    """
    Replace the dst node with the src node.
    """

    def __init__(self, src=None, dst=None, conditions=[],
                              attributes=None, extras={}):
        super(Replace, self).__init__(src, dst, conditions, extras)
        self.attributes = spacedList(attributes)

    def __call__(self, root):
        src, dst, skip = self.process_nodes(root)
        if skip:
            return None

        src = src[0]
        dst = dst[0]

        if self.attributes:
            if 'all' in self.attributes:
                dst.attrib = src.attrib
            else:
                for attribute in self.attributes:
                    dst.attrib[attribute] = src.attrib[attribute]
        else:
            parent = dst.getparent()
            parent.replace(dst, src)

        return src


class Class(BaseSingle):
    def __init__(self, src=None, remove='', add='', conditions=[], extras={}):
        super(Class, self).__init__(src, conditions, extras)
        self.remove = spacedList(remove)
        self.add = spacedList(add)

    def __call__(self, root):
        src, skip = self.process_nodes(root)
        if skip:
            return None
        src = src[0]
        klasses = src.attrib.get('class', '')
        if not klasses:
            klasses = set([])
        else:
            klasses = set(klasses.split(' '))

        for klass in self.remove:
            if klass in klasses:
                klasses.remove(klass)
        for klass in self.add:
            if klass not in klasses:
                klasses.add(klass)
        src.attrib['class'] = ' '.join(klasses)

        return src


class Group(Base):
    def __init__(self, rules=[], conditions=[], extras={}):
        super(Group, self).__init__(conditions=conditions, extras=extras)
        self.rules = rules

    def __call__(self, root):
        if self.skip(root):
            return
        for rule in self.rules:
            rule(root)
