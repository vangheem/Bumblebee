

class BaseIf(object):
    pass


class IfContent(BaseIf):

    def __init__(self, selector):
        self.selector = selector

    def __call__(self, root, extras={}):
        return len(self.selector(root)) > 0


class Not(object):

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, root, extras={}):
        return not self.condition(root, extras)
