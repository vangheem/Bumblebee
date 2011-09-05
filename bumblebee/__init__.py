
from repoze.xmliter.utils import getHTMLSerializer


def transform(doc, rules):
    if isinstance(doc, basestring):
        doc = getHTMLSerializer([doc])

    root = doc.tree.getroot()

    for rule in rules:
        rule(root)

    return doc
