

class Base(object):

    def __init__(self, node=None):
        pass


class CSS(Base):
    """
    Selector for css
    """

    def __init__(self, selector, _=None):
        self.selector = selector

    def __call__(self, node, extras={}):
        return node.cssselect(self.selector)


class XPath(Base):
    """
    """

    def __init__(self, xpath, _=None):
        self.xpath = xpath

    def __call__(self, node, extras={}):
        return node.xpath(self.xpath)


class NodeHTML(Base):

    def __init__(self, value, node):
        self.html_nodes = node.getchildren()

    def __call__(self, node, extras={}):
        return self.html_nodes
