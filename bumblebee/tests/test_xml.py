import unittest
from bumblebee.xml import convertRules
from bumblebee.rules import Before
from bumblebee.rules import After
from bumblebee.rules import Drop
from bumblebee.rules import Replace
from bumblebee.rules import Class
from bumblebee.rules import Group
from bumblebee.rules import Tag
from bumblebee.selectors import NodeHTML


class TestXMLToRules(unittest.TestCase):

    def test_before_rule(self):
        rules = convertRules("""<xml>
<before src="#foo" dst="#bar" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Before)
        self.assertEquals(rules[0].src.selector, '#foo')
        self.assertEquals(rules[0].dst.selector, '#bar')

    def test_after_rule(self):
        rules = convertRules("""<xml>
<after src="#foo" dst="#bar" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), After)
        self.assertEquals(rules[0].src.selector, '#foo')
        self.assertEquals(rules[0].dst.selector, '#bar')

    def test_drop_rule(self):
        rules = convertRules("""<xml>
<drop src="#foo" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Drop)
        self.assertEquals(rules[0].src.selector, '#foo')

    def test_replace_rule(self):
        rules = convertRules("""<xml>
<replace src="#foo" dst="#bar" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Replace)
        self.assertEquals(rules[0].src.selector, '#foo')
        self.assertEquals(rules[0].dst.selector, '#bar')

    def test_class_rule(self):
        rules = convertRules("""<xml>
<class src="#foo" add="one two" remove="three four" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Class)
        self.assertEquals(rules[0].src.selector, '#foo')
        self.assertEquals(rules[0].add, ['one', 'two'])
        self.assertEquals(rules[0].remove, ['three', 'four'])

    def test_group_rule(self):
        rules = convertRules("""<xml>
<group if-content="#foo">
        <drop src="#bar" />
    </group></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Group)

    def test_tag_rule(self):
        rules = convertRules("""<xml>
<tag src="#foo" tag="p" /></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), Tag)


class TestXMLToRulesSelectors(unittest.TestCase):

    def test_html_selectors(self):
        rules = convertRules("""<xml>
<after src-html="" dst="#bar">
<h1>Hi!</h1>
</after></xml>""")
        self.assertEquals(len(rules), 1)
        self.assertEquals(type(rules[0]), After)
        self.assertEquals(type(rules[0].src), NodeHTML)

if __name__ == '__main__':
    unittest.main()
