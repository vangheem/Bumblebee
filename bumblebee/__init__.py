
from repoze.xmliter.utils import getHTMLSerializer


def transform(doc, rules, extras={}, throw_errors=False):
    if isinstance(doc, basestring):
        doc = getHTMLSerializer([doc])

    root = doc.tree.getroot()

    for rule in rules:
        try:
            rule(root, extras)
        except:
            if throw_errors:
                raise

    return doc
