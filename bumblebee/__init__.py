
from repoze.xmliter.utils import getHTMLSerializer


def transform(doc, rules, extras={}):
    if isinstance(doc, basestring):
        doc = getHTMLSerializer([doc])

    root = doc.tree.getroot()

    for rule in rules:
        rule(root, extras)

    return doc
