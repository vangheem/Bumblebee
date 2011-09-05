

class BaseIf(object):

    def __init__(self, extras={}):
        self.extras = extras


class IfContent(BaseIf):

    def __init__(self, selector, extras={}):
        super(IfContent, self).__init__(extras)
        self.selector = selector

    def __call__(self, root):
        return len(self.selector(root)) > 0


class Not(object):

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, root):
        return not self.condition(root)
