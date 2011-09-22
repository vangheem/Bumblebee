from lxml.html import fromstring
from bumblebee.rules import Before
from bumblebee.rules import After
from bumblebee.rules import Drop
from bumblebee.rules import Replace
from bumblebee.rules import Class
from bumblebee.rules import Group
from bumblebee.rules import Tag
from bumblebee.conditions import IfContent
from bumblebee.conditions import Not
from bumblebee.selectors import CSS, XPath, NodeHTML
from bumblebee.exceptions import XMLUnknownTag
from bumblebee.exceptions import XMLUnknownCondition
from bumblebee.exceptions import XMLUnknownSelector


_tags = {
    'before': Before,
    'after': After,
    'drop': Drop,
    'replace': Replace,
    'class': Class,
    'group': Group,
    'tag': Tag
}


def addTag(name, klass):
    _tags[name] = klass

_conditions = {
    'content': IfContent
}


def addCondition(name, klass):
    _conditions[name] = klass

_selector_attributes = ['src', 'dst', 'content']


def addSelectorAttributeName(name):
    _selector_attributes.append(name)

_selectors = {
    'css': CSS,
    'xpath': XPath,
    'html': NodeHTML
}


def addSelector(name, klass):
    _selectors[name] = klass


def getSelector(name, value, node):
    if '-' not in name:
        return CSS(value, node)
    name, selector = name.split('-')
    if selector in _selectors:
        return _selectors[selector](value, node)
    else:
        raise XMLUnknownSelector("%s is unknown." % selector)


def _removeall(val, *args):
    for arg in args:
        val = val.replace(arg, '')
    return val


def getRuleFromNode(node):
    if node.tag not in _tags:
        raise XMLUnknownTag("%s is unknown." % node.tag)
    rule_class = _tags[node.tag]

    kwargs = {'conditions': []}
    for name, value in node.attrib.items():
        stripped_name = _removeall(name, 'if-', 'not-', \
                            *['-' + s for s in _selectors])
        if name.startswith('if-'):
            if stripped_name not in _conditions:
                raise XMLUnknownCondition("%s is unknown." % name)
            cond_klass = _conditions[stripped_name]
            cond = cond_klass(value)
            if name.startswith('if-not-'):
                cond = Not(cond)
            kwargs['conditions'].append(cond)
        elif stripped_name in _selector_attributes:
            kwargs[stripped_name] = getSelector(name, value, node)
        else:
            kwargs[name] = value
    if node.tag == 'group':
        rules = []
        for child in node.getchildren():
            rule = getRuleFromNode(child)
            if rule:
                rules.append(rule)
        kwargs['rules'] = rules
    return rule_class(**kwargs)


def convertRules(xml, raise_errors=False):
    root = fromstring(xml)
    rules = []
    for node in root.getchildren():
        try:
            rule = getRuleFromNode(node)
            if rule:
                rules.append(rule)
        except:
            if raise_errors:
                raise
    return rules
