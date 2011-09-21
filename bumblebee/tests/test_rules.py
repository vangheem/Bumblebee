import unittest
from bumblebee.tests import basichtml
from bumblebee.rules import Before
from bumblebee.rules import After
from bumblebee.rules import Drop
from bumblebee.rules import Replace
from bumblebee.rules import Class
from bumblebee.rules import Group
from bumblebee.rules import Tag
from bumblebee.selectors import CSS
from bumblebee.conditions import IfContent
from repoze.xmliter.utils import getHTMLSerializer


class TestRules(unittest.TestCase):

    def get_root(self):
        return getHTMLSerializer([basichtml]).tree.getroot()

    def test_before_rule(self):
        root = self.get_root()
        footer = CSS('#footer')
        content = CSS("#content")
        rule = Before(footer, content)
        result = rule(root)
        self.assertEquals(result[0].getnext().attrib['id'], 'content')

    def test_after_rule(self):
        root = self.get_root()
        footer = CSS('#footer')
        content = CSS("#content")
        rule = After(content, footer)
        result = rule(root)

        self.assertEquals(result[0].getprevious().attrib['id'], 'footer')

    def test_drop_rule(self):
        root = self.get_root()
        footer = CSS('#footer')
        rule = Drop(footer)
        rule(root)

        self.assertEquals(len(footer(root)), 0)

    def test_replace_rule(self):
        root = self.get_root()
        footer = CSS('#footer')
        content = CSS("#content")
        rule = Replace(content, footer)
        rule(root)

        self.assertEquals(len(footer(root)), 0)
        self.assertEquals(len(content(root)), 1)

    def test_class_rule(self):
        root = self.get_root()
        footer = CSS("#footer")
        rule = Class(footer, add="foobar")
        rule(root)

        self.assertEquals(footer(root)[0].attrib['class'], 'foobar')

    def test_group_rule(self):
        root = self.get_root()
        footer = CSS('#footer')
        content = CSS("#content")
        condition = IfContent(footer)
        droprule = Drop(content)
        rule = Group(rules=[droprule], conditions=[condition])
        rule(root)

        self.assertEquals(len(content(root)), 0)
        self.assertEquals(len(footer(root)), 1)

    def test_group_false_rule(self):
        root = self.get_root()
        foobar = CSS('#foobar')
        content = CSS("#content")
        condition = IfContent(foobar)
        droprule = Drop(content)
        rule = Group(rules=[droprule], conditions=[condition])
        rule(root)

        self.assertEquals(len(content(root)), 1)
        self.assertEquals(len(foobar(root)), 0)

    def test_tag_rule(self):
        root = self.get_root()
        foobar = CSS('#footer')
        tagrule = Tag(foobar, tag='p')
        tagrule(root)

        self.assertEquals(len(foobar(root)), 1)
        self.assertEquals(foobar(root)[0].tag, 'p')

if __name__ == '__main__':
    unittest.main()
