from lxml.etree import fromstring

from bumblebee.rules import Before
from bumblebee.rules import After
from bumblebee.rules import Drop
from bumblebee.rules import Replace
from bumblebee.rules import Class
from bumblebee.rules import Group
from bumblebee.conditions import IfContent
from bumblebee.conditions import Not
from bumblebee.selectors import CSS, XPath

_tags = {
    'before': Before,
    'after': After,
    'drop': Drop,
    'replace': Replace,
    'class': Class,
    'group': Group
}


def addTag(name, klass):
    _tags[name] = klass

_conditions = {
    'content': IfContent
}


def addCondition(name, klass):
    _conditions[name] = klass

_selector_attributes = ['src', 'dst', 'content']


def getSelector(name, value):
    if name.endswith(':xpath'):
        return XPath(value)
    else:
        return CSS(value)


def _removeall(val, *args):
    for arg in args:
        val = val.replace(arg, '')
    return val


def getRuleFromNode(node, extras):
    if node.tag not in _tags:
        raise Exception("Unknown tag")
    rule_class = _tags[node.tag]

    kwargs = {'conditions': [], 'extras': extras}
    for name, value in node.attrib.items():
        stripped_name = _removeall(name, 'if-', ':xpath', 'not-')
        if name.startswith('if-'):
            if stripped_name not in _conditions:
                raise Exception("Unknown Condition")
            cond_klass = _conditions[stripped_name]
            cond = cond_klass(value, extras)
            if name.startswith('if-not-'):
                cond = Not(cond)
            kwargs['conditions'].append(cond)
        elif stripped_name in _selector_attributes:
            kwargs[stripped_name] = getSelector(name, value)
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


def convertRules(xml, extras={}):
    root = fromstring(xml)

    rules = []
    for node in root.getchildren():
        try:
            rule = getRuleFromNode(node, extras)
            if rule:
                rules.append(rule)
        except:
            pass
    return rules
